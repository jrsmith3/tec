# coding: utf-8
import astropy.units
import pytest
import tec

from contextlib import nullcontext as does_not_raise


class TestIdealConstructorHappyPath():
    def test_params_without_default_values(self, valid_emitter, valid_collector):
        with does_not_raise():
            ideal_model = tec.models.Ideal(emitter=valid_emitter, collector=valid_collector)


    def test_params_with_default_values(self, valid_emitter, valid_collector):
        with does_not_raise():
            ideal_model = tec.models.Ideal(emitter=valid_emitter, collector=valid_collector, back_emission=False)


# Pytest fixture definitions
# ==========================
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
