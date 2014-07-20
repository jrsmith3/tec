# -*- coding: utf-8 -*-
from distutils.core import setup

setup(name = "electrode",
      version = "1.1.0",
      author = "Joshua Ryan Smith",
      author_email = "joshua.r.smith@gmail.com",
      packages = ["electrode"],
      url = "https://github.com/jrsmith3/electrode",
      description = "Simulator of thermoelectron emission from an electrode.",
      classifiers = ["Programming Language :: Python",
                     "License :: OSI Approved :: MIT License",
                     "Operating System :: OS Independent",
                     "Development Status :: 4 - Beta",
                     "Intended Audience :: Science/Research",
                     "Topic :: Scientific/Engineering :: Physics",
                     "Natural Language :: English",],
      install_requires = ["numpy",
                          "scipy",
                          "astropy"],)
