from mirror import *
from math import *

def canonical_circle(radius, x_center, y_center):
    dots = []

    for x in range(int(x_center), round(x_center + radius / sqrt(2)) + 1):
        y = sqrt(radius * radius - (x - x_center) * (x - x_center)) + y_center
        dots.append(Point(x, y))

    dots = mirror_circle(dots, x_center, y_center)

    return dots

def canonical_ellipse():
    pass