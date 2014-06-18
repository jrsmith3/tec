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
class ElectrodeAPITestBaseJustInputParams(unittest.TestCase):
    """
    Base class for API tests.

    This class defines a common setUp method that all the tests in this suite use.
    """

    def setUp(self):
        """
        Set up a dictionary that can properly instantiate an Electrode object.
        """
        self.input_params = copy.copy(input_params)


class ElectrodeAPITestBaseWithElectrode(unittest.TestCase):
    """
    Base class for API tests.

    This class defines a common setUp method that all the tests in this suite use.
    """

    def setUp(self):
        """
        Set up a dictionary that can properly instantiate an Electrode object.
        """
        self.El = Electrode(copy.copy(input_params))


# Test classes
# ============
class InstantiationInputNonDict(unittest.TestCase):
    """
    Tests instantiation when non-dict data is used.
    """

    def test_Electrode_no_input_arg(self):
        """Attempt to instantiate Electrode with no input argument."""
        self.assertRaises(TypeError, Electrode, None)

    def test_Electrode_non_dict_input_arg(self):
        """Attempt to instantiate Electrode with a non-dict input argument."""
        self.assertRaises(TypeError, Electrode, "this string is not a dict.")


class InstantiationInputIncomplete(ElectrodeAPITestBaseJustInputParams):
    """
    Tests instantiating when input dict is missing required data.
    """

    def test_Electrode_input_arg_sans_temp(self):
        """Instantiating argument missing temp."""
        del(self.input_params["temp"])
        self.assertRaises(KeyError, Electrode, self.input_params)

    def test_Electrode_input_arg_sans_barrier(self):
        """Instantiating argument missing barrier."""
        del(self.input_params["barrier"])
        self.assertRaises(KeyError, Electrode, self.input_params)

    def test_Electrode_input_arg_sans_richardson(self):
        """Instantiating argument missing richardson."""
        del(self.input_params["richardson"])
        self.assertRaises(KeyError, Electrode, self.input_params)


class InstantiationInputSuperfluousKeys(ElectrodeAPITestBaseJustInputParams):
    """
    Electrode can be instantiated with dict with superfluous keys.
    """

    def test_Electrode_input_superfluous_keys(self):
        """Instantiating argument with additional key."""
        self.input_params["superfluous"] = "value not even numeric!"
        try:
            El = Electrode(self.input_params)
        except:
            self.fail("Superfluous key in input param dict caused failure of instantiation.")


class InstantiationInputFieldsWrongType(ElectrodeAPITestBaseJustInputParams):
    """
    Tests instantiating when input dict has non-numeric data items.
    """

    def test_Electrode_input_temp_non_numeric(self):
        """Instantiating argument temp is non-numeric."""
        self.input_params["temp"] = "this string is non-numeric."

        try:
            El = Electrode(self.input_params)
        except TypeError:
            # Instantiating an Electrode with a dict with key `temp` having a non-numeric field raised a TypeError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`temp` field of instantiating dict must be numeric.")

    def test_Electrode_input_barrier_non_numeric(self):
        """Instantiating argument barrier is non-numeric."""
        self.input_params["barrier"] = "this string is non-numeric."
        try:
            El = Electrode(self.input_params)
        except TypeError:
            # Instantiating an Electrode with a dict with key `barrier` having a non-numeric field raised a TypeError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`barrier` field of instantiating dict must be numeric.")

    def test_Electrode_input_richardson_non_numeric(self):
        """Instantiating argument richardson is non-numeric."""
        self.input_params["richardson"] = "this string is non-numeric."
        try:
            El = Electrode(self.input_params)
        except TypeError:
            # Instantiating an Electrode with a dict with key `richardson` having a non-numeric field raised a TypeError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`richardson` field of instantiating dict must be numeric.")


