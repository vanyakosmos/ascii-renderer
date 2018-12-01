import numpy as np


def to_vec(*args, **kwargs):
    def dec(f):
        return np.vectorize(f, *args, **kwargs)

    return dec
