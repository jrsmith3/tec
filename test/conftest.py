# coding: utf-8
import astropy.units
import pytest
import tec


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


@pytest.fixture
def valid_emitter_args():
    args = {
        "temperature": 2000.,
        "barrier": 2.,
        "richardson": 120.,
        "voltage": 0.,
        "position": 0.,
        "emissivity": 1.,
    }

    return args


@pytest.fixture
def valid_collector_args():
    args = {
        "temperature": 300.,
        "barrier": 0.8,
        "richardson": 120.,
        "voltage": 0.,
        "position": 10.,
        "emissivity": 1.,
    }

    return args


@pytest.fixture
def valid_emitter(valid_emitter_args):
    emitter = tec.electrode.Metal(**valid_emitter_args)

    return emitter


@pytest.fixture
def valid_collector(valid_collector_args):
    collector = tec.electrode.Metal(**valid_collector_args)

    return collector


@pytest.fixture
def valid_ideal_model(valid_emitter, valid_collector):
    ideal_model = tec.models.Ideal(emitter=valid_emitter, collector=valid_collector)

    return ideal_model
