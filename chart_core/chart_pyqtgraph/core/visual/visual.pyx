#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : visual.pyx
@Author  : Link
@Time    : 2022/8/25 19:05
@Mark    : 
"""

cimport numpy as np
cimport cython

def add(a, b):
    cdef double x = 1.1
    cdef char y = 3

    return x + b + x

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef coord_to_np(np.ndarray[np.int16_t, ndim=1] x, np.ndarray[np.int16_t, ndim=1] y,
                 np.ndarray[np.float32_t, ndim=1] d, np.ndarray[np.float64_t, ndim=2] c):
    cdef int l
    l = x.shape[0]
    for i in range(l):
        c[x[i], y[i]] = d[i]
