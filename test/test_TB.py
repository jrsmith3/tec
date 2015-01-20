# -*- coding: utf-8 -*-
import numpy as np
from tec.electrode import Metal, TB
from astropy import units
import unittest
import copy

input_params = {"temp": 300.,
                "barrier": 2.0,
                "richardson": 10., 
                "thickness": 1., 
                "nea": 0.1, }

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

    # Input arguments wrong type
    # ==========================
    def test_thickness_non_numeric(self):
        """
        TB instantiation requires numeric `thickness` value
        """
        self.input_params["thickness"] = "this string is non-numeric."

        try:
            El = TB(**self.input_params)
        except TypeError:
            # Attempting to instantiate a `tec.electrode.TB` with a non-numeric `thickness` argument raised a TypeError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`thickness` field of instantiating dict must be numeric.")

    def test_nea_non_numeric(self):
        """
        TB instantiation requires numeric `nea` value
        """
        self.input_params["nea"] = "this string is non-numeric."

        try:
            El = TB(**self.input_params)
        except TypeError:
            # Attempting to instantiate a `tec.electrode.TB` with a non-numeric `nea` argument raised a TypeError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`nea` field of instantiating dict must be numeric.")

    # Input arguments outside constraints
    # ===================================
    def test_thickness_less_than_zero(self):
        """
        TB instantiation requires `thickness` > 0.
        """
        self.input_params["thickness"] = -1.1
        self.assertRaises(ValueError, TB, **self.input_params)

    def test_nea_less_than_zero(self):
        """
        TB instantiation requires `nea` > 0.
        """
        self.input_params["nea"] = -1.1
        self.assertRaises(ValueError, TB, **self.input_params)


class Set(Base):
    """
    Tests all aspects of setting attributes

    Tests include: setting attributes with non-numeric data, setting attributes outside their constraints, etc.
    """

    # Set attribute wrong type
    # ========================
    def test_thickness_non_numeric(self):
        """
        TB can only set `thickness` with numeric value.
        """
        non_num = "this string is non-numeric."
        try:
            self.el.thickness = non_num
        except TypeError:
            # Setting `thickness` as a type that isn't numeric should raise a TypeError, so things are working.
            pass
        else:
            self.fail("`thickness` attribute can be assigned a non-numeric value.")

    def test_nea_non_numeric(self):
        """
        TB can only set `nea` with numeric value.
        """
        non_num = "this string is non-numeric."
        try:
            self.el.nea = non_num
        except TypeError:
            # Setting `nea` as a type that isn't numeric should raise a TypeError, so things are working.
            pass
        else:
            self.fail("`nea` attribute can be assigned a non-numeric value.")

    # Set attribute outside constraint
    # ================================
    def test_thickness_less_than_zero(self):
        """
        TB must set `thickness` > 0.
        """
        try:
            self.el.thickness = -1.1
        except ValueError:
            # Attempting to set the `thickness` attribute with a negative value raised a ValueError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`thickness` attribute can be assigned a negative value.")

    def test_nea_less_than_zero(self):
        """
        TB must set `nea` > 0.
        """
        try:
            self.el.nea = -1.1
        except ValueError:
            # Attempting to set the `nea` attribute with a negative value raised a ValueError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`nea` attribute can be assigned a negative value.")


class MethodsInput(Base):
    """
    Tests methods which take input parameters

    Tests include: passing invalid input, etc.
    """
    def test_transmission_coeff_non_numeric_electron_energy(self):
        """
        electron_energy for transmission_coeff method must be numeric
        """
        non_num = "this string isn't numeric"
        self.assertRaises(TypeError, self.el.transmission_coeff, non_num)

    def test_transmission_coeff_negative_electron_energy(self):
        """
        electron_energy for transmission_coeff method must > 0
        """
        electron_energy = -0.1
        self.assertRaises(ValueError, self.el.transmission_coeff, electron_energy)

    def test_transmission_coeff_electron_energy_non_eV(self):
        """
        electron_energy for transmission_coeff method must have units compatible with eV
        """
        electron_energy = units.Quantity(0.1, "m")
        self.assertRaises(units.UnitsError, self.el.transmission_coeff, electron_energy)


class MethodsReturnType(Base):
    """
    Tests methods' output types
    """
    def test_transmission_coeff_type(self):
        """
        transmission_coeff should return a float
        """
        electron_energy = 0.1
        self.assertIsInstance(self.el.transmission_coeff(electron_energy), float)

    def test_motive_type(self):
        """
        motive should return a float
        """
        electron_energy = 0.1
        self.assertIsInstance(self.el.motive(), units.Quantity)


class MethodsReturnUnits(Base):
    """
    Tests methods' output units where applicable
    """
    def test_motive(self):
        """
        Metal.motive should return a value with unit eV
        """
        self.assertEqual(self.el.motive().unit, units.Unit("eV"))


class MethodsReturnValues(Base):
    """
    Tests values of methods against known values
    """
    pass
