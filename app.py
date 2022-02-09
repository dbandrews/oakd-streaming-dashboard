import socket
import os
import random

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
                    "margin": dict(l=10, r=10, b=0, t=30),
                    "size": dict(width="50vh", height="50vh"),
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
                            "colorbar": {"title": "Class"},
                            "colorscale": "Viridis",
                        },
                        "mode": "markers",
                        "type": "scatter3d",
                    }
                ],
            },
        ),
        dcc.Interval(id="my-interval", interval=100),
    ]
)

# Setup for MobileNet class color scheme
colors = [
    "DarkOrange",  # FF8C00	255, 140, 0
    "DarkOrchid",  # 9932CC	153, 50, 204
    "DarkRed",  # 8B0000	139, 0, 0
    "DarkSalmon",  # E9967A	233, 150, 122
    "DarkSeaGreen",  # 8FBC8F	143, 188, 143
    "DarkSlateBlue",  # 483D8B	72, 61, 139
    "DarkSlateGray",  # 2F4F4F	47, 79, 79
    "DarkSlateGrey",  # 2F4F4F	47, 79, 79
    "DarkTurquoise",  # 00CED1	0, 206, 209
    "DarkViolet",  # 9400D3	148, 0, 211
    "DeepPink",  # FF1493	255, 20, 147
    "DeepSkyBlue",  # 00BFFF	0, 191, 255
    "DimGray",  # 696969	105, 105, 105
    "DodgerBlue",  # 1E90FF	30, 144, 255
    "FireBrick",  # B22222	178, 34, 34
    "FloralWhite",  # FFFAF0	255, 250, 240
    "ForestGreen",  # 228B22	34, 139, 34
    "Fuchsia",  # FF00FF	255, 0, 255
    "Gainsboro",
    "Gold",
    "GoldenRod",
]

# MobilenetSSD label texts
classes = [
    "background",
    "aeroplane",
    "bicycle",
    "bird",
    "boat",
    "bottle",
    "bus",
    "car",
    "cat",
    "chair",
    "cow",
    "diningtable",
    "dog",
    "horse",
    "motorbike",
    "person",
    "pottedplant",
    "sheep",
    "sofa",
    "train",
    "tvmonitor",
]

color_lookup = {x: y for x, y in zip(classes, colors)}


@app.callback(Output("detections", "extendData"), [Input("my-interval", "n_intervals")])
def display_output(n):

    # Get detections
    detections = get_detections(1)

    # return new data
    return (
        {
            "marker.color": [detections["class"].to_list()],
            "marker.color": [
                [
                    color_lookup[x] if x != "" else "black"
                    for x in detections["class"].to_list()
                ]
            ],
            "text": [
                detections["class"].to_list(),
            ],
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
        10000,  # Max number of detections
    )

    return fig


if __name__ == "__main__":
    load_dotenv()
    app.run_server(debug=True, host="localhost", port=8050)
