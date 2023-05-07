# coding: utf-8
import astropy.units
import pytest
import tec

from contextlib import nullcontext as does_not_raise


def test_tec_constructor_happy_path(valid_ideal_model):
    with does_not_raise():
        device = tec.TEC(valid_ideal_model)


def test_model_arg_copied_on_instantiation(valid_ideal_model):
    """
    The `model` object passed to the constructor should be copied
    """
    device = tec.TEC(valid_ideal_model)

    assert device.model is not valid_ideal_model


@pytest.mark.parametrize("method_under_test,expected_output",
        [
            (
                "interelectrode_spacing",
                astropy.units.Quantity(10., astropy.units.um),
            ),
            (
                "output_voltage",
                astropy.units.Quantity(5., astropy.units.V),
            ),
            (
                "contact_potential",
                astropy.units.Quantity(1.2, astropy.units.V),
            ),
            (
                "forward_current_density",
                astropy.units.Quantity(1.16381647e-06, "A/cm2"),
            ),
            (
                "back_current_density",
                astropy.units.Quantity(3.92658733e-07, "A/cm2"),
            ),
            (
                "output_current_density",
                astropy.units.Quantity(7.71157739e-07, "A/cm2"),
            ),
            (
                "output_power_density",
                astropy.units.Quantity(3.8557887e-06, "W/cm2"),
            ),
            (
                "carnot_efficiency",
                astropy.units.Quantity(0.85, astropy.units.dimensionless_unscaled),
            ),
            (
                "efficiency",
                astropy.units.Quantity(4.25207974e-08, astropy.units.dimensionless_unscaled),
            ),
            (
                "heat_supply_rate",
                astropy.units.Quantity(90.68006553, astropy.units.W),
            ),
            (
                "electron_cooling_rate",
                astropy.units.Quantity(4.85357264e-06, astropy.units.W),
            ),
            (
                "thermal_radiation_rate",
                astropy.units.Quantity(90.68006067, astropy.units.W),
            ),
        ]
    )
def test_methods_regression(valid_ideal_model, method_under_test, expected_output):
    device = tec.TEC(valid_ideal_model)
    output = getattr(device, method_under_test)()

    assert astropy.units.allclose(expected_output, output)
