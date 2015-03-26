# -*- coding: utf-8 -*-
from setuptools import setup
execfile("tec/version.py")

setup(name="tec",
    version=__version__,
    author="Joshua Ryan Smith",
    author_email="joshua.r.smith@gmail.com",
    packages=["tec",
        "tec/electrode", ],
    url="https://github.com/jrsmith3/tec",
    license="MIT",
    description="Utils for simulating vacuum thermionic energy conversion devices",
    classifiers=["Programming Language :: Python",
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: OS Independent",
                 "Development Status :: 4 - Beta",
                 "Intended Audience :: Science/Research",
                 "Topic :: Scientific/Engineering :: Physics",
                 "Natural Language :: English", ],
    install_requires=["numpy",
        "scipy",
        "matplotlib",
        "astropy",
        "physicalproperty",
        "ibei"], )
