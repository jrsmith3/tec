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
class TestIdealfrom_argsCases():
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



def test_normalization_length_current_density_eq_0(self, valid_langmuir_model):
    pass

def test_normalization_length_current_density_gt_0(self, valid_langmuir_model):
    pass


@pytest.fixture
def valid_langmuir_model(valid_emitter, valid_collector):
    langmuir_model = tec.models.Langmuir(emitter=valid_emitter, collector=valid_collector)

    return langmuir_model


# --------------------------------------------------------------------
# em_params = {"temp": 1000.,
#              "barrier": 2.,
#              "richardson": 10., }

# co_params = {"temp": 300.,
#              "barrier": 1.,
#              "richardson": 10.,
#              "position": 10., }

# em = Metal(**em_params)
# co = Metal(**co_params)


# class Base(unittest.TestCase):
#     """
#     Base class for tests

#     This class is intended to be subclassed so that I don't have to rewrite the same `setUp` method for each class containing tests.
#     """
#     def setUp(self):
#         """
#         Create new Langmuir object for every test
#         """
#         if em.position > co.position:
#             raise ValueError("Initialization em.position > co.position.")

#         self.t = Langmuir(em, co)

#         self.em = em
#         self.co = co

#         # Create `Langmuir` objects for each regime: accelerating,
#         # space charge limited, and retarding.
#         saturation_point_voltage = self.t.saturation_point_voltage()
#         critical_point_voltage = self.t.critical_point_voltage()

#         # accelerating mode:
#         accelerating_voltage = saturation_point_voltage - units.Quantity(1., "V")
#         co_accelerating = Metal(**co_params)
#         co_accelerating.voltage = accelerating_voltage

#         self.t_accel = Langmuir(em, co_accelerating)

#         # space charge limited mode:
#         scl_voltage = (saturation_point_voltage + critical_point_voltage) / 2
#         co_scl = Metal(**co_params)
#         co_scl.voltage = scl_voltage

#         self.t_scl = Langmuir(em, co_scl)

#         # retarding mode:
#         retarding_voltage = critical_point_voltage + units.Quantity(1., "V")
#         co_retarding = Metal(**co_params)
#         co_retarding.voltage = retarding_voltage

#         self.t_ret = Langmuir(em, co_retarding)


# class Instantiation(Base):
#     """
#     Tests all aspects of instantiation

#     Tests include: instantiation with args of wrong type, etc.
#     """
#     def test_additional_arbitrary_args(self):
#         """
#         Langmuir can be instantiated with additional arbitrary args
#         """
#         try:
#             el = Langmuir(em, co, not_an_arg="nope sure not")
#         except TypeError:
#             self.fail("Instantiation failed with additional arbitrary args")


# class MethodsInput(Base):
#     """
#     Tests methods which take input parameters

#     Tests include: passing invalid input, etc.
#     """
#     def test_normalization_length_non_numeric(self):
#         """
#         normalization_length should raise TypeError with non-numeric, non astropy.units.Quantity input
#         """
#         current_density = "this string is non-numeric"
#         self.assertRaises(TypeError, self.t.normalization_length, current_density)

#     def test_normalization_length_negative_current_density(self):
#         """
#         normalization_length should raise ValueError with negative value of input
#         """
#         current_density = -1.
#         self.assertRaises(ValueError, self.t.normalization_length, current_density)

#     def test_critical_point_target_function_above_bound(self):
#         """
#         critical_point_target_function should raise ValueError if input is greater than the upper bound
#         """
#         current_density = 2 * self.t.emitter.thermoelectron_current_density()
#         self.assertRaises(ValueError, self.t.critical_point_target_function, current_density)

#     def test_critical_point_target_function_below_bound(self):
#         """
#         critical_point_target_function should raise ValueError if input is greater than the upper bound
#         """
#         current_density = -1.
#         self.assertRaises(ValueError, self.t.critical_point_target_function, current_density)


# class MethodsReturnType(Base):
#     """
#     Tests methods' output types
#     """
#     def test_back_current_density(self):
#         """
#         back_current_density should return astropy.units.Quantity
#         """
#         self.assertIsInstance(self.t.back_current_density(), units.Quantity)

#     def test_normalization_length(self):
#         """
#         normalization_length should return astropy.units.Quantity
#         """
#         current_density = units.Quantity(1, "A cm-2")
#         self.assertIsInstance(self.t.normalization_length(current_density), units.Quantity)

#     def test_saturation_point_voltage(self):
#         """
#         saturation_point_voltage should return astropy.units.Quantity
#         """
#         self.assertIsInstance(self.t.saturation_point_voltage(), units.Quantity)

#     def test_saturation_point_current_density(self):
#         """
#         saturation_point_current_density should return astropy.units.Quantity
#         """
#         self.assertIsInstance(self.t.saturation_point_current_density(), units.Quantity)

#     def test_critical_point_voltage(self):
#         """
#         critical_point_voltage should return astropy.units.Quantity
#         """
#         self.assertIsInstance(self.t.critical_point_voltage(), units.Quantity)

#     def test_critical_point_current_density(self):
#         """
#         critical_point_current_density should return astropy.units.Quantity
#         """
#         self.assertIsInstance(self.t.critical_point_current_density(), units.Quantity)

