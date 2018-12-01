import os
import sys
from time import sleep, time

import numpy as np

import shaders
from shaders import Data
from utils import to_vec


# various greyscale palettes
greyscale_max = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`\'. '
greyscale_mini = '@%#*+=-:.'
greyscale_rect = '▓▒░=:.'
greyscale_rect2 = '█▇▆▅▄▃▂▁ '
GREYSCALE = greyscale_rect[::-1]

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


def jump_to_the_top():
    """
    > \033[K - clear line
    > \033[F - move cursor up
    """
    sys.stdout.write("\033[F" * HEIGHT)


@to_vec(otypes=[np.object])
def map_char(i):
    i = max(0.0, min(0.999, i))
    c = GREYSCALE[int((len(GREYSCALE)) * i)]
    return c * 2


def set_pixel(texture, buff, shader, y, x, t):
    i = shader(Data(
        y=y,
        h=HEIGHT,
        x=x,
        w=WIDTH,
        time=t,
        buff=texture
    ))
    buff[y, x] = i


def apply_shaders(texture, buff):
    t = time()
    # texture is readonly inside shader
    texture_ = texture.copy()
    for shader in SHADERS:
        for y in range(HEIGHT):
            for x in range(WIDTH):
                set_pixel(texture_, buff, shader, y, x, t)
        texture_ = buff.copy()


def draw_blank():
    for _ in range(HEIGHT):
        print(' ' * WIDTH)


def draw(texture, buff):
    apply_shaders(texture, buff)
    chars: np.ndarray = map_char(buff)
    jump_to_the_top()
    print('\n'.join(chars.sum(axis=1)))


def loop():
    buff = np.zeros([HEIGHT, WIDTH], dtype=np.float)
    texture = np.ones([HEIGHT, WIDTH], dtype=np.float)
    counter = 0
    draw_blank()
    try:
        while True:
            draw(texture, buff)
            sleep(THROTTLE)
            counter += 1
    except KeyboardInterrupt:
        pass
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
    # canvas.set_texture('images/eye.png')
    if ALT_SCREEN:
        print('\033[?1049h\033[H')
    loops_number = loop()
    if ALT_SCREEN:
        print('\033[?1049l')
    else:
        clear_screen()
    show_fps_stats(s, loops_number)


if __name__ == '__main__':
    main()
