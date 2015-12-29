# -*- coding: utf-8 -*-
import numpy as np
from astropy import units
import unittest
from tec.electrode import Metal
from tec.models import Langmuir

em = Metal(temp=1000., barrier=2., richardson=10.)
co = Metal(temp=300., barrier=1., richardson=10., position=10.)


class Base(unittest.TestCase):
    """
    Base class for tests

    This class is intended to be subclassed so that I don't have to rewrite the same `setUp` method for each class containing tests.
    """
    def setUp(self):
        """
        Create new Langmuir object for every test
        """
        if em.position > co.position:
            raise ValueError("Initialization em.position > co.position.")

        self.t = Langmuir(em, co)

        self.em = em
        self.co = co


class MethodsInput(Base):
    """
    Tests methods which take input parameters

    Tests include: passing invalid input, etc.
    """
    def test_normalization_length_non_numeric(self):
        """
        normalization_length should raise TypeError with non-numeric, non astropy.units.Quantity input
        """
        current_density = "this string is non-numeric"
        self.assertRaises(TypeError, self.t.normalization_length, current_density)

    def test_normalization_length_negative_current_density(self):
        """
        normalization_length should raise ValueError with negative value of input
        """
        current_density = -1.
        self.assertRaises(ValueError, self.t.normalization_length, current_density)

    def test_normalization_length_zero_current_density(self):
        """
        normalization_length should raise ValueError with zero value of input
        """
        current_density = 0.
        self.assertRaises(ValueError, self.t.normalization_length, current_density)


class MethodsReturnType(Base):
    """
    Tests methods' output types
    """
    def test_back_current_density(self):
        """
        back_current_density should return astropy.units.Quantity
        """
        self.assertIsInstance(self.t.back_current_density(), units.Quantity)

    def test_normalization_length(self):
        """
        normalization_length should return astropy.units.Quantity
        """
        current_density = units.Quantity(1, "A cm-2")
        self.assertIsInstance(self.t.normalization_length(current_density), units.Quantity)


class MethodsReturnUnits(Base):
    """
    Tests methods' output units where applicable
    """
    def test_back_current_density(self):
        """
        back_current_density should return a value with unit A/cm2
        """
        self.assertEqual(self.t.back_current_density().unit, units.Unit("A/cm2"))

    def test_normalization_length(self):
        """
        normalization_length should return a value with unit um
        """
        current_density = units.Quantity(1, "A cm-2")
        self.assertEqual(self.t.normalization_length(current_density).unit, units.Unit("um"))


class MethodsReturnValues(Base):
    """
    Tests values of methods against known values
    """
    pass
