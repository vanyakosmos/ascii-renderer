import os
import sys
from time import sleep, time

import numpy as np

import shaders
from image import get_image
from shaders import Data
from utils import to_vec


# draw everything in separate buffer (slower but prettier)
ALT_SCREEN = True

# various greyscale palettes
greyscale_max = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`\'. '
greyscale_mini = '@%#*+=-:.'
greyscale_rect = '▓▒░=:.'
greyscale_rect2 = '█▇▆▅▄▃▂▁ '
GREYSCALE = greyscale_rect[::-1]


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


@to_vec(otypes=[np.object])
def map_char(i):
    i = max(0.0, min(0.999, i))
    c = GREYSCALE[int((len(GREYSCALE)) * i)]
    return c * 2


class Canvas:
    def __init__(self, h, w, shader, throttle=0.0):
        self.h = h
        self.w = w
        self.throttle = throttle
        self.counter = 0

        self.shaders = shader if type(shader) is list else [shader]
        self.buff = np.zeros([h, w], dtype=np.float)
        self.texture = np.ones([h, w], dtype=np.float)

    def set_texture(self, path, match_height=True):
        w, h = (-1, self.h) if match_height else (self.w, -1)
        arr = get_image(path, height=h, width=w)
        self.h, self.w = arr.shape
        self.texture = arr
        self.buff = np.zeros_like(arr)

    def clear(self):
        """
        > \033[K - clear line
        > \033[F - move cursor up
        """
        sys.stdout.write("\033[F" * self.h)

    def set_pixel(self, shader, texture, y, x, t):
        i = shader(Data(
            y=y,
            h=self.h,
            x=x,
            w=self.w,
            time=t,
            buff=texture
        ))
        self.buff[y, x] = i

    def set_pixel_one(self, args):
        self.set_pixel(*args)

    def apply_shaders(self):
        t = time()
        # texture is readonly inside shader
        texture = self.texture
        for shader in self.shaders:
            for y in range(self.h):
                for x in range(self.w):
                    self.set_pixel(
                        shader,
                        texture,
                        y, x, t
                    )
            texture = self.buff.copy()

    def draw_blank(self):
        for _ in range(self.h):
            print(' ' * self.w)

    def draw(self):
        self.apply_shaders()
        chars: np.ndarray = map_char(self.buff)
        self.clear()
        print('\n'.join(chars.sum(axis=1)))

    def loop(self):
        self.draw_blank()
        while True:
            self.draw()
            sleep(self.throttle)
            self.counter += 1


def main():
    h, w = 40, 75
    # h, w = 20, 35

    canvas = Canvas(
        h, w,
        shader=[shaders.waves],
        throttle=0.,
    )
    s = time()
    canvas.set_texture('images/eye.png')
    try:
        if ALT_SCREEN:
            print('\033[?1049h\033[H')
        canvas.loop()
    except KeyboardInterrupt:
        """
        fps stats for single 'waves' shader and eye.png with 40c height:
        - plain: 20-25
        - threads: 20-25
        - with numba's @jit: 85-95
        """
        if ALT_SCREEN:
            print('\033[?1049l')
        else:
            clear_screen()
        dif = time() - s
        print(f"{canvas.counter / dif:.2f}fps ({canvas.counter}f / {dif:.2f}s)")


if __name__ == '__main__':
    main()
