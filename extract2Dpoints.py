import bpy
import numpy as np


image = '1992_007.jpg'
clip = bpy.data.movieclips[image]

# Dimension du movieclip
width, height = clip.size

# 

trackpoints = clip.tracking.tracks

for trackpoint in trackpoints :
    name = trackpoint.name
    x, y = trackpoint.markers.find_frame(1).co
    x = round(x*width)
    y = round(y*height)
    print(name, x, y)