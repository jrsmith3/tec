# -*- coding: utf-8 -*-
import numpy as np
from electrode import Electrode
from astropy.units import Quantity
from astropy.units import Unit
import unittest
import copy

input_params = {"temp": 300.,
                "barrier": 2.0,
                "richardson": 10.,}


# Base classes
# ============
class TestBaseJustInputParams(unittest.TestCase):
    """
    Base class for tests.

    This class defines a common setUp method that features an attribute which can be used to instantiate `Electrode` objects.
    """
    def setUp(self):
        """
        Set up a dictionary that can properly instantiate an `Electrode` object.
        """
        self.input_params = copy.copy(input_params)


class TestBaseWithElectrode(unittest.TestCase):
    """
    Base class for tests.

    This class defines a common setUp method that features an attribute which is an `Electrode` object.
    """
    def setUp(self):
        """
        Set up an `Electrode` object.
        """
        self.El = Electrode(copy.copy(input_params))


# Test classes
# ============
class InstantiationInputNonDict(unittest.TestCase):
    """
    Tests instantiation when non-dict data is used.
    """
    def test_no_input_arg(self):
        """
        Electrode instantiation without input argument is invalid.
        """
        self.assertRaises(TypeError, Electrode, None)

    def test_non_dict_input_arg(self):
        """
        Electrode instantiation with non-dict input argument is invalid.
        """
        self.assertRaises(TypeError, Electrode, "this string is not a dict.")


class InstantiationInputIncomplete(TestBaseJustInputParams):
    """
    Tests instantiating when input dict is missing required data.
    """
    def test_temp_missing(self):
        """
        Electrode instantiating dict requires `temp` key.
        """
        del(self.input_params["temp"])
        self.assertRaises(KeyError, Electrode, self.input_params)

    def test_barrier_missing(self):
        """
        Electrode instantiating dict requires `barrier` key.
        """
        del(self.input_params["barrier"])
        self.assertRaises(KeyError, Electrode, self.input_params)

    def test_richardson_missing(self):
        """
        Electrode instantiating dict requires `richardson` key.
        """
        del(self.input_params["richardson"])
        self.assertRaises(KeyError, Electrode, self.input_params)


class InstantiationInputSuperfluousKeys(TestBaseJustInputParams):
    """
    Tests instantiation with dict with superfluous keys.
    """
    def test_superfluous_keys(self):
        """
        Electrode can be instantiated with dict with superfluous keys.
        """
        self.input_params["superfluous"] = "value not even numeric!"
        try:
            El = Electrode(self.input_params)
        except:
            self.fail("Superfluous key in input param dict caused failure of instantiation.")


class InstantiationInputFieldsWrongType(TestBaseJustInputParams):
    """
    Tests instantiating when input dict has non-numeric data items.
    """
    def test_temp_non_numeric(self):
        """
        Electrode instantiation requires numeric `temp` value.
        """
        self.input_params["temp"] = "this string is non-numeric."

        try:
            El = Electrode(self.input_params)
        except TypeError:
            # Instantiating an Electrode with a dict with key `temp` having a non-numeric field raised a TypeError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`temp` field of instantiating dict must be numeric.")

    def test_barrier_non_numeric(self):
        """
        Electrode instantiation requires numeric `barrier` value.
        """
        self.input_params["barrier"] = "this string is non-numeric."
        try:
            El = Electrode(self.input_params)
        except TypeError:
            # Instantiating an Electrode with a dict with key `barrier` having a non-numeric field raised a TypeError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`barrier` field of instantiating dict must be numeric.")

    def test_richardson_non_numeric(self):
        """
        Electrode instantiation requires numeric `richardson` value.
        """
        self.input_params["richardson"] = "this string is non-numeric."
        try:
            El = Electrode(self.input_params)
        except TypeError:
            # Instantiating an Electrode with a dict with key `richardson` having a non-numeric field raised a TypeError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`richardson` field of instantiating dict must be numeric.")


class InstantiationInputOutsideConstraints(TestBaseJustInputParams):
    """
    Tests instantiating when input dict values are outside their constraints.

    See the class docstring for information about the constraints on
    the input data.
    """
    def test_temp_less_than_zero(self):
        """
        Electrode instantiation requires `temp` > 0.
        """
        self.input_params["temp"] = -1.1
        self.assertRaises(ValueError, Electrode, self.input_params)

    def test_barrier_less_than_zero(self):
        """
        Electrode instantiation requires `barrier` > 0.
        """
        self.input_params["barrier"] = -1.1
        self.assertRaises(ValueError, Electrode, self.input_params)

    def test_richardson_less_than_zero(self):
        """
        Electrode instantiation requires `richardson` > 0.
        """
        self.input_params["richardson"] = -1.1
        self.assertRaises(ValueError, Electrode, self.input_params)


class SetDataWrongType(TestBaseWithElectrode):
    """
    Tests setting attributes with non-numeric data.
    """
    def test_temp_non_numeric(self):
        """
        Electrode can only set `temp` with numeric value.
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
        Electrode can only set `barrier` with numeric value.
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
        Electrode can only set `richardson` with numeric value.
        """
        non_num = "this string is non-numeric."
        try:
            self.El.richardson = non_num
        except TypeError:
            # Setting `richardson` as a type that isn't numeric should raise a TypeError, so things are working.
            pass
        else:
            self.fail("`richardson` attribute can be assigned a non-numeric value.")


class SetDataOutsideConstraints(TestBaseWithElectrode):
    """
    Tests setting attributes when input values are outside their constraints.

    See the class docstring for information about the constraints on
    the data.
    """
    def test_temp_less_than_zero(self):
        """
        Electrode must set `temp` > 0.
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
        Electrode must set `barrier` > 0.
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
        Electrode must set `richardson` > 0.
        """
        try:
            self.El.richardson = -1.1
        except ValueError:
            # Attempting to set the `richardson` attribute with a negative value raised a ValueError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`richardson` attribute can be assigned a negative value.")


class CalculatorsReturnType(TestBaseWithElectrode):
    """
    Tests output types of the calculator methods.
    """
    def test_calc_richardson_current_density(self):
        """
        Electrode.calc_richardson_current_density should return an astropy.units.Quantity.
        """
        self.assertIsInstance(
            self.El.calc_richardson_current_density(), Quantity)

class CalculatorsReturnUnits(TestBaseWithElectrode):
    """
    Tests output units, where applicable, of the calculator methods.
    """
    def test_calc_richardson_current_density(self):
        """
        Electrode.calc_richardson_current_density should return a value with unit A/cm2.
        """
        self.assertEqual(
            self.El.calc_richardson_current_density().unit, Unit("A/cm2"))

class CalculatorsReturnValues(TestBaseWithElectrode):
    """
    Tests values of calculator methods against known values.
    """
    pass
