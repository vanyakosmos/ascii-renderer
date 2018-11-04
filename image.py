import numpy as np
from PIL import Image


def get_size(im, width, height):
    if width == -1 and height == -1:
        width, height = im.size
    elif width == -1:
        w, h = im.size
        width = int(w / h * height)
    elif height == -1:
        w, h = im.size
        height = int(h / w * width)
    return width, height


def get_image(path, width=-1, height=-1):
    im = Image.open(path).convert('I')

    w, h = get_size(im, width, height)
    im = im.resize([w, h])
    arr = np.array(im, dtype=np.float)
    arr /= 255
    return arr
