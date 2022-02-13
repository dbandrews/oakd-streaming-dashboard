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
