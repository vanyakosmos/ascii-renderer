import asyncio
import sys
from math import cos, sin
from time import time
from typing import NamedTuple

import numpy as np


greyscale = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`\'. '
greyscale_mini = '@%#*+=-:. '


class Data(NamedTuple):
    x: float
    y: float
    time: float
    pix: float


def map_char(i):
    c = greyscale_mini[int((len(greyscale_mini) - 1) * i)]
    return f'{c} '


map_char = np.vectorize(map_char)


class Canvas:
    def __init__(self, h, w, shaders, throttle=0.0):
        self.h = h
        self.w = w
        self.throttle = throttle

        self.drawn = 0

        self.shaders = shaders if type(shaders) is list else [shaders]
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
        for shader in self.shaders:
            i = shader(Data(y=y / self.h, x=x / self.w, time=t, pix=i))
            i = max(0, min(1, i))  # clip
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


def waves(d: Data):
    return abs(cos(sin(d.time + 2 * d.x * d.pix) * 3 * d.y + d.time))


def eyes(d: Data):
    return 1 - (sin(d.time + d.x * 20) + cos(d.time + d.y * 20)) / 2


def main():
    h, w = 40, 75
    # h, w = 20, 35

    canvas = Canvas(
        h, w,
        shaders=[eyes, waves],
        throttle=0.05,
    )
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(canvas.loop())
        loop.close()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
