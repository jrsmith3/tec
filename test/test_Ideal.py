# coding: utf-8
import astropy.units
import pytest
import tec

from contextlib import nullcontext as does_not_raise


class TestIdealConstructorHappyPath():
    def test_params_without_default_values(self, valid_emitter, valid_collector):
        with does_not_raise():
            ideal_model = tec.models.Ideal(emitter=valid_emitter, collector=valid_collector)


# Pytest fixture definitions
# ==========================
@pytest.fixture
def valid_emitter():
    emitter = tec.electrode.Metal(temperature=2000, barrier=1.4)

    return emitter


@pytest.fixture
def valid_collector():
    collector = tec.electrode.Metal(temperature=300, barrier=0.8, position=10)

    return collector
