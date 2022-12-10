# coding: utf-8
import astropy.units
import copy
from tec.electrode import Metal
import unittest

input_params = {"temp": 300.,
                "barrier": 2.0,
                "richardson": 10., }


# Base classes
# ============
class Base(unittest.TestCase):
    """
    Base class for tests

    This class is intended to be subclassed so that the same `setUp`
    method does not have to be rewritten for each class containing
    tests.
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

    Tests include: instantiation with args of wrong type,
    instantiation with input values outside constraints, etc.
    """
    # Instantiation via `__init__`
    # ============================
    # Input arguments wrong type
    # --------------------------
    def test_temp_non_numeric(self):
        """
        Metal instantiation requires numeric `temp` value
        """
        self.input_params["temp"] = "this string is non-numeric."

        try:
            El = Metal(**self.input_params)
        except TypeError:
            # Attempting to instantiate a `tec.electrode.Metal` with a
            # non-numeric `temp` argument raised a TypeError which is
            # exactly what we wanted to do.
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
            # Attempting to instantiate a `tec.electrode.Metal` with a
            # non-numeric `barrier` argument raised a TypeError which
            # is exactly what we wanted to do.
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
            # Attempting to instantiate a `tec.electrode.Metal` with a
            # non-numeric `richardson` argument raised a TypeError
            # which is exactly what we wanted to do.
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
            # Attempting to instantiate a `tec.electrode.Metal` with a
            # non-numeric `voltage` argument raised a TypeError which
            # is exactly what we wanted to do.
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
            # Attempting to instantiate a `tec.electrode.Metal` with a
            # non-numeric `position` argument raised a TypeError
            # which is exactly what we wanted to do.
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
            # Attempting to instantiate a `tec.electrode.Metal` with a
            # non-numeric `emissivity` argument raised a TypeError
            # which is exactly what we wanted to do.
            pass
        else:
            self.fail("Shouldn't be able to instantiate with non-numeric `emissivity` argument.")

    # Input arguments outside constraints
    # -----------------------------------
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

    # Other instantiation conditions
    # ------------------------------
    def test_additional_arbitrary_args(self):
        """
        Metal can be instantiated with additional arbitrary args
        """
        self.input_params["not_an_argument"] = "not_an_argument"
        try:
            el = Metal(**self.input_params)
        except TypeError:
            self.fail("Instantiation failed with additional arbitrary args")

    # Instantiation via `from_dict`
    # ============================
    # Input arguments wrong type
    # --------------------------
    def test_from_dict_temp_non_numeric(self):
        """
        Metal.from_dict instantiation requires numeric `temp` value
        """
        self.input_params["temp"] = "this string is non-numeric."

        try:
            El = Metal.from_dict(self.input_params)
        except TypeError:
            # Attempting to instantiate a `tec.electrode.Metal` with a
            # non-numeric `temp` argument raised a TypeError which is
            # exactly what we wanted to do.
            pass
        else:
            self.fail("Shouldn't be able to instantiate with non-numeric `temp` argument.")

    def test_from_dict_barrier_non_numeric(self):
        """
        Metal.from_dict instantiation requires numeric `barrer` value
        """
        self.input_params["barrier"] = "this string is non-numeric."
        try:
            El = Metal.from_dict(self.input_params)
        except TypeError:
            # Attempting to instantiate a `tec.electrode.Metal` with a
            # non-numeric `barrier` argument raised a TypeError which
            # is exactly what we wanted to do.
            pass
        else:
            self.fail("Shouldn't be able to instantiate with non-numeric `barrier` argument.")

    def test_from_dict_richardson_non_numeric(self):
        """
        Metal.from_dict instantiation requires numeric `richardson` value
        """
        self.input_params["richardson"] = "this string is non-numeric."
        try:
            El = Metal.from_dict(self.input_params)
        except TypeError:
            # Attempting to instantiate a `tec.electrode.Metal` with a
            # non-numeric `richardson` argument raised a TypeError
            # which is exactly what we wanted to do.
            pass
        else:
            self.fail("Shouldn't be able to instantiate with non-numeric `richardson` argument.")

    def test_from_dict_voltage_non_numeric(self):
        """
        Metal.from_dict instantiation requires numeric `voltage` value
        """
        self.input_params["voltage"] = "this string is non-numeric."
        try:
            El = Metal.from_dict(self.input_params)
        except TypeError:
            # Attempting to instantiate a `tec.electrode.Metal` with a
            # non-numeric `voltage` argument raised a TypeError which
            # is exactly what we wanted to do.
            pass
        else:
            self.fail("Shouldn't be able to instantiate with non-numeric `voltage` argument.")

    def test_from_dict_position_non_numeric(self):
        """
        Metal.from_dict instantiation requires numeric `position` value
        """
        self.input_params["position"] = "this string is non-numeric."
        try:
            El = Metal.from_dict(self.input_params)
        except TypeError:
            # Attempting to instantiate a `tec.electrode.Metal` with a
            # non-numeric `position` argument raised a TypeError
            # which is exactly what we wanted to do.
            pass
        else:
            self.fail("Shouldn't be able to instantiate with non-numeric `position` argument.")

    def test_from_dict_emissivity_non_numeric(self):
        """
        Metal.from_dict instantiation requires numeric `emissivity` value
        """
        self.input_params["emissivity"] = "this string is non-numeric."
        try:
            El = Metal.from_dict(self.input_params)
        except TypeError:
            # Attempting to instantiate a `tec.electrode.Metal` with a
            # non-numeric `emissivity` argument raised a TypeError
            # which is exactly what we wanted to do.
            pass
        else:
            self.fail("Shouldn't be able to instantiate with non-numeric `emissivity` argument.")

    # Input arguments outside constraints
    # -----------------------------------
    def test_from_dict_temp_less_than_zero(self):
        """
        Metal.from_dict instantiation requires `temp` > 0
        """
        self.input_params["temp"] = -1.1
        self.assertRaises(ValueError, Metal.from_dict, self.input_params)

    def test_from_dict_barrier_less_than_zero(self):
        """
        Metal.from_dict instantiation requires `barrier` > 0
        """
        self.input_params["barrier"] = -1.1
        self.assertRaises(ValueError, Metal.from_dict, self.input_params)

    def test_from_dict_richardson_less_than_zero(self):
        """
        Metal.from_dict instantiation requires `richardson` > 0
        """
        self.input_params["richardson"] = -1.1
        self.assertRaises(ValueError, Metal.from_dict, self.input_params)

    def test_from_dict_emissivity_less_than_zero(self):
        """
        Metal.from_dict instantiation requires `emissivity` > 0
        """
        self.input_params["emissivity"] = -1.1
        self.assertRaises(ValueError, Metal.from_dict, self.input_params)

    def test_from_dict_emissivity_greater_than_one(self):
        """
        Metal.from_dict instantiation requires `emissivity` < 1
        """
        self.input_params["emissivity"] = 1.1
        self.assertRaises(ValueError, Metal.from_dict, self.input_params)

    # Input argument missing required key
    # -----------------------------------
    def test_from_dict_missing_key_temp(self):
        """
        Metal.from_dict instantiation requires "temp" key
        """
        del self.input_params["temp"]
        self.assertRaises(TypeError, Metal, self.input_params)

    def test_from_dict_missing_key_barrier(self):
        """
        Metal.from_dict instantiation requires "barrier" key
        """
        del self.input_params["barrier"]
        self.assertRaises(TypeError, Metal, self.input_params)

    # Other instantiation conditions
    # ------------------------------
    def test_from_dict_additional_arbitrary_keys(self):
        """
        Metal.from_dict can be instantiated with additional arbitrary keys
        """
        self.input_params["not_an_argument"] = "not_an_argument"
        try:
            el = Metal.from_dict(self.input_params)
        except TypeError:
            self.fail("Instantiation failed with additional arbitrary args")
