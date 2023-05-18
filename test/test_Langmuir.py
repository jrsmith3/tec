# coding: utf-8
import astropy.units
import pytest
import tec

from contextlib import nullcontext as does_not_raise


class TestLangmuirConstructorHappyPath():
    def test_params_without_default_values(self, valid_emitter, valid_collector):
        with does_not_raise():
            langmuir_model = tec.models.Langmuir(emitter=valid_emitter, collector=valid_collector)


@pytest.mark.skip(reason="Test needs to be generalized.")
def test_electrode_args_copied_on_instantiation(valid_emitter, valid_collector):
    """
    The `emitter` and `collector` objects passed to the constructor should be copied

    I am not implementing this test because it would be a copy of the
    test with the same name in `test/test_Ideal.py`. I need to figure
    out how to generalize it.
    """
    raise


@pytest.mark.skip(reason="Tests need to be generalized.")
class TestLangmuirConstructorParamsOutsideConstraints():
    """
    I'm not implemeting these tests yet because they should be common
    across all the classes found in `tec.models`.
    """
    def test_emitter_temperature_lt_collector_temperature(self, valid_emitter_args, valid_collector_args):
        raise

    def test_emitter_temperature_eq_collector_temperature(self, valid_emitter_args, valid_collector_args):
        raise

    def test_emitter_barrier_lt_collector_barrier(self, valid_emitter_args, valid_collector_args):
        raise

    def test_emitter_barrier_eq_collector_barrier(self, valid_emitter_args, valid_collector_args):
        raise

    def test_emitter_position_gt_collector_position(self, valid_emitter_args, valid_collector_args):
        raise

    def test_emitter_position_eq_collector_position(self, valid_emitter_args, valid_collector_args):
        raise


@pytest.mark.xfail(reason="Method needs to be implemented.")
class TestLangmuirfrom_argsCases():
    """
    I'm not implemeting these tests yet because they should be common
    across all the classes found in `tec.models`.

    I may need to write more of these tests; `test/test_Ideal.py` has
    some.
    """
    def test_returns_TEC(self, valid_emitter_args, valid_collector_args):
        args = dict({"emitter_" + key: val for key, val in valid_emitter_args.items()})
        args.update({"collector_" + key: val for key, val in valid_collector_args.items()})

        assert isinstance(tec.models.Langmuir.from_args(**args), tec.TEC)


class TestLangmuirMethodsConsistency():
    """
    Test specific conditions for `Langmuir` object's methods
    """
    @pytest.mark.parametrize("current_density", [
            -0.5,
            astropy.units.Quantity(-0.5, "A/cm2"),
            ]
        )
    def test_normalization_length_current_density_lt_0_raises(self, valid_langmuir_model, current_density):
        with pytest.raises(ValueError):
            norm_l = valid_langmuir_model.normalization_length(current_density)


    @pytest.mark.parametrize("current_density", [
            0.,
            astropy.units.Quantity(0., "A/cm2"),
            ]
        )
    def test_normalization_length_current_density_eq_0_does_not_raise(self, valid_langmuir_model, current_density):
        with does_not_raise():
                norm_l = valid_langmuir_model.normalization_length(current_density)


    @pytest.mark.parametrize("current_density", [
            0.5,
            astropy.units.Quantity(0.5, "A/cm2"),
            ]
        )
    def test_normalization_length_current_density_gt_0_does_not_raise(self, valid_langmuir_model, current_density):
        with does_not_raise():
                norm_l = valid_langmuir_model.normalization_length(current_density)


    def test_normalization_length_current_density_incompatible_unit(self, valid_langmuir_model):
        current_density = astropy.units.m

        with pytest.raises(astropy.units.core.UnitConversionError):
            norm_l = valid_langmuir_model.normalization_length(current_density)


class TestLangmuirMethodsHappyPath():
    """
    Methods should just run without raising any exceptions
    """
    def test_saturation_point_voltage_does_not_raise(self, valid_langmuir_model):
        with does_not_raise():
            saturation_point_voltage = valid_langmuir_model.saturation_point_voltage()


    def test_saturation_point_current_density_does_not_raise(self, valid_langmuir_model):
        with does_not_raise():
            saturation_point_current_density = valid_langmuir_model.saturation_point_current_density()


    def test_critical_point_voltage_does_not_raise(self, valid_langmuir_model):
        with does_not_raise():
            critical_point_voltage = valid_langmuir_model.critical_point_voltage()


    def test_critical_point_current_density_does_not_raise(self, valid_langmuir_model):
        with does_not_raise():
            critical_point_current_density = valid_langmuir_model.critical_point_current_density()


    def test_max_motive_does_not_raise(self, valid_langmuir_model):
        with does_not_raise():
            max_motive = valid_langmuir_model.max_motive()


@pytest.fixture
def valid_langmuir_model(valid_emitter, valid_collector):
    langmuir_model = tec.models.Langmuir(emitter=valid_emitter, collector=valid_collector)

    return langmuir_model
