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


class TestIdealConstructorParamsOutsideConstraints():
    def test_emitter_temperature_lt_collector_temperature(self, valid_emitter_args, valid_collector_args):
        invalid_emitter_args = valid_emitter_args.copy()
        invalid_emitter_args["temperature"] = 0.5 * valid_collector_args["temperature"]

        emitter = tec.electrode.Metal(**invalid_emitter_args)
        collector = tec.electrode.Metal(**valid_collector_args)

        with pytest.raises(ValueError):
            ideal_model = tec.models.Ideal(emitter=emitter, collector=collector)


    def test_emitter_temperature_eq_collector_temperature(self, valid_emitter_args, valid_collector_args):
        invalid_emitter_args = valid_emitter_args.copy()
        invalid_emitter_args["temperature"] = valid_collector_args["temperature"]

        emitter = tec.electrode.Metal(**invalid_emitter_args)
        collector = tec.electrode.Metal(**valid_collector_args)

        with pytest.raises(ValueError):
            ideal_model = tec.models.Ideal(emitter=emitter, collector=collector)


    def test_emitter_barrier_lt_collector_barrier(self, valid_emitter_args, valid_collector_args):
        invalid_emitter_args = valid_emitter_args.copy()
        invalid_emitter_args["barrier"] = 0.5 * valid_collector_args["barrier"]

        emitter = tec.electrode.Metal(**invalid_emitter_args)
        collector = tec.electrode.Metal(**valid_collector_args)

        with pytest.raises(ValueError):
            ideal_model = tec.models.Ideal(emitter=emitter, collector=collector)


    def test_emitter_barrier_eq_collector_barrier(self, valid_emitter_args, valid_collector_args):
        invalid_emitter_args = valid_emitter_args.copy()
        invalid_emitter_args["barrier"] = valid_collector_args["barrier"]

        emitter = tec.electrode.Metal(**invalid_emitter_args)
        collector = tec.electrode.Metal(**valid_collector_args)

        with pytest.raises(ValueError):
            ideal_model = tec.models.Ideal(emitter=emitter, collector=collector)


    def test_emitter_position_gt_collector_position(self, valid_emitter_args, valid_collector_args):
        invalid_emitter_args = valid_emitter_args.copy()
        invalid_emitter_args["position"] = 2 * valid_collector_args["position"]

        emitter = tec.electrode.Metal(**invalid_emitter_args)
        collector = tec.electrode.Metal(**valid_collector_args)

        with pytest.raises(ValueError):
            ideal_model = tec.models.Ideal(emitter=emitter, collector=collector)


    def test_emitter_position_eq_collector_position(self, valid_emitter_args, valid_collector_args):
        invalid_emitter_args = valid_emitter_args.copy()
        invalid_emitter_args["position"] = valid_collector_args["position"]

        emitter = tec.electrode.Metal(**invalid_emitter_args)
        collector = tec.electrode.Metal(**valid_collector_args)

        with pytest.raises(ValueError):
            ideal_model = tec.models.Ideal(emitter=emitter, collector=collector)


# There's only one test in the following test categories so I'm
# implementing them using functions instead of classes.
def test_Ideal_alt_constructor_from_args_returns_TEC(valid_emitter_args, valid_collector_args):
    args = dict({"emitter_" + key: val for key, val in valid_emitter_args.items()})
    args.update({"collector_" + key: val for key, val in valid_collector_args.items()})
    args.update({"back_emission": False})

    assert isinstance(tec.models.Ideal.from_args(**args), tec.TEC)


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
