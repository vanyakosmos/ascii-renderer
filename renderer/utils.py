from time import sleep, time

import numpy as np


def to_vec(*args, **kwargs):
    def dec(f):
        return np.vectorize(f, *args, **kwargs)

    return dec


def keep_steady_fps(s, fps):
    """
    :param s: start time of frame
    :param fps: targeted FpS
    """
    t = (1 / fps - (time() - s)) / 2
    if t > 0:
        sleep(t)
