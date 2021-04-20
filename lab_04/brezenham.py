from mirror import *
from math import *

def brezenham_circle(radius, x_center, y_center):
    dots = []

    x = 0
    y = radius

    dots.append(Point(x + x_center, y + y_center))

    # (x0 + 1) ^ 2 + (y0 - 1) ^ 2 - radius ^ 2 = [x0 = 0, y0 = radius] = 2 - 2 * radius
    delta = 2 - 2 * radius

    while x < y:

        if delta <= 0:  # Внутри или на окружности

            delta_1 = 2 * (delta + y) - 1  # Разность расстояний горизонтального и диагонального пискелей до окружности
            if delta_1 < 0:  # Горизонтальный ближе
                x += 1
                delta += 2 * x + 1
            else:  # Диагональный ближе
                x += 1
                y -= 1
                delta += 2 * (x - y + 1)

        else:  # Вне окружности

            delta_2 = 2 * (delta - x) - 1  # Разность расстояний диагонального и вертикального пискелей до окружности
            if delta_2 < 0:  # Диагональный ближе
                x += 1
                y -= 1
                delta += 2 * (x - y + 1)
            else:  # Вертикальный ближе
                y -= 1
                delta += 1 - 2 * y

        dots.append(Point(x + x_center, y + y_center))

    dots = mirror_circle(dots, x_center, y_center)

    return dots

def brezenham_ellipse(a, b, x_center, y_center):
    dots = []

    a2 = a * a
    b2 = b * b

    x = 0
    y = b
    dots.append(Point(x + x_center, y + y_center))

    # (x + 1)^2 / a^2 + (y - 1)^2 / b^2 - 1  ~~  b2 * (x + 1)^2 + a^2 * (y - 1)^2 - a^2*b^2 =
    # = [x = 0, y = b] = b^2 + a^2 * (b - 1)^2 - a^2*b^2 = b^2 - 2*a^2*b + a^2 = b^2 - a^2 * (2 * b - 1)
    delta = b2 - a2 * (2 * b - 1)

    while y > 0:

        if delta <= 0:  # Если внутри эллипса или на нем

            delta_1 = 2 * delta + a2 * (2 * y - 1)  # Разность расстояний горизонтального и диагонального пискелей до эллипса
            if delta_1 < 0:  # Горизонтальный ближе
                x += 1
                delta += b2 * (2 * x + 1)
            else:  # Диагональный ближе
                x += 1
                y -= 1
                delta += b2 * (2 * x + 1)
                delta += a2 * (1 - 2 * y)

        else:  # Если вне эллипса
            delta_2 = 2 * delta - b2 * (2 * x + 1) # Разность расстояний диагонального и вертикального пискелей до эллипса
            if delta_2 < 0:  # Диагональный ближе
                x += 1
                y -= 1
                delta += a2 * (1 - 2 * y)
                delta += b2 * (2 * x + 1)
            else:  # Вертикальный ближе
                y -= 1
                delta += a2 * (1 - 2 * y)

        dots.append(Point(x + x_center, y + y_center))

    dots = mirror_ellipse(dots, x_center, y_center)

    return dots