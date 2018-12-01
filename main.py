import os
import sys
from time import sleep, time

import numpy as np

import shaders
from utils import to_vec


# various greyscale palettes
greyscale_max = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`\'. '
greyscale_mini = '@%#*+=-:.'
greyscale_rect = '▓▒░=:.'
greyscale_rect2 = '█▇▆▅▄▃▂▁ '
GS = greyscale_rect[::-1]

# canvas size
HEIGHT = 30
WIDTH = 45

# draw everything in separate buffer (slower but prettier)
ALT_SCREEN = False

# misc
THROTTLE = 0.
SHADERS = (shaders.waves,)


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def jump_to_the_top(buff):
    """
    > \033[K - clear line
    > \033[F - move cursor up
    """
    sys.stdout.write("\033[F" * buff.shape[0])


@to_vec(otypes=[np.object])
def map_char(i):
    i = max(0.0, min(1.0, i))
    c = GS[int((len(GS) - 1) * i)]
    return c * 2


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


def draw_blank(buff):
    h, w = buff.shape
    for _ in range(h):
        print(' ' * w)


def draw_buff(buff):
    chars: np.ndarray = map_char(buff.copy())
    jump_to_the_top(buff)
    print('\n'.join(chars.sum(axis=1)))


def draw(texture, buff):
    apply_shaders(texture, buff)
    draw_buff(buff)


def loop(height, width):
    buff = np.zeros([height, width], dtype=np.float)
    texture = np.ones([height, width], dtype=np.float)
    counter = 0
    if ALT_SCREEN:
        print('\033[?1049h\033[H')
    draw_blank(buff)
    try:
        while True:
            draw(texture, buff)
            sleep(THROTTLE)
            counter += 1
    except KeyboardInterrupt:
        pass
    if ALT_SCREEN:
        print('\033[?1049l')
    else:
        clear_screen()
    return counter


def show_fps_stats(start, loops_number):
    """
    fps stats for single 'waves' shader and eye.png with 40c height:
    - plain: 20-25
    - threads: 20-25
    - with numba's @jit: 85-95
    """
    dif = time() - start
    print(f"{loops_number / dif:.2f}fps ({loops_number}f / {dif:.2f}s)")


def main():
    s = time()
    loops_number = loop(HEIGHT, WIDTH)
    show_fps_stats(s, loops_number)


if __name__ == '__main__':
    main()
