from mirror import *
from math import *

def canonical_circle(radius, x_center, y_center):
    dots = []

    x_center = int(x_center)
    y_center = int(y_center)

    for x in range(x_center, round(x_center + radius / sqrt(2)) + 1):
        y = y_center + sqrt(radius ** 2 - (x - x_center) ** 2)
        dots.append(Point(x, y))

    dots = mirror_circle(dots, x_center, y_center)

    return dots

def canonical_ellipse(a, b, x_center, y_center):
    dots = []

    x_center = int(x_center)
    y_center = int(y_center)

    limit = round(x_center + a / sqrt(1 + b ** 2 / a ** 2))

    for x in range(x_center, limit):
        y = y_center + sqrt(a ** 2 * b ** 2 - (x - x_center) ** 2 * b ** 2) / a
        dots.append(Point(x, y))

    limit = round(y_center + b / sqrt(1 + a ** 2 / b ** 2))

    for y in range(limit, y_center - 1, -1):
        x = x_center + sqrt(a ** 2 * b ** 2 - (y - y_center) ** 2 * a ** 2) / b
        dots.append(Point(x, y))

    dots = mirror_ellipse(dots, x_center, y_center)

    return dots