import asyncio
import sys
from time import time

import numpy as np

import shaders
from image import get_image
from shaders import Data


greyscale_max = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`\'. '
greyscale_mini = '@%#*+=-:.'
greyscale_rect = '█▓▒░'
greyscale_rect2 = '█▇▆▅▄▃▂▁'

greyscale = greyscale_mini


def map_char(i):
    i = max(0.0, min(0.999, i))
    c = greyscale[int((len(greyscale)) * i)]
    return f'{c} '


map_char = np.vectorize(map_char)


class Canvas:
    def __init__(self, h, w, shader, throttle=0.0):
        self.h = h
        self.w = w
        self.throttle = throttle

        self.drawn = 0

        self.shader = shader if type(shader) is list else [shader]
        self.buff = None
        self.init_buff = np.zeros([h, w], dtype=np.float)

    def set_texture(self, path):
        arr = get_image(path, height=self.h)
        self.h, self.w = arr.shape
        self.init_buff = arr

    def clear(self):
        for y in range(self.drawn):
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")
        self.drawn = 0
        self.buff = self.init_buff.copy()

    async def set_pixel(self, shader, texture, buffer, y, x, t):
        try:
            i = shader(Data(
                y=y,
                h=self.h,
                x=x,
                w=self.w,
                time=t,
                buff=texture
            ))
        except Exception:
            i = 1.0
        buffer[y, x] = i

    async def draw(self):
        self.clear()
        t = time()

        texture = self.init_buff
        for shader in self.shader:
            await asyncio.wait([
                self.set_pixel(
                    shader,
                    texture,
                    self.buff,
                    y, x, t
                )
                for y in range(self.h)
                for x in range(self.w)
            ])
            texture = self.buff.copy()
        buff = np.array(map_char(self.buff), dtype=np.object)
        print('\n'.join(buff.sum(axis=1)))
        self.drawn = self.h

    async def loop(self):
        while True:
            await asyncio.wait([
                self.draw(),
                asyncio.sleep(self.throttle)
            ])


def main():
    h, w = 40, 75
    # h, w = 20, 35

    canvas = Canvas(
        h, w,
        shader=[shaders.waves],
        throttle=0.,
    )
    canvas.set_texture('images/py.png')
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(canvas.loop())
        loop.close()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
