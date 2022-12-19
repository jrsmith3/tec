# coding: utf-8
import astropy.units
import pytest


collect_ignore = [
    "test_Langmuir.py",
    "test_SC.py",
    "test_TECBase.py",
]


# Common fixtures
# ===============
@pytest.fixture
def valid_metal_constructor_quantity_args():
    args = {
        "temperature": astropy.units.Quantity(300., astropy.units.K),
        "barrier": astropy.units.Quantity(0.8, astropy.units.eV),
        "richardson": astropy.units.Quantity(110., "A/(cm2 K2)"),
        "voltage": astropy.units.Quantity(0.1, astropy.units.V),
        "position": astropy.units.Quantity(10., astropy.units.um),
        "emissivity": astropy.units.Quantity(1., astropy.units.dimensionless_unscaled),
    }

    return args


@pytest.fixture(params=[(lambda x: x), (lambda x: x.value)])
def valid_metal_constructor_args(request, valid_metal_constructor_quantity_args):
    args = {key: request.param(val) for key, val in valid_metal_constructor_quantity_args.items()}

    return args
