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


# There's only one test in the following test categories so I'm
# implementing them using functions instead of classes.
@pytest.mark.parametrize("argname,val", [
        ("temperature", astropy.units.s),
        ("barrier", astropy.units.s),
        ("richardson", astropy.units.s),
        ("voltage", astropy.units.s),
        ("position", astropy.units.s),
        ("emissivity", astropy.units.m),
        ]
    )
def test_metal_constructor_params_incompatible_units(valid_constructor_quantity_args, argname, val):
    valid_constructor_arg_value = valid_constructor_quantity_args[argname].value

    invalid_constructor_args = valid_constructor_quantity_args.copy()
    invalid_constructor_args[argname] = astropy.units.Quantity(valid_constructor_arg_value, val)

    with pytest.raises(astropy.units.core.UnitConversionError):
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
