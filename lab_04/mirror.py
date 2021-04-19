from point import *

def mirror_circle(dots, x_center, y_center):
    dots = mirror_bisect(dots, x_center, y_center)
    dots = mirror_x_axis(dots, y_center)
    dots = mirror_y_axis(dots, x_center)

    return dots


def mirror_bisect(dots, x_center, y_center):
    mirror_dots = []

    for i in range(len(dots) - 1, 0, -1):
        x = x_center + (dots[i].y - y_center)
        y = y_center + (dots[i].x - x_center)
        mirror_dots.append(Point(x, y))

    return dots + mirror_dots


def mirror_x_axis(dots, y_center):
    mirror_dots = []

    for i in range(len(dots) - 1, 0, -1):
        x = dots[i].x
        y = 2 * y_center - dots[i].y
        mirror_dots.append(Point(x, y))

    return dots + mirror_dots


def mirror_y_axis(dots, x_center):
    mirror_dots = []

    for i in range(len(dots) - 1, 0, -1):
        x = 2 * x_center - dots[i].x
        y = dots[i].y
        mirror_dots.append(Point(x, y))

    return dots + mirror_dots
