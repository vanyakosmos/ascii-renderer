import os
from time import time

import numpy as np

from renderer import shaders
from renderer.drawer import draw_blank, draw_buff
from renderer.image import get_image
from renderer.settings import ALT_SCREEN, HEIGHT, KEEP_STEADY_FPS, WIDTH
from renderer.utils import keep_steady_fps


SHADERS = (shaders.julia,)


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def set_pixel(texture, buff, shader, y, x, t):
    i = shader(
        y=y,
        x=x,
        time=t,
        buff=texture,
    )
    buff[y, x] = i


def apply_shaders(texture, buff):
    t = time()
    # texture is readonly inside shader
    texture_ = texture.copy()
    h, w = buff.shape
    for shader in SHADERS:
        for y in range(h):
            for x in range(w):
                set_pixel(texture_, buff, shader, y, x, t)
        texture_ = buff.copy()


def draw(texture, buff):
    apply_shaders(texture, buff)
    draw_buff(buff)


def loop(texture=None):
    if texture is None:
        texture = np.ones([HEIGHT, WIDTH], dtype=np.float)
    buff = np.zeros_like(texture, dtype=np.float)
    counter = 0
    if ALT_SCREEN:
        print('\033[?1049h\033[H')
    draw_blank(buff)
    try:
        while True:
            s = time()
            draw(texture, buff)
            if KEEP_STEADY_FPS:
                keep_steady_fps(s, 30)
            counter += 1
    except KeyboardInterrupt:
        pass
    if ALT_SCREEN:
        print('\033[?1049l')
    else:
        clear_screen()
    return counter


def show_fps_stats(start, loops_number):
    dif = time() - start
    print(f"{loops_number / dif:.2f}fps ({loops_number}f / {dif:.2f}s)")


def main():
    s = time()
    texture = get_image('images/py.png', height=HEIGHT)
    loops_number = loop(texture)
    show_fps_stats(s, loops_number)


if __name__ == '__main__':
    main()
