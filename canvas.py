import asyncio
import sys
from time import time

import numpy as np

import shaders
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
        self.buff = np.zeros([h, w], dtype=np.float)

    @classmethod
    def from_image(cls):
        # todo
        pass

    def clear(self):
        for y in range(self.drawn):
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")
        self.drawn = 0

    async def set_pixel(self, y, x, t):
        i = self.buff[y, x]
        for shader in self.shader:
            i = shader(Data(y=y / self.h, x=x / self.w, time=t, pix=i))
        self.buff[y, x] = i

    async def draw(self):
        self.clear()
        t = time()
        await asyncio.wait([
            self.set_pixel(y, x, t)
            for y in range(self.h)
            for x in range(self.w)
        ])
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
    # h, w = 40, 75
    h, w = 20, 35

    canvas = Canvas(
        h, w,
        shader=[shaders.waves(False)],
        throttle=0.,
    )
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(canvas.loop())
        loop.close()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
