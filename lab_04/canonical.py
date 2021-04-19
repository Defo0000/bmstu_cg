from mirror import *
from math import *

def canonical_circle(radius, x_center, y_center):
    dots = []

    for x in range(int(x_center), round(x_center + radius / sqrt(2)) + 1):
        y = sqrt(radius * radius - (x - x_center) * (x - x_center)) + y_center
        dots.append(Point(x, y))

    dots = mirror_circle(dots, x_center, y_center)

    return dots

def canonical_ellipse(a, b, x_center, y_center):
    dots = []

    a2 = a * a
    b2 = b * b

    limit = round(x_center + a / sqrt(1 + b2 / a2))

    for x in range(int(x_center), limit):
        y = y_center + b * sqrt(a2 - (x - x_center) * (x - x_center)) / a
        dots.append(Point(x, y))

    limit = round(y_center + b / sqrt(1 + a2 / b2))

    for y in range(limit, int(y_center) - 1, -1):
        x = x_center + a * sqrt(b2 - (y - y_center) * (y - y_center)) / b
        dots.append(Point(x, y))

    dots = mirror_ellipse(dots, x_center, y_center)

    return dots