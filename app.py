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
                            # "colorscale": "Viridis",
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
    "darkorange",  # ff8c00	255, 140, 0
    "darkorchid",  # 9932cc	153, 50, 204
    "darkred",  # 8b0000	139, 0, 0
    "darksalmon",  # e9967a	233, 150, 122
    "darkseagreen",  # 8fbc8f	143, 188, 143
    "darkslateblue",  # 483d8b	72, 61, 139
    "darkslategray",  # 2f4f4f	47, 79, 79
    "darkslategrey",  # 2f4f4f	47, 79, 79
    "darkturquoise",  # 00ced1	0, 206, 209
    "darkviolet",  # 9400d3	148, 0, 211
    "deeppink",  # ff1493	255, 20, 147
    "deepskyblue",  # 00bfff	0, 191, 255
    "dimgray",  # 696969	105, 105, 105
    "dodgerblue",  # 1e90ff	30, 144, 255
    "firebrick",  # b22222	178, 34, 34
    "hotpink",  # fffaf0	255, 250, 240
    "forestgreen",  # 228b22	34, 139, 34
    "fuchsia",  # ff00ff	255, 0, 255
    "gainsboro",
    "gold",
    "goldenrod",
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
    load_dotenv()
    app.run_server(debug=True, host="localhost", port=8050)
