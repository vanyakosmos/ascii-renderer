from math import cos, sin
from typing import NamedTuple

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
