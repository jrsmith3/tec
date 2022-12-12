# coding: utf-8
import astropy.units
import pytest
import tec

from contextlib import nullcontext as does_not_raise


class TestMetalConstructorHappyPath():
    def test_params_without_default_values(self, valid_constructor_args):
        valid_constructor_args.pop("voltage")
        valid_constructor_args.pop("position")
        valid_constructor_args.pop("emissivity")

        with does_not_raise():
            emitter = tec.electrode.Metal(**valid_constructor_args)


    def test_params_with_default_values(self, valid_constructor_args):
        with does_not_raise():
            emitter = tec.electrode.Metal(**valid_constructor_args)


    @pytest.mark.parametrize("argname", [
            "voltage",
            "position",
            ]
        )
    def test_params_that_can_equal_zero(self, valid_constructor_args, argname):
        valid_constructor_args[argname] = 0

        with does_not_raise():
            emitter = tec.electrode.Metal(**valid_constructor_args)


    @pytest.mark.parametrize("argname,val", [
            ("temperature", astropy.units.Quantity(26.85, astropy.units.deg_C)),
            ("barrier", astropy.units.Quantity(3.20435313e-19, astropy.units.J)),
            ("richardson", astropy.units.Quantity(10_000., "mA/(cm2 K2)")),
            ("voltage", astropy.units.Quantity(100., astropy.units.mV)),
            ("position", astropy.units.Quantity(1e-7, astropy.units.m)),
            ]
        )
    def test_quantity_params_compatible_units(self, valid_constructor_quantity_args, argname, val):
        valid_constructor_quantity_args[argname] = val

        with does_not_raise():
            emitter = tec.electrode.Metal(**valid_constructor_quantity_args)


class TestMetalConstructorParamsOutsideConstraints():
    @pytest.mark.parametrize("argname", [
            "temperature",
            "barrier",
            "richardson",
            "emissivity",
            ]
        )
    def test_param_eq_0(self, valid_constructor_args, argname):
        invalid_constructor_args = valid_constructor_args.copy()
        invalid_constructor_args[argname] = 0 * valid_constructor_args[argname]

        with pytest.raises(ValueError):
            emitter = tec.electrode.Metal(**invalid_constructor_args)


    @pytest.mark.parametrize("argname", [
            "temperature",
            "barrier",
            "richardson",
            "emissivity",
            ]
        )
    def test_param_lt_0(self, valid_constructor_args, argname):
        invalid_constructor_args = valid_constructor_args.copy()
        invalid_constructor_args[argname] = -1 * valid_constructor_args[argname]

        with pytest.raises(ValueError):
            emitter = tec.electrode.Metal(**invalid_constructor_args)


    @pytest.mark.parametrize("argname", [
            "emissivity",
            ]
        )
    def test_param_gt_1(self, valid_constructor_args, argname):
        invalid_constructor_args = valid_constructor_args.copy()

        if isinstance(valid_constructor_args[argname], astropy.units.Quantity):
            invalid_constructor_args[argname] = 1.1 * valid_constructor_args[argname].unit
        else:
            invalid_constructor_args[argname] = 1.1 * valid_constructor_args[argname]

        with pytest.raises(ValueError):
            emitter = tec.electrode.Metal(**invalid_constructor_args)


# Pytest fixture definitions
# ==========================
@pytest.fixture
def valid_constructor_quantity_args():
    args = {
        "temperature": astropy.units.Quantity(300., astropy.units.K),
        "barrier": astropy.units.Quantity(2., astropy.units.eV),
        "richardson": astropy.units.Quantity(10., "A/(cm2 K2)"),
        "voltage": astropy.units.Quantity(0.1, astropy.units.V),
        "position": astropy.units.Quantity(0.1, astropy.units.um),
        "emissivity": astropy.units.Quantity(1., astropy.units.dimensionless_unscaled),
    }

    return args


@pytest.fixture(params=[(lambda x: x), (lambda x: x.value)])
def valid_constructor_args(request, valid_constructor_quantity_args):
    args = {key: request.param(val) for key, val in valid_constructor_quantity_args.items()}

    return args







# =========================================
# `unittest` stuff below; delete eventually
# =========================================
import copy
import unittest

input_params = {"temp": 300.,
                "barrier": 2.0,
                "richardson": 10., }

# Base classes
# ============
@pytest.mark.skip("These tests are being deprecated")
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
@pytest.mark.skip("These tests are being deprecated")
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
