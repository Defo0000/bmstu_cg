from mirror import *
from math import *

def middle_point_circle(radius, x_center, y_center):
    dots = []

    x = 0
    y = radius

    dots.append(Point(x + x_center, y + y_center))

    # delta = (x + 1)^2 + (y - 0.5)^2 - radius^2 = [x = 0, y = radius] = 1.25 - radius
    delta = 1.25 - radius

    while y > x:
        x += 1

        if delta >= 0:  # Средняя точка вне окружности
            y -= 1  # Выбирается диагональный пиксель
            delta += 2 * x - 2 * y + 5
        else:
            delta += 2 * x + 3  # Выбирается горизонтальный пиксель

        dots.append(Point(x + x_center, y + y_center))

    dots = mirror_circle(dots, x_center, y_center)

    return dots

def middle_point_ellipse(a, b, x_center, y_center):
    dots = []

    a2 = a * a
    b2 = b * b

    x = 0
    y = b
    dots.append(Point(x + x_center, y + y_center))

    limit = round(a / sqrt(1 + b2 / a2))
    delta = b2 - round(a2 * (b - 0.25))
    while x < limit:

        if delta > 0:
            y -= 1
            x += 1
            delta += b2 * (2 * x + 1)
            delta -= 2 * a2 * y
        else:
            x += 1
            delta += b2 * (2 * x + 1)
        dots.append(Point(x + x_center, y + y_center))

    x = a
    y = 0

    n = len(dots)

    limit = round(b / sqrt(1 + a2 / b2))
    delta = a2 - round(b2 * (a - 0.25))
    while y < limit:

        if delta > 0:
            x -= 1
            y += 1
            delta -= 2 * b2 * x
            delta += a2 * (2 * y + 1)
        else:
            y += 1
            delta += a2 * (2 * y + 1)
        dots.append(Point(x + x_center, y + y_center))

    # Необходимо для корректного расположения точек в массиве (друг за другом) для последующего отображения и рисовки
    reverse = dots[n:]
    reverse = reverse[::-1]
    dots = dots[:n] + reverse

    dots = mirror_ellipse(dots, x_center, y_center)

    return dots