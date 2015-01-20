# -*- coding: utf-8 -*-
import numpy as np
from tec.electrode import Metal, TB
from tec.models import Simple_TB
from astropy import units
import unittest
import copy

em = Metal(temp=1000., barrier=2., richardson=10.)
co = TB(temp=300., barrier=1., richardson=10., thickness=1., nea=0.1, position=10.)

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
        if em.position > co.position:
            raise ValueError("Initialization em.position > co.position.")

        self.t = Simple_TB(em, co)

        self.em = em
        self.co = co


class Instantiation(Base):
    """
    Tests all aspects of instantiation

    Tests include: instantiation with non-numeric args, instantiation with input values outside constraints, etc.
    """
    def test_collector_non_TB(self):
        """
        collector not `tec.electrode.TB` -> Simple_TB init raises TypeError
        """
        self.assertRaises(TypeError, Simple_TB, self.em, self.em)


class Set(Base):
    """
    Tests all aspects of setting attributes

    Tests include: setting attributes with non-numeric data, setting attributes outside their constraints, etc.
    """
    pass


class MethodsInput(Base):
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
