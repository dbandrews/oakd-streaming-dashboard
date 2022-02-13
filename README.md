# OAKD Streaming Dashboard

A Dash app for streaming detections from an OpenCV OAKD spatial AI camera. 

For use with [`oakd-streaming`](https://github.com/dbandrews/oakd-streaming). Relies on HTTP server streaming the video feed, and a TCP server streaming the detected classes and coordinates. See the repo for more details.

## Demo

![demo](/visuals/oakd.gif)

## Setup

Setup `conda` env with:

```
conda env create -f environment.yaml
```

Setup a `.env` file containg lines:

```
TCP_HOST="<IP_ADDRESS_OF_DEVICE_STREAMING_OAKD>"
TCP_PORT=<PORT_DETECTIONS_STREAMED_ON>
HTTP_PORT=<PORT_HTTP_SERVER_STREAMED_ON>
```

These variables correspond to the variables used in the [`oakd-streaming`](https://github.com/dbandrews/oakd-streaming) script.

## Running

Run with:

```
conda activate oakd-dashboard
python app.py
```

## Limitations/Improvements Needed

- [ ] Use of TCP socket is inefficient as it keeps getting created and closed. Need to keep alive for quicker use in callback
- [ ] Hard coded color map for MobileNet SSD Classes
- [ ] No color bar for classes
