from math import sqrt, sin, cos, exp

def f1(x, z):
    return sin(x) ** 2 + cos(z) ** 2

def f2(x, z):
    return x ** 2 / 20 - z ** 2 / 20

def f3(x, z):
    return exp(sin(sqrt(x ** 2 + z ** 2)))

def f4(x, z):
    return x ** 2 / 20 + z ** 2 / 20

def f5(x, z):
    return x * z / 25

def f6(x, z):
    return cos(x)