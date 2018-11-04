from math import cos, sin

from typing import NamedTuple
from functools import partial


class Data(NamedTuple):
    x: float
    y: float
    time: float
    pix: float


def waves_(pass_pix, d: Data):
    p = d.pix if pass_pix else 1
    return abs(cos(sin(d.time + 2 * d.x * p) * 3 * d.y * p + d.time))


def waves(pass_pix=True):
    return partial(waves_, pass_pix)


def eyes(d: Data):
    return 1 - (sin(d.time + d.x * 10) + cos(d.time + d.y * 10))
