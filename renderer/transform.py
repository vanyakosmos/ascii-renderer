import numpy as np
from numba import jit


@jit
def rotation_mat_x(t):
    t = np.deg2rad(t)
    return np.array([
        [1, 0, 0, 0],
        [0, np.cos(t), -np.sin(t), 0],
        [0, np.sin(t), np.cos(t), 0],
        [0, 0, 0, 1],
    ], dtype=np.float)


@jit
def rotation_mat_y(t):
    t = np.deg2rad(t)
    return np.array([
        [np.cos(t), 0, np.sin(t), 0],
        [0, 1, 0, 0],
        [-np.sin(t), 0, np.cos(t), 0],
        [0, 0, 0, 1],
    ], dtype=np.float)


@jit
def rotation_mat_z(t):
    t = np.deg2rad(t)
    return np.array([
        [np.cos(t), -np.sin(t), 0, 0],
        [np.sin(t), np.cos(t), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ], dtype=np.float)


@jit
def rotation_mat(x=0., y=0., z=0.):
    return np.linalg.multi_dot([rotation_mat_z(z), rotation_mat_y(y), rotation_mat_x(x)])


@jit
def rotate(vs, x=0., y=0., z=0.):
    r = rotation_mat(x, y, z)
    vs = np.dot(vs, r)
    return vs


@jit
def trans_mat(x=0., y=0., z=0.):
    return np.array([
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1],
    ], dtype=np.float)


@jit
def scale_mat(x=1., y=1., z=1.):
    return np.array([
        [x, 0, 0, 1],
        [0, y, 0, 1],
        [0, 0, z, 1],
        [0, 0, 0, 1],
    ], dtype=np.float)
