from mirror import *
from math import *
import numpy as np

def parametric_circle(radius, x_center, y_center):
    dots = []

    step = 1 / radius
    for t in np.arange(pi / 2, pi / 4, -step):
        x = x_center + radius * cos(t)
        y = y_center + radius * sin(t)
        dots.append(Point(x, y))

    dots = mirror_circle(dots, x_center, y_center)

    return dots


def parametric_ellipse(a, b, x_center, y_center):
    dots = []

    step = 1 / max(a, b)
    for t in np.arange(pi/2, 0, -step):
        x = x_center + a * cos(t)
        y = y_center + b * sin(t)
        dots.append(Point(x, y))

    dots = mirror_ellipse(dots, x_center, y_center)

    return dots