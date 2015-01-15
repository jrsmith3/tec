# -*- coding: utf-8 -*-
from distutils.core import setup
import tec

setup(name = "tec",
      version = tec.__version__,
      author = "Joshua Ryan Smith",
      author_email = "joshua.r.smith@gmail.com",
      packages = ["tec",
                  "tec/electrode",
                  "physicalproperty"],
      url = "https://github.com/jrsmith3/tec",
      description = "Utils for simulating vacuum thermionic energy conversion devices",
      classifiers = ["Programming Language :: Python",
                     "License :: OSI Approved :: MIT License",
                     "Operating System :: OS Independent",
                     "Development Status :: 4 - Beta",
                     "Intended Audience :: Science/Research",
                     "Topic :: Scientific/Engineering :: Physics",
                     "Natural Language :: English",],
      install_requires = ["numpy",
                       	  "scipy",
                          "sympy",
                     	  "matplotlib",],
      license = "MIT",)