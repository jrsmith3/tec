#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Tests API of the TEC_Langmuir class.

These tests can be considered "logical testing" as described in the README. The definition of "logical testing" define the scope and purpose of these tests.

Please note that TEC objects (and their children) have attributes of type "Electrode." These tests do not test functionality of these Electrode attributes -- for example attempting to set illegal values for the temp of the Emitter attribute.
"""

__author__ = "Joshua Ryan Smith (joshua.r.smith@gmail.com)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2013 Joshua Ryan Smith"
__license__ = ""

from tec import TEC_Langmuir
from scipy import interpolate
import unittest

if __name__ == '__main__':
  unittest.main()
