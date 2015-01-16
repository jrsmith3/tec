# -*- coding: utf-8 -*-
import numpy as np
from tec.electrode import Metal
from astropy.units import Quantity
from astropy.units import Unit
import unittest
import copy

input_params = {"temp": 300.,
                "barrier": 2.0,
                "richardson": 10., }


# Base classes
# ============
class TestBaseJustInputParams(unittest.TestCase):
    """
    Base class for tests

    This class defines a common `setUp` method that features an attribute which can be used to instantiate `Metal` objects.
    """
    def setUp(self):
        """
        Create dict attribute that can instantiate a `Metal` object
        """
        self.input_params = copy.copy(input_params)


class TestBaseWithMetal(unittest.TestCase):
    """
    Base class for tests

    This class defines a common setUp method that features an attribute which is a `Metal` object.
    """
    def setUp(self):
        """
        Set up a `Metal` object
        """
        self.El = Metal(**input_params)


# Test classes
# ============
class InstantiationInputArgsWrongType(TestBaseJustInputParams):
    """
    Test instantiation with non-numeric args
    """
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


class InstantiationInputOutsideConstraints(TestBaseJustInputParams):
    """
    Tests instantiating when input dict values are outside their constraints

    See the class docstring for information about the constraints on
    the input data.
    """
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


class SetAttribsWrongType(TestBaseWithMetal):
    """
    Tests setting attributes with non-numeric data
    """
    def test_temp_non_numeric(self):
        """
        Metal can only set `temp` with numeric value
        """
        non_num = "this string is non-numeric."
        try:
            self.El.temp = non_num
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
            self.El.barrier = non_num
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
            self.El.richardson = non_num
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
            self.El.voltage = non_num
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
            self.El.position = non_num
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
            self.El.emissivity = non_num
        except TypeError:
            # Setting `emissivity` as a type that isn't numeric should raise a TypeError, so things are working.
            pass
        else:
            self.fail("`emissivity` attribute can be assigned a non-numeric value.")


class SetAttribsOutsideConstraints(TestBaseWithMetal):
    """
    Tests setting attributes when input values are outside their constraints

    See the class docstring for information about the constraints on
    the data.
    """
    def test_temp_less_than_zero(self):
        """
        Metal must set `temp` > 0
        """
        try:
            self.El.temp = -1.1
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
            self.El.barrier = -1.1
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
            self.El.richardson = -1.1
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
            self.El.emissivity = -1.1
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
            self.El.emissivity = 1.1
        except ValueError:
            # Attempting to set the `emissivity` attribute with a negative value raised a ValueError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`emissivity` attribute can be assigned a negative value.")


class CalculatorsReturnType(TestBaseWithMetal):
    """
    Tests output types of the calculator methods
    """
    def test_motive(self):
        """
        Metal.motive should return an astropy.units.Quantity
        """
        self.assertIsInstance(self.El.motive(), Quantity)

    def test_thermoelectron_current_density(self):
        """
        Metal.thermoelectron_current_density should return an astropy.units.Quantity
        """
        self.assertIsInstance(self.El.thermoelectron_current_density(), Quantity)


class CalculatorsReturnUnits(TestBaseWithMetal):
    """
    Tests output units, where applicable, of the calculator methods
    """
    def test_motive(self):
        """
        Metal.motive should return a value with unit eV
        """
        self.assertEqual(self.El.motive().unit, Unit("eV"))

    def test_thermoelectron_current_density(self):
        """
        Metal.thermoelectron_current_density should return a value with unit A/cm2
        """
        self.assertEqual(self.El.thermoelectron_current_density().unit, Unit("A/cm2"))


class CalculatorsReturnValues(TestBaseWithMetal):
    """
    Tests values of calculator methods against known values
    """
    pass
