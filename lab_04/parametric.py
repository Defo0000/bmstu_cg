from mirror import *
from math import *

def parametric_circle(radius, x_center, y_center):
    dots = []

    step = round(1 / radius) + 1
    for angle in range(90, 45, -step):
        x = x_center + radius * cos(radians(angle))
        y = y_center + radius * sin(radians(angle))
        dots.append(Point(x, y))

    dots = mirror_circle(dots, x_center, y_center)

    return dots


def parametrical_ellipse(a, b, x_center, y_center):
    dots = []

    return dots