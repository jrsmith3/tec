# coding: utf-8
import astropy.units
import pytest
import tec

from contextlib import nullcontext as does_not_raise


def test_tec_constructor_happy_path(valid_ideal_model):
    with does_not_raise():
        device = tec.TEC(valid_ideal_model)


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
        ]
    )
def test_methods_regression(valid_ideal_model, method_under_test, expected_output):
    device = tec.TEC(valid_ideal_model)
    output = getattr(device, method_under_test)()

    assert astropy.units.allclose(expected_output, output)
