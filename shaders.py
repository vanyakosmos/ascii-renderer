from math import cos, sin
from typing import NamedTuple

import numpy as np
from numpy import ndarray


class Data(NamedTuple):
    # position
    x: int
    y: int
    # canvas size
    w: int
    h: int
    # misc
    time: float
    buff: ndarray


def dist(a, b):
    a = np.asarray(a)
    b = np.asarray(b)
    return np.sqrt(np.sum((a - b) ** 2))


def waves(d: Data):
    x = d.x / d.w
    y = d.y / d.h
    r = abs(cos(sin(d.time + 2 * x) * 3 * y + d.time))
    s = 2
    p = d.buff[max(0, d.y - s):d.y + s, max(0, d.x - s):d.x + s].mean()
    return r * p


def eyes(d: Data):
    x = d.x / d.w
    y = d.y / d.h
    p = d.buff[d.y, d.x]
    return 1 - (sin(d.time + x * 10) + cos(d.time + y * 10)) * p


def pulsar(d: Data):
    x = d.x / d.w
    y = d.y / d.h
    cx, cy = 0.5, 0.5
    r = dist([cx, cy], [x, y])
    t = d.time % 1.
    if r > t:
        return 0
    p = d.buff[d.y, d.x]
    return (1 - t) * p
