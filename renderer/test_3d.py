from time import time

import numpy as np
from numba import jit

from models import cube
from renderer.drawer import draw_blank, draw_buff
from renderer.settings import HEIGHT, KEEP_STEADY_FPS, WIDTH
from renderer.transform import rotate
from renderer.utils import keep_steady_fps


canvas = np.zeros([HEIGHT, WIDTH], dtype=np.float)
colors = np.zeros([HEIGHT, WIDTH], dtype=np.float)
z_buff = np.zeros([HEIGHT, WIDTH], dtype=np.float)


@jit(nopython=True)
def set_pixel(arr, x, y, c=1.):
    h, w = arr.shape
    if not 0 <= x < w or not 0 <= y < h:
        return
    arr[y, x] = c


@jit(nopython=True)
def draw_line(arr, v0, v1, c=1.):
    for t in np.arange(0, 1, 0.01):
        x1, y1 = v0[:2]
        x2, y2 = v1[:2]
        x = x1 * (1 - t) + x2 * t
        y = y1 * (1 - t) + y2 * t
        set_pixel(arr, int(x), int(y), c)


def draw_tri_mesh(screen, v0, v1, v2):
    draw_line(screen, v0, v1)
    draw_line(screen, v1, v2)
    draw_line(screen, v2, v0)


@jit
def draw_tri(screen, v0, v1, v2, c=1):
    vs = np.stack([v0, v1, v2])
    xmi = int(np.min(vs[:, 0]))
    xma = int(np.max(vs[:, 0]))
    ymi = int(np.min(vs[:, 1]))
    yma = int(np.max(vs[:, 1]))

    for x in range(xmi, xma + 1):
        for y in range(ymi, yma + 1):
            if inside_tri([x, y], v0, v1, v2):
                set_pixel(screen, x, y, c)


@jit
def inside_tri(p, v0, v1, v2):
    dx = p[0] - v0[0]
    dy = p[1] - v0[1]
    dx20 = v2[0] - v0[0]
    dy20 = v2[1] - v0[1]
    dx10 = v1[0] - v0[0]
    dy10 = v1[1] - v0[1]
    s_p = (dy20 * dx) - (dx20 * dy)
    t_p = (dx10 * dy) - (dy10 * dx)
    d = (dx10 * dy20) - (dy10 * dx20)
    if d > 0:
        return (s_p >= 0) and (t_p >= 0) and (s_p + t_p) <= d
    else:
        return (s_p <= 0) and (t_p <= 0) and (s_p + t_p) >= d


@jit(nopython=True)
def norm(v):
    return v / np.sqrt(np.sum(v ** 2))


def map_to_screen_coords(screen, vs, s=2):
    h, w = screen.shape
    vs = vs.copy()
    vs[:, 0] = (vs[:, 0] + s) / (s * 2) * h
    vs[:, 1] = (vs[:, 1] + s) / (s * 2) * w
    vs[:, 2] = (vs[:, 2] + s) / (s * 2) * h
    return vs


@jit
def tri_normal(v0, v1, v2):
    n = np.cross((v2 - v0)[:3], (v1 - v0)[:3])
    n = norm(n)
    return n


@jit
def luminance(v0, v1, v2, direction=None):
    if direction is None:
        direction = [0, 0, 1]
    n = tri_normal(v0, v1, v2)
    c = n.dot(direction)
    return c


def get_triangles(screen_vs):
    for i in range(0, len(cube.triangles), 3):
        v0 = screen_vs[cube.triangles[i]]
        v1 = screen_vs[cube.triangles[i + 1]]
        v2 = screen_vs[cube.triangles[i + 2]]
        yield v0, v1, v2


def main():
    vs = cube.vertices.copy()
    vs = vs * 2 - 1  # centralize vertices around (0,0,0)
    ones = np.ones((vs.shape[0], 1), dtype=np.float)
    vs = np.concatenate((vs, ones), axis=1)

    draw_blank(canvas)
    start = time()
    counter = 0
    try:
        while True:
            s = time()
            vs = rotate(vs, x=1, y=.5)
            screen_vs = map_to_screen_coords(canvas, vs)
            buff = canvas.copy()
            for v0, v1, v2 in get_triangles(screen_vs):
                c = luminance(v0, v1, v2)
                if c <= 0:
                    continue
                draw_tri(buff, v0, v1, v2, c=c)
            draw_buff(buff)
            if KEEP_STEADY_FPS:
                keep_steady_fps(s, 30)
            counter += 1
    except KeyboardInterrupt:
        print(counter / (time() - start))


if __name__ == '__main__':
    main()
