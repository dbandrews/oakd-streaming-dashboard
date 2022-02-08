import socket
import os

import pandas as pd
import dash
import plotly
import plotly.express as px
from dash.dependencies import Input, Output
from dash import dcc, html
from dotenv import load_dotenv


def get_detections(num_detections):
    HOST, PORT = os.environ["TCP_HOST"], int(os.environ["TCP_PORT"])
    # HOST, PORT = "192.168.0.13", 8070
    # Create a socket (SOCK_STREAM means a TCP socket)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and get header data
        sock.connect((HOST, PORT))
        detections = str(sock.recv(1024 * num_detections), "utf-8")
        detections_out = detections.split("\r\n")
        detections_out = [x.split(",") for x in detections_out]
        # detections.append(str(sock.recv(1024), "utf-8").strip().split(","))

    # detections = [
    #     ["chair", "95%", 1, 1, 1],
    #     ["cat", "95%", 1, 1, 1],
    #     ["dog", "95%", 1, 1, 1],
    # ]
    # print(detections)

    return pd.DataFrame(
        data=detections_out, columns=["class", "confidence", "x", "y", "z"]
    )


app = dash.Dash(__name__, update_title=None)

app.layout = html.Div(
    [
        html.H1("3D Object Detection Stream"),
        dcc.Graph(
            id="detections",
            figure={
                "layout": {
                    "title": "Object Detections in 3D",
                    "barmode": "overlay",
                    "margin": dict(l=10, r=10, b=10, t=10),
                    "size": dict(width=1000, height=1000),
                    "uirevision": True,
                },
                "data": [
                    {
                        "x": [],
                        "y": [],
                        "z": [],
                        "marker": {"color": []},
                        "mode": "markers",
                        "type": "scatter3d",
                    }
                ],
            },
        ),
        dcc.Interval(id="my-interval", interval=100),
    ]
)


@app.callback(Output("detections", "extendData"), [Input("my-interval", "n_intervals")])
def display_output(n):

    # Get detections
    detections = get_detections(1)

    # return new data
    return (
        {
            "marker.color": [detections["class"].to_list()],
            "x": [
                detections["x"].to_list(),
            ],
            "y": [
                detections["y"].to_list(),
            ],
            "z": [
                detections["z"].to_list(),
            ],
        },
        [0],
        100,  # Max number of detections
    )

    return fig


if __name__ == "__main__":
    load_dotenv()
    app.run_server(debug=True, host="localhost", port=8050)
