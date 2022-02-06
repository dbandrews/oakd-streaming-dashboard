import socket
import os

import pandas as pd
import dash
import plotly
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
from dotenv import load_dotenv


def get_detections(num_detections):
    HOST, PORT = os.environ["HOST"], os.environ["PORT"]
    # Create a socket (SOCK_STREAM means a TCP socket)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and get header data
        sock.connect((HOST, PORT))
        header = str(sock.recv(1024), "utf-8")
        detections = []
        for i in range(num_detections):
            detections.append(str(sock.recv(1024), "utf-8"))

    return pd.DataFrame(data=detections, columns=["class", "confidence", "x", "y", "z"])


app = dash.Dash()

app.layout = html.Div(
    [
        html.H1("3D Object Detection Stream"),
        dcc.Graph(id="detections"),
        html.Div(id="my-output-interval"),
        dcc.Interval(id="my-interval", interval=1000),
    ]
)


@app.callback(Output("detections", "figure"), [Input("my-interval", "n_intervals")])
def display_output(n):

    # Get detections
    detections = get_detections(10)

    # Create figure
    # Create the graph with subplots
    fig = plotly.tools.make_subplots(rows=2, cols=1, vertical_spacing=0.2)
    fig["layout"]["margin"] = {"l": 30, "r": 10, "b": 30, "t": 10}
    fig["layout"]["legend"] = {"x": 0, "y": 1, "xanchor": "left"}

    fig.append_trace(
        {
            "x": data["time"],
            "y": data["Altitude"],
            "name": "Altitude",
            "mode": "lines+markers",
            "type": "scatter",
        },
        1,
        1,
    )
    fig.append_trace(
        {
            "x": data["Longitude"],
            "y": data["Latitude"],
            "text": data["time"],
            "name": "Longitude vs Latitude",
            "mode": "lines+markers",
            "type": "scatter",
        },
        2,
        1,
    )


if __name__ == "__main__":
    load_dotenv()
    app.run_server(debug=True, threaded=False)