#     def test_critical_point_target_function(self):
#         """
#         critical_point_target_function should return float
#         """
#         current_density = 0.5 * self.t.emitter.thermoelectron_current_density()
#         self.assertIsInstance(self.t.critical_point_target_function(current_density), float)

#     def test_max_motive_accelerating_regime(self):
#         """
#         max_motive should return astropy.units.Quantity in the accelerating regime
#         """
#         self.assertIsInstance(self.t_accel.max_motive(), units.Quantity)

#     def test_max_motive_space_charge_regime(self):
#         """
#         max_motive should return astropy.units.Quantity in the space charge limited regime
#         """
#         self.assertIsInstance(self.t_scl.max_motive(), units.Quantity)

#     def test_max_motive_retarding_regime(self):
#         """
#         max_motive should return astropy.units.Quantity in the retarding regime
#         """
#         self.assertIsInstance(self.t_ret.max_motive(), units.Quantity)

#     def test_output_voltage_target_function_Quantity_argument(self):
#         """
#         output_voltage_target_function should return float when called with `astropy.units.Quantity` argument

#         This test could also be located in the `MethodsInput` test class.
#         """
#         current_density = self.t.emitter.thermoelectron_current_density()
#         self.assertIsInstance(self.t.output_voltage_target_function(current_density), float)

#     def test_output_voltage_target_function_float_argument(self):
#         """
#         output_voltage_target_function should return float when called with `astropy.units.float` argument

#         This test could also be located in the `MethodsInput` test class.
#         """
#         current_density = self.t.emitter.thermoelectron_current_density()
#         self.assertIsInstance(self.t.output_voltage_target_function(current_density.value), float)

#     def test_operating_regime_accelerating_regime(self):
#         """
#         operating_regime should return str in the accelerating regime
#         """
#         self.assertIsInstance(self.t_accel.operating_regime(), str)

#     def test_operating_regime_space_charge_regime(self):
#         """
#         operating_regime should return str in the space charge limited regime
#         """
#         self.assertIsInstance(self.t_scl.operating_regime(), str)

#     def test_operating_regime_retarding_regime(self):
#         """
#         operating_regime should return str in the retarding regime
#         """
#         self.assertIsInstance(self.t_ret.operating_regime(), str)


# class MethodsReturnUnits(Base):
#     """
#     Tests methods' output units where applicable
#     """
#     def test_back_current_density(self):
#         """
#         back_current_density should return a value with unit A/cm2
#         """
#         self.assertEqual(self.t.back_current_density().unit, units.Unit("A/cm2"))

#     def test_normalization_length(self):
#         """
#         normalization_length should return a value with unit um
#         """
#         current_density = units.Quantity(1, "A cm-2")
#         self.assertEqual(self.t.normalization_length(current_density).unit, units.Unit("um"))

#     def test_saturation_point_voltage(self):
#         """
#         saturation_point_voltage should return a value with unit V
#         """
#         self.assertEqual(self.t.saturation_point_voltage().unit, units.Unit("V"))

#     def test_saturation_point_current_density(self):
#         """
#         saturation_point_current_density should return a value with unit A cm^{-2}
#         """
#         self.assertEqual(self.t.saturation_point_current_density().unit, units.Unit("A cm-2"))

#     def test_critical_point_voltage(self):
#         """
#         critical_point_voltage should return a value with unit V
#         """
#         self.assertEqual(self.t.critical_point_voltage().unit, units.Unit("V"))

#     def test_critical_point_current_density(self):
#         """
#         critical_point_current_density should return a value with unit A cm^{-2}
#         """
#         self.assertEqual(self.t.critical_point_current_density().unit, units.Unit("A cm-2"))

#     def test_max_motive_accelerating_regime(self):
#         """
#         max_motive should return a value with unit eV in the accelerating regime
#         """
#         self.assertEqual(self.t_accel.max_motive().unit, units.Unit("eV"))

#     def test_max_motive_space_charge_regime(self):
#         """
#         max_motive should return a value with unit eV in the space charge limited regime
#         """
#         self.assertEqual(self.t_scl.max_motive().unit, units.Unit("eV"))

#     def test_max_motive_retarding_regime(self):
#         """
#         max_motive should return a value with unit eV in the retarding regime
#         """
#         self.assertEqual(self.t_ret.max_motive().unit, units.Unit("eV"))


# class MethodsReturnValues(Base):
#     """
#     Tests values of methods against known values
#     """
#     def test_issue_155(self):
#         """
#         Langmuir.max_motive raises ValueError

#         There's a case where the `Langmuir.max_motive` method will raise a `ValueError`. Specifically when `self.critical_point_current_density() == self.calc_saturation_point_current_density()`. This condition is tested to ensure the `ValueError` is not raised.

#         See: https://github.com/jrsmith3/tec/issues/155
#         """
#         em_params = {'barrier': 1.0,
#                      'emissivity': 0.0,
#                      'position': 0.0,
#                      'richardson': 10.0,
#                      'temp': 300.0,
#                      'voltage': 0.0}

#         co_params = {'barrier': 1.0,
#                      'emissivity': 0.0,
#                      'position': 1.0,
#                      'richardson': 10.0,
#                      'temp': 300.0,
#                      'voltage': 0.0}

#         em = Metal.from_dict(em_params)
#         co = Metal.from_dict(co_params)
#         l = Langmuir(em, co)

#         try:
#             l.max_motive()
#         except ValueError:
#             self.fail("Issue #155 not resolved")