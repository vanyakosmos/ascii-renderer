from itertools import combinations
from time import time, sleep

import numpy as np
from numba import jit

from main import draw_blank, draw_buff


HEIGHT, WIDTH = 40, 40
canvas = np.zeros([HEIGHT, WIDTH], dtype=np.float)
colors = np.zeros([HEIGHT, WIDTH], dtype=np.float)
z_buff = np.zeros([HEIGHT, WIDTH], dtype=np.float)

model = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1],
], dtype=np.float)
vertices = np.array([
    (0, 0, 0),
    (1, 0, 0),
    (1, 1, 0),
    (0, 1, 0),
    (0, 1, 1),
    (1, 1, 1),
    (1, 0, 1),
    (0, 0, 1),
], dtype=np.float)
vertices = vertices * 2 - 1  # centralize vertices around (0,0,0)
triangles = [
    0, 2, 1,
    0, 3, 2,
    2, 3, 4,
    2, 4, 5,
    1, 2, 5,
    1, 5, 6,
    0, 7, 4,
    0, 4, 3,
    5, 4, 7,
    5, 7, 6,
    0, 6, 7,
    0, 1, 6,
]


@jit(nopython=True)
def set_pixel(arr, x, y, c=1.):
    if not 0 <= x <= 1 or not 0 <= y <= 1:
        return
    h, w = arr.shape
    h = int((h - 1) * y)
    w = int((w - 1) * x)
    arr[h, w] = c


def rotation_mat_x(t):
    t = np.deg2rad(t)
    return np.array([
        [1, 0, 0, 0],
        [0, np.cos(t), -np.sin(t), 0],
        [0, np.sin(t), np.cos(t), 0],
        [0, 0, 0, 1],
    ], dtype=np.float)


def rotation_mat_y(t):
    t = np.deg2rad(t)
    return np.array([
        [np.cos(t), 0, np.sin(t), 0],
        [0, 1, 0, 0],
        [-np.sin(t), 0, np.cos(t), 0],
        [0, 0, 0, 1],
    ], dtype=np.float)


def rotation_mat_z(t):
    t = np.deg2rad(t)
    return np.array([
        [np.cos(t), -np.sin(t), 0, 0],
        [np.sin(t), np.cos(t), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ], dtype=np.float)


def rotation_mat(x=0., y=0., z=0.):
    return np.linalg.multi_dot([rotation_mat_z(z), rotation_mat_y(y), rotation_mat_x(x)])


def trans_mat(x=0., y=0., z=0.):
    return np.array([
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1],
    ], dtype=np.float)


def scale_mat(x=1., y=1., z=1.):
    return np.array([
        [x, 0, 0, 1],
        [0, y, 0, 1],
        [0, 0, z, 1],
        [0, 0, 0, 1],
    ], dtype=np.float)


@jit(nopython=True)
def draw_line(arr, x1, y1, x2, y2, c=1):
    for t in np.arange(0, 1, 0.01):
        x = x1 * (1 - t) + x2 * t
        y = y1 * (1 - t) + y2 * t
        set_pixel(arr, x, y, c)


def draw_tri_mesh(screen, vs, tri):
    for i1, i2 in combinations(tri, 2):
        x1, y1 = vs[i1][:2]
        x2, y2 = vs[i2][:2]
        draw_line(screen, x1, y1, x2, y2)


def map_to_screen_coords(vs, s=2):
    vs = vs.copy()
    vs[:, :3] = (vs[:, :3] + s) / (s * 2)
    return vs


def main():
    vs = vertices.copy()
    ones = np.ones((vs.shape[0], 1), dtype=np.float)
    vs = np.concatenate((vs, ones), axis=1)

    r = rotation_mat(x=30, y=30)
    vs = np.dot(vs, r)

    draw_blank(canvas)
    spf = 1/60
    start = time()
    counter = 0
    try:
        while True:
            s = time()
            r = rotation_mat(x=1, y=.5)
            vs = np.dot(vs, r)
            screen_vs = map_to_screen_coords(vs)
            buff = canvas.copy()
            for i in range(0, len(triangles), 3):
                draw_tri_mesh(buff, screen_vs, triangles[i:i + 3])
            draw_buff(buff)
            # preserve fps
            d = time() - s
            if d < spf:
                sleep(spf - d)
            counter += 1
    except KeyboardInterrupt:
        print(counter / (time() - start))


if __name__ == '__main__':
    main()
