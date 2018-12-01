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
def waves(x, y, time, buff):
    x_, y_ = rel(x, y, buff)
    r = abs(cos(sin(time * 5 + 2 * x_) * 3 * y_ + time))
    s = 2
    p = buff[max(0, y - s):y + s, max(0, x - s):x + s].mean()
    return r * p


@jit(nopython=True)
def eyes(x, y, time, buff):
    x_, y_ = rel(x, y, buff)
    p = buff[y, x]
    return (sin(time + x_ * 10) + cos(time + y_ * 10)) * p


@jit(nopython=True)
def pulsar(x, y, time, buff):
    x_, y_ = rel(x, y, buff)
    cx, cy = 0.5, 0.5
    r = dist([cx, cy], [x_, y_])
    t = time % 1.
    if r > t:
        return 0
    p = buff[y, x]
    return (1 - t) * p
