import pandas as pd
import numpy as np
import os
import sys
import datetime

def load_room_boundaries():
    boudaries_file = open("data/Boundaries.txt", "r")
    room_class_files = open("data/room_classes.txt", "r")
    boundaries = dict()
    room_classes = dict()
    for line in boudaries_file:
        line = line.split()
        if line[0] == "#":
            continue
        class_ = line[0]
        ANP0020_action = (line[1], line[2])
        ANP0020_alert = (line[3], line[4])
        ANP0019_action = line[5]
        ANP0019_alert = line[6]
        ANP0230_action = line[8]
        ANP0230_alert = line[9]
        boundaries[class_] = {"ANP0020_action": ANP0020_action, "ANP0020_alert": ANP0020_alert,
                              "ANP0019_action": ANP0019_action, "ANP0019_alert": ANP0019_alert,
                              "ANP0230_action": ANP0230_action, "ANP0230_alert": ANP0230_alert}

    for line in room_class_files:
        line = line.split()
        room = line[0]
        class_ = line[1]
        location = line[2]
        room_classes[room] = {"class": class_, "location": location, "ANP0020_action": boundaries[class_]["ANP0020_action"], "ANP0020_alert": boundaries[class_]["ANP0020_alert"],
                              "ANP0019_action": boundaries[class_]["ANP0019_action"], "ANP0019_alert": boundaries[class_]["ANP0019_alert"],
                              "ANP0230_action": boundaries[class_]["ANP0230_action"], "ANP0230_alert": boundaries[class_]["ANP0230_alert"]}
    return room_classes

def load_color_codes():
    file_with_color_codes = open("data/colorcodes.txt")
    colors = dict()
    for line in file_with_color_codes:
        line = line.split()
        color = " ".join(line[:-1])
        code = line[-1]
        colors[color] = code
    return colors


room_classes = load_room_boundaries()