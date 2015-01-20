# -*- coding: utf-8 -*-
import numpy as np
from tec.electrode import Metal
from astropy import units
import unittest
import copy

input_params = {"temp": 300.,
                "barrier": 2.0,
                "richardson": 10., }


# Base classes
# ============
class Base(unittest.TestCase):
    """
    Base class for tests

    This class is intended to be subclassed so that the same `setUp` method does not have to be rewritten for each class containing tests.
    """
    def setUp(self):
        """
        Create dict attribute that can instantiate a `Metal` object
        """
        self.input_params = copy.copy(input_params)
        self.el = Metal(**input_params)


# Test classes
# ============
class Instantiation(Base):
    """
    Tests all aspects of instantiation

    Tests include: instantiation with args of wrong type, instantiation with input values outside constraints, etc.
    """
    # Input arguments wrong type
    # ==========================
    def test_temp_non_numeric(self):
        """
        Metal instantiation requires numeric `temp` value
        """
        self.input_params["temp"] = "this string is non-numeric."

        try:
            El = Metal(**self.input_params)
        except TypeError:
            # Attempting to instantiate a `tec.electrode.Metal` with a non-numeric `temp` argument raised a TypeError which is exactly what we wanted to do.
            pass
        else:
            self.fail("Shouldn't be able to instantiate with non-numeric `temp` argument.")

    def test_barrier_non_numeric(self):
        """
        Metal instantiation requires numeric `barrer` value
        """
        self.input_params["barrier"] = "this string is non-numeric."
        try:
            El = Metal(**self.input_params)
        except TypeError:
            # Attempting to instantiate a `tec.electrode.Metal` with a non-numeric `barrier` argument raised a TypeError which is exactly what we wanted to do.
            pass
        else:
            self.fail("Shouldn't be able to instantiate with non-numeric `barrier` argument.")

    def test_richardson_non_numeric(self):
        """
        Metal instantiation requires numeric `richardson` value
        """
        self.input_params["richardson"] = "this string is non-numeric."
        try:
            El = Metal(**self.input_params)
        except TypeError:
            # Attempting to instantiate a `tec.electrode.Metal` with a non-numeric `richardson` argument raised a TypeError which is exactly what we wanted to do.
            pass
        else:
            self.fail("Shouldn't be able to instantiate with non-numeric `richardson` argument.")

    def test_voltage_non_numeric(self):
        """
        Metal instantiation requires numeric `voltage` value
        """
        self.input_params["voltage"] = "this string is non-numeric."
        try:
            El = Metal(**self.input_params)
        except TypeError:
            # Attempting to instantiate a `tec.electrode.Metal` with a non-numeric `voltage` argument raised a TypeError which is exactly what we wanted to do.
            pass
        else:
            self.fail("Shouldn't be able to instantiate with non-numeric `voltage` argument.")

    def test_position_non_numeric(self):
        """
        Metal instantiation requires numeric `position` value
        """
        self.input_params["position"] = "this string is non-numeric."
        try:
            El = Metal(**self.input_params)
        except TypeError:
            # Attempting to instantiate a `tec.electrode.Metal` with a non-numeric `position` argument raised a TypeError which is exactly what we wanted to do.
            pass
        else:
            self.fail("Shouldn't be able to instantiate with non-numeric `position` argument.")

    def test_emissivity_non_numeric(self):
        """
        Metal instantiation requires numeric `emissivity` value
        """
        self.input_params["emissivity"] = "this string is non-numeric."
        try:
            El = Metal(**self.input_params)
        except TypeError:
            # Attempting to instantiate a `tec.electrode.Metal` with a non-numeric `emissivity` argument raised a TypeError which is exactly what we wanted to do.
            pass
        else:
            self.fail("Shouldn't be able to instantiate with non-numeric `emissivity` argument.")

    # Input arguments outside constraints
    # ===================================
    def test_temp_less_than_zero(self):
        """
        Metal instantiation requires `temp` > 0
        """
        self.input_params["temp"] = -1.1
        self.assertRaises(ValueError, Metal, **self.input_params)

    def test_barrier_less_than_zero(self):
        """
        Metal instantiation requires `barrier` > 0
        """
        self.input_params["barrier"] = -1.1
        self.assertRaises(ValueError, Metal, **self.input_params)

    def test_richardson_less_than_zero(self):
        """
        Metal instantiation requires `richardson` > 0
        """
        self.input_params["richardson"] = -1.1
        self.assertRaises(ValueError, Metal, **self.input_params)

    def test_emissivity_less_than_zero(self):
        """
        Metal instantiation requires `emissivity` > 0
        """
        self.input_params["emissivity"] = -1.1
        self.assertRaises(ValueError, Metal, **self.input_params)

    def test_emissivity_greater_than_one(self):
        """
        Metal instantiation requires `emissivity` < 1
        """
        self.input_params["emissivity"] = 1.1
        self.assertRaises(ValueError, Metal, **self.input_params)


