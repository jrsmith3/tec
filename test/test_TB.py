# -*- coding: utf-8 -*-
import numpy as np
from tec.electrode import Metal, TB
from astropy.units import Quantity
from astropy.units import Unit
import unittest
import copy

input_params = {"temp": 300.,
                "barrier": 2.0,
                "richardson": 10., 
                "thickness": 1., }

# Base classes
# ============
class Base(unittest.TestCase):
    """
    Base class for tests

    This class defines a common `setUp` method that defines attributes which are used in the various tests.
    """
    def setUp(self):
        """
        Create dict attribute that can instantiate a `Metal` object
        """
        self.input_params = copy.copy(input_params)
        self.el = TB(**input_params)


# Test classes
# ============
class Instantiation(Base):
    """
    Tests all aspects of instantiation

    Tests include: instantiation with non-numeric args, instantiation with input values outside constraints, etc.
    """
    pass


class Set(Base):
    """
    Tests all aspects of setting attributes

    Tests include: setting attributes with non-numeric data, setting attributes outside their constraints, etc.
    """
    pass


class MethodsInput(Base)
    """
    Tests methods which take input parameters

    Tests include: passing invalid input, etc.
    """
    pass


class MethodsReturnType(Base):
    """
    Tests methods' output types
    """
    pass


class MethodsReturnUnits(Base):
    """
    Tests methods' output units where applicable
    """
    pass


class MethodsReturnValues(Base):
    """
    Tests values of methods against known values
    """
    pass
