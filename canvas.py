import asyncio
import sys
from time import time

import numpy as np

import shaders
from image import get_image
from shaders import Data


greyscale_max = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`\'. '
greyscale_mini = '@%#*+=-:.'
greyscale_rect = '▓▒░=:.'
greyscale_rect2 = '█▇▆▅▄▃▂▁'

greyscale = greyscale_rect


def map_char(i):
    i = max(0.0, min(0.999, i))
    c = greyscale[int((len(greyscale)) * i)]
    return f'{c}{c}'


map_char = np.vectorize(map_char)


class Canvas:
    def __init__(self, h, w, shader, throttle=0.0):
        self.h = h
        self.w = w
        self.throttle = throttle

        self.drawn = 0

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
        for y in range(self.drawn):
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")
        self.drawn = 0

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

    async def apply_shaders(self):
        t = time()
        # texture is readonly inside shader
        texture = self.texture
        for shader in self.shaders:
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

    async def draw(self):
        self.clear()
        await self.apply_shaders()
        chars_mat = np.array(map_char(self.buff), dtype=np.object)
        print('\n'.join(chars_mat.sum(axis=1)))
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
