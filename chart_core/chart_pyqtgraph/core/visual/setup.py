#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : setup.py
@Author  : Link
@Time    : 2022/8/25 22:46
@Mark    : 
"""

from distutils.core import setup, Extension

from Cython.Build import cythonize
import numpy

setup(ext_modules=cythonize(
    Extension(
        "visual",
        sources=["visual.pyx"],
        language='c',
        include_dirs=[numpy.get_include()],

    )
    , language_level=3))
