from mirror import *
from math import *

def middle_point_circle(radius, x_center, y_center):
    dots = []

    x = radius
    y = 0

    dots.append(Point(x + x_center, y + y_center))

    # delta = (x - 0.5)^2 + (y + 1)^2 - radius^2 = [x = radius, y = 0] = 1.25 - radius
    delta = 1.25 - radius

    while x > y:
        y += 1

        if delta > 0:  # Средняя точка вне окружности
            x -= 1  # Выбирается диагональный пиксель
            delta -= x + x - 2

        delta += y + y + 3  # Выбирается горизонтальный пиксель

        dots.append(Point(x + x_center, y + y_center))

    dots = mirror_circle(dots, x_center, y_center)

    return dots

def middle_point_ellipse(a, b, x_center, y_center):
    dots = []

    a2 = a * a
    b2 = b * b
    bd = 2 * b2
    ad = 2 * a2

    x = 0
    y = b
    dots.append(Point(x + x_center, y + y_center))

    limit = round(a / sqrt(1 + b2 / a2))
    f = b2 - round(a2 * (b - 0.25))
    while x < limit:

        if f > 0:
            y -= 1
            f -= ad * y
        x += 1
        f += b2 * (2 * x + 1)

        dots.append(Point(x + x_center, y + y_center))

    x = a
    y = 0

    limit = round(b / sqrt(1 + a2 / b2))
    f = a2 - round(b2 * (a - 0.25))
    while y < limit:

        if f > 0:
            x -= 1
            f -= bd * x
        y += 1
        f += a2 * (2 * y + 1)

        dots.append(Point(x + x_center, y + y_center))

    dots = mirror_ellipse(dots, x_center, y_center)

    return dots