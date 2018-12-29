import random
from math import cos, sin

import numpy as np
from numba import jit


@jit(nopython=True)
def dist(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.sqrt(np.sum((a - b) ** 2))


@jit(nopython=True)
def rel(x, y, buff):
    h, w = buff.shape
    return x / w, y / h


@jit(nopython=True)
def bound(v, a=0, b=1):
    return min(b, max(a, v))


@jit(nopython=True)
def waves(x, y, time, texture, buff):
    x_, y_ = rel(x, y, buff)
    r = abs(cos(sin(time * 2 + 2 * x_) * 3 * y_ + time))
    s = 2
    p = texture[max(0, y - s):y + s, max(0, x - s):x + s].mean()
    return r * p


@jit(nopython=True)
def eyes(x, y, time, texture, buff):
    x_, y_ = rel(x, y, buff)
    p = texture[y, x]
    return (sin(time + x_ * 10) + cos(time + y_ * 10)) * p


@jit(nopython=True)
def pulsar(x, y, time, texture, buff):
    x_, y_ = rel(x, y, buff)
    cx, cy = 0.5, 0.5
    r = dist([cx, cy], [x_, y_])
    t = time % 1.
    if r > t:
        return 0
    p = texture[y, x]
    return (1 - t) * p


@jit(nopython=True)
def julia(x, y, time, texture, buff):
    maxIter = 15
    zoom = 1
    r = 0.7885
    h, w = buff.shape
    cx = r * cos(time)
    cy = r * sin(time)
    moveX, moveY = 0., 0.
    # algo
    zx = 1.5 * (x - w / 2) / (0.5 * zoom * w) + moveX
    zy = 1.0 * (y - h / 2) / (0.5 * zoom * h) + moveY
    i = maxIter
    while zx * zx + zy * zy < 4 and i > 1:
        tmp = zx * zx - zy * zy + cx
        zy, zx = 2.0 * zx * zy + cy, tmp
        i -= 1
    i = i / maxIter
    # i = abs(i - buff[y, x])
    return i


@jit(nopython=True)
def doom_fire(x, y, time, texture, buff):
    """
    http://fabiensanglard.net/doom_fire_psx/
    """
    h, w = buff.shape
    if y == h - 1:
        return 1.0
    ry = random.randint(0, 1)
    rx = random.randint(-1, 1)
    p = buff[bound(y + ry, 0, h - 1), bound(x + rx, 0, w - 1)]
    return p - 0.03 * random.random()
