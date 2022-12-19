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


class TestIdealfrom_argsCases():
    def test_returns_TEC(self, valid_emitter_args, valid_collector_args):
        args = dict({"emitter_" + key: val for key, val in valid_emitter_args.items()})
        args.update({"collector_" + key: val for key, val in valid_collector_args.items()})
        args.update({"back_emission": False})

        assert isinstance(tec.models.Ideal.from_args(**args), tec.TEC)


    def test_TEC_back_current_density_zero_back_emission_false(self, valid_emitter_args, valid_collector_args):
        args = dict({"emitter_" + key: val for key, val in valid_emitter_args.items()})
        args.update({"collector_" + key: val for key, val in valid_collector_args.items()})
        args.update({"back_emission": False})

        device = tec.models.Ideal.from_args(**args)

        assert device.back_emission is False
        assert device.back_current_density() == 0


    def test_TEC_back_current_density_nonzero_back_emission_true(self, valid_emitter_args, valid_collector_args):
        args = dict({"emitter_" + key: val for key, val in valid_emitter_args.items()})
        args.update({"collector_" + key: val for key, val in valid_collector_args.items()})
        args.update({"back_emission": True})

        device = tec.models.Ideal.from_args(**args)

        assert device.back_emission is True
        assert device.back_current_density() > 0