class InstantiationInputOutsideConstraints(ElectrodeAPITestBaseJustInputParams):
    """
    Tests instantiating when input dict values are outside their constraints.

    See the Electrode class docstring for information about the constraints on
    the input data.
    """

    def test_Electrode_input_temp_less_than_zero(self):
        """Instantiating argument temp < 0."""
        self.input_params["temp"] = -1.1
        self.assertRaises(ValueError, Electrode, self.input_params)

    def test_Electrode_input_barrier_less_than_zero(self):
        """Instantiating argument barrier < 0."""
        self.input_params["barrier"] = -1.1
        self.assertRaises(ValueError, Electrode, self.input_params)

    def test_Electrode_input_richardson_less_than_zero(self):
        """Instantiating argument richardson < 0."""
        self.input_params["richardson"] = -1.1
        self.assertRaises(ValueError, Electrode, self.input_params)


class SetDataWrongType(ElectrodeAPITestBaseWithElectrode):
    """
    Tests setting attributes when input data is non-numeric.
    """

    def test_Electrode_set_temp_non_numeric(self):
        """Set argument temp non-numeric."""
        non_num = "this string is non-numeric."
        try:
            self.El.temp = non_num
        except TypeError:
            # Setting `temp` as a type that isn't numeric should raise a TypeError, so things are working.
            pass
        else:
            self.fail("`temp` attribute can be assigned a non-numeric value.")

    def test_Electrode_set_barrier_non_numeric(self):
        """Set argument barrier non-numeric."""
        non_num = "this string is non-numeric."
        try:
            self.El.barrier = non_num
        except TypeError:
            # Setting `barrier` as a type that isn't numeric should raise a TypeError, so things are working.
            pass
        else:
            self.fail("`barrier` attribute can be assigned a non-numeric value.")

    def test_Electrode_set_richardson_non_numeric(self):
        """Set argument richardson non-numeric."""
        non_num = "this string is non-numeric."
        try:
            self.El.richardson = non_num
        except TypeError:
            # Setting `richardson` as a type that isn't numeric should raise a TypeError, so things are working.
            pass
        else:
            self.fail("`richardson` attribute can be assigned a non-numeric value.")


class SetDataOutsideConstraints(ElectrodeAPITestBaseWithElectrode):
    """
    Tests setting attributes when input values are outside their constraints.

    See the Electrode class docstring for information about the constraints on
    the data.
    """

    def test_Electrode_set_temp_less_than_zero(self):
        """Set argument temp < 0."""
        try:
            self.El.temp = -1.1
        except ValueError:
            # Attempting to set the `temp` attribute with a negative value raised a ValueError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`temp` attribute can be assigned a negative value.")

    def test_Electrode_set_barrier_less_than_zero(self):
        """Set argument barrier < 0."""
        try:
            self.El.barrier = -1.1
        except ValueError:
            # Attempting to set the `barrier` attribute with a negative value raised a ValueError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`barrier` attribute can be assigned a negative value.")

    def test_Electrode_set_richardson_less_than_zero(self):
        """Set argument richardson < 0."""
        try:
            self.El.richardson = -1.1
        except ValueError:
            # Attempting to set the `richardson` attribute with a negative value raised a ValueError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`richardson` attribute can be assigned a negative value.")


class CalculatorsReturnTypeAndUnits(ElectrodeAPITestBaseWithElectrode):
    """
    Tests output types and units (where applicable) of the Electrode calculator methods.
    """
    # There is probably a much more elegant way to check units than I'm doing
    # below.

    def test_Electrode_calc_richardson_current_density_type(self):
        """
        calc_calc_richardson_current_density should return an astropy.units.Quantity.
        """
        self.assertIsInstance(
            self.El.calc_richardson_current_density(), Quantity)

    def test_Electrode_calc_calc_richardson_current_density_unit(self):
        """
        calc_calc_richardson_current_density should return a value with unit A/cm2.
        """
        self.assertEqual(
            self.El.calc_richardson_current_density().unit, Unit("A/cm2"))
