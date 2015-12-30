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

    def test_critical_point_target_function_above_bound(self):
        """
        critical_point_target_function should raise ValueError if input is greater than the upper bound
        """
        current_density = 2 * self.t.emitter.thermoelectron_current_density()
        self.assertRaises(ValueError, self.t.critical_point_target_function, current_density)

    def test_critical_point_target_function_below_bound(self):
        """
        critical_point_target_function should raise ValueError if input is greater than the upper bound
        """
        current_density = -1.
        self.assertRaises(ValueError, self.t.critical_point_target_function, current_density)


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

    def test_saturation_point_voltage(self):
        """
        saturation_point_voltage should return astropy.units.Quantity
        """
        self.assertIsInstance(self.t.saturation_point_voltage(), units.Quantity)

    def test_saturation_point_current_density(self):
        """
        saturation_point_current_density should return astropy.units.Quantity
        """
        self.assertIsInstance(self.t.saturation_point_current_density(), units.Quantity)

    def test_critical_point_voltage(self):
        """
        critical_point_voltage should return astropy.units.Quantity
        """
        self.assertIsInstance(self.t.critical_point_voltage(), units.Quantity)

    def test_critical_point_current_density(self):
        """
        critical_point_current_density should return astropy.units.Quantity
        """
        self.assertIsInstance(self.t.critical_point_current_density(), units.Quantity)

    def test_critical_point_target_function(self):
        """
        critical_point_target_function should return float
        """
        current_density = 0.5 * self.t.emitter.thermoelectron_current_density()
        self.assertIsInstance(self.t.critical_point_target_function(current_density), float)

    def test_critical_point_voltage(self):
        """
        critical_point_voltage should return astropy.units.Quantity
        """
        self.assertIsInstance(self.t.critical_point_voltage(), units.Quantity)

    def test_output_voltage_target_function(self):
        """
        output_voltage_target_function should return float
        """
        current_density = self.t.emitter.thermoelectron_current_density()
        self.assertIsInstance(self.t.output_voltage_target_function(current_density), float)


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

    def test_saturation_point_voltage(self):
        """
        saturation_point_voltage should return a value with unit V
        """
        self.assertEqual(self.t.saturation_point_voltage().unit, units.Unit("V"))

    def test_critical_point_voltage(self):
        """
        critical_point_voltage should return a value with unit V
        """
        self.assertEqual(self.t.critical_point_voltage().unit, units.Unit("V"))


class MethodsReturnValues(Base):
    """
    Tests values of methods against known values
    """
    pass