class Set(Base):
    """
    Tests all aspects of setting attributes

    Tests include: setting attributes of wrong type, setting attributes outside their constraints, etc.
    """
    # Set attribute wrong type
    # ========================
    def test_temp_non_numeric(self):
        """
        Metal can only set `temp` with numeric value
        """
        non_num = "this string is non-numeric."
        try:
            self.el.temp = non_num
        except TypeError:
            # Setting `temp` as a type that isn't numeric should raise a TypeError, so things are working.
            pass
        else:
            self.fail("`temp` attribute can be assigned a non-numeric value.")

    def test_barrier_non_numeric(self):
        """
        Metal can only set `barrier` with numeric value
        """
        non_num = "this string is non-numeric."
        try:
            self.el.barrier = non_num
        except TypeError:
            # Setting `barrier` as a type that isn't numeric should raise a TypeError, so things are working.
            pass
        else:
            self.fail("`barrier` attribute can be assigned a non-numeric value.")

    def test_richardson_non_numeric(self):
        """
        Metal can only set `richardson` with numeric value
        """
        non_num = "this string is non-numeric."
        try:
            self.el.richardson = non_num
        except TypeError:
            # Setting `richardson` as a type that isn't numeric should raise a TypeError, so things are working.
            pass
        else:
            self.fail("`richardson` attribute can be assigned a non-numeric value.")

    def test_voltage_non_numeric(self):
        """
        Metal can only set `voltage` with numeric value
        """
        non_num = "this string is non-numeric."
        try:
            self.el.voltage = non_num
        except TypeError:
            # Setting `voltage` as a type that isn't numeric should raise a TypeError, so things are working.
            pass
        else:
            self.fail("`voltage` attribute can be assigned a non-numeric value.")

    def test_position_non_numeric(self):
        """
        Metal can only set `position` with numeric value
        """
        non_num = "this string is non-numeric."
        try:
            self.el.position = non_num
        except TypeError:
            # Setting `position` as a type that isn't numeric should raise a TypeError, so things are working.
            pass
        else:
            self.fail("`position` attribute can be assigned a non-numeric value.")

    def test_emissivity_non_numeric(self):
        """
        Metal can only set `emissivity` with numeric value
        """
        non_num = "this string is non-numeric."
        try:
            self.el.emissivity = non_num
        except TypeError:
            # Setting `emissivity` as a type that isn't numeric should raise a TypeError, so things are working.
            pass
        else:
            self.fail("`emissivity` attribute can be assigned a non-numeric value.")

    # Set attribute outside constraint
    # ================================
    def test_temp_less_than_zero(self):
        """
        Metal must set `temp` > 0
        """
        try:
            self.el.temp = -1.1
        except ValueError:
            # Attempting to set the `temp` attribute with a negative value raised a ValueError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`temp` attribute can be assigned a negative value.")

    def test_barrier_less_than_zero(self):
        """
        Metal must set `barrier` > 0
        """
        try:
            self.el.barrier = -1.1
        except ValueError:
            # Attempting to set the `barrier` attribute with a negative value raised a ValueError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`barrier` attribute can be assigned a negative value.")

    def test_richardson_less_than_zero(self):
        """
        Metal must set `richardson` > 0
        """
        try:
            self.el.richardson = -1.1
        except ValueError:
            # Attempting to set the `richardson` attribute with a negative value raised a ValueError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`richardson` attribute can be assigned a negative value.")

    def test_emissivity_less_than_zero(self):
        """
        Metal must set `emissivity` > 0
        """
        try:
            self.el.emissivity = -1.1
        except ValueError:
            # Attempting to set the `emissivity` attribute with a negative value raised a ValueError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`emissivity` attribute can be assigned a negative value.")

    def test_emissivity_greater_than_one(self):
        """
        Metal must set `emissivity` < 1
        """
        try:
            self.el.emissivity = 1.1
        except ValueError:
            # Attempting to set the `emissivity` attribute with a negative value raised a ValueError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`emissivity` attribute can be assigned a negative value.")


class MethodsReturnType(Base):
    """
    Tests methods' output types
    """
    def test_motive(self):
        """
        Metal.motive should return an astropy.units.Quantity
        """
        self.assertIsInstance(self.el.motive(), units.Quantity)

    def test_thermoelectron_current_density(self):
        """
        Metal.thermoelectron_current_density should return an astropy.units.Quantity
        """
        self.assertIsInstance(self.el.thermoelectron_current_density(), units.Quantity)


class MethodsReturnUnits(Base):
    """
    Tests methods' output units where applicable
    """
    def test_motive(self):
        """
        Metal.motive should return a value with unit eV
        """
        self.assertEqual(self.el.motive().unit, units.Unit("eV"))

    def test_thermoelectron_current_density(self):
        """
        Metal.thermoelectron_current_density should return a value with unit A/cm2
        """
        self.assertEqual(self.el.thermoelectron_current_density().unit, units.Unit("A/cm2"))


class MethodsReturnValues(Base):
    """
    Tests values of methods against known values
    """
    pass
