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
    # HOST, PORT = os.environ["TCP_HOST"], os.environ["TCP_PORT"]
    # HOST, PORT = "192.168.0.13", 8070
    # Create a socket (SOCK_STREAM means a TCP socket)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and get header data
        sock.connect((HOST, PORT))
        header = str(sock.recv(1024), "utf-8")
        detections = []
        for i in range(num_detections):
            detections.append(str(sock.recv(1024), "utf-8").strip().split(","))

    # detections = [
    #     ["chair", "95%", 1, 1, 1],
    #     ["cat", "95%", 1, 1, 1],
    #     ["dog", "95%", 1, 1, 1],
    # ]
    print(detections)

    return pd.DataFrame(data=detections, columns=["class", "confidence", "x", "y", "z"])


app = dash.Dash()

app.layout = html.Div(
    [
        html.H1("3D Object Detection Stream"),
        dcc.Graph(id="detections"),
        dcc.Interval(id="my-interval", interval=1000),
    ]
)


@app.callback(Output("detections", "figure"), [Input("my-interval", "n_intervals")])
def display_output(n):

    # Get detections
    detections = get_detections(1)

    # Create figure
    # Create the graph with subplots
    fig = plotly.subplots.make_subplots(rows=2, cols=1, vertical_spacing=0.2)
    fig["layout"]["margin"] = {"l": 30, "r": 10, "b": 30, "t": 10}
    fig["layout"]["legend"] = {"x": 0, "y": 1, "xanchor": "left"}

    fig.append_trace(
        {
            "x": detections["class"],
            # "y": data["Altitude"],
            "name": "Classes",
            # "mode": "lines+markers",
            "type": "bar",
        },
        1,
        1,
    )
    fig.append_trace(
        {
            "x": detections["x"],
            "y": detections["y"],
            # "z": detections["z"],
            "text": detections["class"],
            "name": "3D Points",
            "mode": "markers",
            "type": "scatter",
        },
        2,
        1,
    )

    return fig


if __name__ == "__main__":
    load_dotenv()
    app.run_server(debug=True, host="localhost", port=8050)
