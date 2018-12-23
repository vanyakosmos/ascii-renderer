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
    im = Image.open(path).convert('RGBA')
    bg = Image.new('RGBA', im.size, (255, 255, 255, 255))
    bg.paste(im, mask=im)
    im = bg.convert('I')
    w, h = get_size(im, width, height)
    im = im.resize([w, h])
    arr = np.array(im, dtype=np.float)
    arr /= 255
    return arr


def main():
    get_image('images/py.png')


if __name__ == '__main__':
    main()
