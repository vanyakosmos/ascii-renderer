from PIL import Image
import numpy as np


def get_size(im, width, height):
    if width is None and height is None:
        width, height = im.size
    elif width is None:
        w, h = im.size
        width = int(w / h * height)
    elif height is None:
        w, h = im.size
        height = int(h / w * width)
    return width, height


def get_image(path, width=None, height=None):
    im = Image.open(path).convert('I')

    w, h = get_size(im, width, height)
    im = im.resize([w, h])
    arr = np.array(im, dtype=np.float)
    arr /= 255
    return arr


def main():
    arr = get_image('images/py.png', 20)
    print(arr)
    print(arr.shape)
    print(arr.mean())


if __name__ == '__main__':
    main()
