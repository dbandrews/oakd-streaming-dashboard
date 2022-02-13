import socket
import os
from click import style

import pandas as pd
import dash
import plotly.express as px
from dash.dependencies import Input, Output
from dash import dcc, html
import dash_bootstrap_components as dbc
from dotenv import load_dotenv

from colors import color_lookup


load_dotenv()


def get_detections(num_detections):
    HOST, PORT = os.environ["TCP_HOST"], int(os.environ["TCP_PORT"])
    # Create a socket (SOCK_STREAM means a TCP socket)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and get header data
        sock.connect((HOST, PORT))
        detections = str(sock.recv(1024 * num_detections), "utf-8")
        detections_out = detections.split("\r\n")
        detections_out = [x.split(",") for x in detections_out][0]

    return pd.DataFrame(
        data=[detections_out], columns=["class", "confidence", "x", "y", "z"]
    )


app = dash.Dash(
    __name__,
    update_title=None,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)

app.layout = dbc.Container(
    children=[
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.H1("3D Object Detection Stream"),
                        dcc.Graph(
                            id="detections",
                            figure={
                                "layout": {
                                    "title": "Object Detections in 3D",
                                    "barmode": "overlay",
                                    "margin": dict(b=30, t=30),
                                    # "size": dict(width="50vh", height="1000px"),
                                    "uirevision": False,
                                },
                                "data": [
                                    {
                                        "x": [],
                                        "y": [],
                                        "z": [],
                                        "text": [],
                                        "marker": {
                                            "color": [],
                                            "size": 10,
                                            # "colorbar": {"title": "Class"},
                                            # "colorscale": list(zip(color_lookup)),
                                            # "colorscale": "Viridis",
                                        },
                                        "mode": "markers",
                                        "type": "scatter3d",
                                    }
                                ],
                            },
                        ),
                        dcc.Interval(id="my-interval", interval=300),
                    ],
                    width=True,
                ),
            ],
            class_name="g-0",
        ),
        dbc.Row(
            children=[
                # Add a shim because output from OAKD video feeds is off center
                dbc.Col(html.Div(), width={"size": 3}),
                dbc.Col(
                    html.Iframe(
                        src=f"http://{os.environ['TCP_HOST']}:{os.environ['HTTP_PORT']}/",
                        style={"width": "100vh", "height": "100vh"},
                    ),
                    width=True,
                ),
            ],
            justify="evenly",
            class_name="g-0",
        ),
    ],
    style={"height": "100vh"},
)


@app.callback(Output("detections", "extendData"), [Input("my-interval", "n_intervals")])
def display_output(n):

    # Get detections
    detections = get_detections(1)

    # return new data
    return (
        {
            "marker.color": [
                [
                    color_lookup[x]  # if x != "" else "black"
                    for x in detections["class"].to_list()
                ]
            ],
            "text": [detections["class"].to_list()],
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

    app.run_server(debug=True, host="localhost", port=8050)
