from mirror import *
from math import *

def parametric_circle(radius, x_center, y_center):
    dots = []

    step = round(1 / radius) + 1
    for t in range(90, 45, -step):
        x = x_center + radius * cos(radians(t))
        y = y_center + radius * sin(radians(t))
        dots.append(Point(x, y))

    dots = mirror_circle(dots, x_center, y_center)

    return dots


def parametric_ellipse(a, b, x_center, y_center):
    dots = []

    step = round(1 / max(a, b)) + 1
    for t in range(90, 0, -step):
        x = x_center + a * cos(radians(t))
        y = y_center + b * sin(radians(t))
        dots.append(Point(x, y))

    dots = mirror_ellipse(dots, x_center, y_center)

    return dots