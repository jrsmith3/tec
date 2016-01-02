# -*- coding: utf-8 -*-

import collections
import numpy as np
from tec.electrode import Metal
from tec import TECBase
from astropy import units
import unittest
import copy

em_params = {"temp": 1000.,
            "barrier": 2.,
            "richardson": 10.,}

co_params = {"temp": 300.,
            "barrier": 1.,
            "richardson": 10.,
            "position": 10.,}

em = Metal(**em_params)
co = Metal(**co_params)


class Base(unittest.TestCase):
    """
    Base class for tests

    This class is intended to be subclassed so that I don't have to rewrite the same `setUp` method for each class containing tests.
    """
    def setUp(self):
        """
        Create new TECBase object for every test
        """
        if em.position > co.position:
            raise ValueError("Initialization em.position > co.position.")

        self.t = TECBase(em, co)

        self.em = em
        self.co = co

        self.em_params = em_params
        self.co_params = co_params


class Instantiation(Base):
    """
    Tests all aspects of instantiation

    Tests include: instantiation with args of wrong type, etc.
    """
    # Instantiation via `__init__`
    # ============================
    def test_emitter_non_electrode(self):
        """
        emitter nonelectrode -> TECBase init raises TypeError
        """
        non_electrode = "this string is not an electrode"
        self.assertRaises(TypeError, TECBase, non_electrode, self.co)

    def test_collector_non_electrode(self):
        """
        collector nonelectrode -> TECBase init raises TypeError
        """
        non_electrode = "this string is not an electrode"
        self.assertRaises(TypeError, TECBase, self.em, non_electrode)

    def test_additional_arbitrary_args(self):
        """
        TECBase can be instantiated with additional arbitrary args
        """
        try:
            el = TECBase(em, co, not_an_arg="nope sure not")
        except TypeError:
            self.fail("Instantiation failed with additional arbitrary args")

    # Instantiation via `from_dict`
    # =============================
    # Bad input
    # ---------
    def test_from_dict_emitter_missing(self):
        """
        TECBase.from_dict raises TypeError when misisng "emitter"
        """
        params = {"collector": self.co}
        self.assertRaises(TypeError, TECBase.from_dict, params)

    def test_from_dict_emitter_non_electrode(self):
        """
        emitter nonelectrode -> TECBase init raises TypeError
        """
        params = {"emitter": "not an electrode",
            "collector": self.co}
        self.assertRaises(TypeError, TECBase.from_dict, params)

    def test_from_dict_collector_non_electrode(self):
        """
        collector nonelectrode -> TECBase init raises TypeError
        """
        params = {"emitter": self.em,
            "collector": "not an electrode"}
        self.assertRaises(TypeError, TECBase.from_dict, params)

    # Valid input
    # -----------
    def test_from_dict_additional_arbitrary_args(self):
        """
        TECBase can be instantiated with additional arbitrary args
        """
        params = {"emitter": self.em,
            "collector": self.co,
            "not_an_arg": "nope sure not"}

        try:
            t = TECBase.from_dict(params)
        except TypeError:
            self.fail("Instantiation failed with additional arbitrary args")


class Set(Base):
    """
    Tests all aspects of setting attributes

    Tests include: setting attributes of wrong type, etc.
    """
    def test_emitter_non_electrode(self):
        """
        set emitter nonelectrode raises TypeError
        """
        non_electrode = "this string is not an electrode"
        try:
            self.t.emitter = non_electrode
        except TypeError:
            # Setting `emitter` as a type that isn't a subclass of `tec.electrode.Metal` should raise a TypeError, so things are working.
            pass
        else:
            self.fail("`emitter` attribute can be assigned a non-electrode value.")

    def test_collector_non_electrode(self):
        """
        set collector nonelectrode raises TypeError
        """
        non_electrode = "this string is not an electrode"
        try:
            self.t.collector = non_electrode
        except TypeError:
            # Setting `collector` as a type that isn't a subclass of `tec.electrode.Metal` should raise a TypeError, so things are working.
            pass
        else:
            self.fail("`collector` attribute can be assigned a non-electrode value.")


class Iteration(Base):
    """
    Tests class's iteration API
    """
    # TECBase.iterelectrodes
    def test_iterelectrodes_is_iterable(self):
        """
        TECBase.iterelectrodes must be iterable
        """
        self.assertIsInstance(self.t.iterelectrodes(), collections.Iterable)

    # TECBase.iterelectrodesdicts
    def test_iterelectrodesdicts_is_iterable(self):
        """
        TECBase.iterelectrodesdicts must be iterable
        """
        self.assertIsInstance(self.t.iterelectrodesdicts(), collections.Iterable)

    # TECBase.__iter__
    def test_is_iterable(self):
        """
        TECBase must be iterable
        """
        self.assertIsInstance(self.t, collections.Iterable)


class MethodsInput(Base):
    """
    Tests methods which take input parameters

    Tests include: passing invalid input, etc.
    """
    def test_i64(self):
        """
        motive should exit with valid input

        Tests issue #64.
        """
        abscissae = units.Quantity([self.t.emitter.position, self.t.collector.position])
        position = abscissae.mean()

        self.t.motive(position)

    def test_motive_valid_quantity_array(self):
        """
        motive should accept valid numpy array input

        Valid input means the values fall within the interelectrode space.
        """
        abscissae = units.Quantity([self.t.emitter.position, self.t.collector.position])

        self.t.motive(abscissae)

    def test_motive_valid_numpy_array(self):
        """
        motive should accept valid numpy array input

        Valid input means the values fall within the interelectrode space.
        """
        abscissae = units.Quantity([self.t.emitter.position, self.t.collector.position])

        self.t.motive(abscissae.value)

    def test_motive_non_numeric(self):
        """
        motive should raise TypeError with non-numeric, non astropy.units.Quantity input
        """
        position = "this string is non-numeric"
        self.assertRaises(TypeError, self.t.motive, position)

    def test_motive_num_below_interelectrode_space(self):
        """
        motive should raise ValueError for numerical input below the interelectrode space
        """
        offset = units.Quantity(1., "um")
        position = -np.abs(em.position.value) - offset.value
        self.assertRaises(ValueError, self.t.motive, position)

    def test_motive_num_above_interelectrode_space(self):
        """
        motive should raise ValueError for numerical input above the interelectrode space
        """
        offset = units.Quantity(1., "um")
        position = np.abs(co.position.value) + offset.value
        self.assertRaises(ValueError, self.t.motive, position)

    def test_motive_quantity_below_interelectrode_space(self):
        """
        motive should raise ValueError for numerical input below the interelectrode space
        """
        offset = units.Quantity(1., "um")
        position = -np.abs(em.position) - offset
        self.assertRaises(ValueError, self.t.motive, position)

    def test_motive_quantity_above_interelectrode_space(self):
        """
        motive should raise ValueError for numerical input above the interelectrode space
        """
        offset = units.Quantity(1., "um")
        position = np.abs(co.position) + offset
        self.assertRaises(ValueError, self.t.motive, position)


class MethodsReturnType(Base):
    """
    Tests methods' output types
    """
    def test_motive(self):
        """
        motive should return an astropy.units.Quantity
        """
        abscissae = units.Quantity([self.t.emitter.position, self.t.collector.position])
        position = abscissae.mean()

        self.assertIsInstance(self.t.motive(position), units.Quantity)

    def test_max_motive(self):
        """
        max_motive should return an astropy.units.Quantity
        """
        self.assertIsInstance(self.t.max_motive(), units.Quantity)

    def test_max_motive_position(self):
        """
        max_motive_position should return astropy.units.Quantity
        """
        self.assertIsInstance(self.t.max_motive_position(), units.Quantity)

    def test_interelectrode_spacing(self):
        """
        interelectrode_spacing should return astropy.units.Quantity
        """
        self.assertIsInstance(self.t.interelectrode_spacing(), units.Quantity)

    def test_output_voltage(self):
        """
        output_voltage should return astropy.units.Quantity
        """
        self.assertIsInstance(self.t.output_voltage(), units.Quantity)

    def test_contact_potential(self):
        """
        contact_potential should return astropy.units.Quantity
        """
        self.assertIsInstance(self.t.contact_potential(), units.Quantity)

    def test_forward_current_density(self):
        """
        forward_current_density should return astropy.units.Quantity
        """
        self.assertIsInstance(self.t.forward_current_density(), units.Quantity)

    def test_back_current_density(self):
        """
        back_current_density should return astropy.units.Quantity
        """
        self.assertIsInstance(self.t.back_current_density(), units.Quantity)

    def test_output_current_density(self):
        """
        output_current_density should return astropy.units.Quantity
        """
        self.assertIsInstance(self.t.output_current_density(), units.Quantity)

    def test_output_power_density(self):
        """
        output_power_density should return astropy.units.Quantity
        """
        self.assertIsInstance(self.t.output_power_density(), units.Quantity)

    def test_carnot_efficiency(self):
        """
        carnot_efficiency should return float
        """
        self.assertIsInstance(self.t.carnot_efficiency(), float)

    def test_efficiency(self):
        """
        efficiency should return float
        """
        self.t.collector.voltage = 0.1
        if self.t.output_power_density() <= 0:
            raise ValueError("Output power density is non-positive; this test will not work.")
        self.assertIsInstance(self.t.efficiency(), float)

    def test_heat_supply_rate(self):
        """
        heat_supply_rate should return astropy.units.Quantity
        """
        self.assertIsInstance(self.t.heat_supply_rate(), units.Quantity)

    def test_electron_cooling_rate(self):
        """
        electron_cooling_rate should return astropy.units.Quantity
        """
        self.assertIsInstance(self.t.electron_cooling_rate(), units.Quantity)

    def test_thermal_rad_rate(self):
        """
        thermal_rad_rate should return astropy.units.Quantity
        """
        self.assertIsInstance(self.t.thermal_rad_rate(), units.Quantity)


class MethodsReturnUnits(Base):
    """
    Tests methods' output units where applicable
    """
    def test_motive(self):
        """
        motive should return a value with unit eV
        """
        abscissae = units.Quantity([self.t.emitter.position, self.t.collector.position])
        position = abscissae.mean()

        self.assertEqual(self.t.motive(position).unit, units.Unit("eV"))

    def test_max_motive(self):
        """
        max_motive should return a value with unit eV
        """
        self.assertEqual(self.t.max_motive().unit, units.Unit("eV"))

    def test_max_motive_position(self):
        """
        max_motive_position should return a value with unit um
        """
        self.assertEqual(self.t.max_motive_position().unit, units.Unit("um"))

    def test_interelectrode_spacing(self):
        """
        interelectrode_spacing should return a value with unit um
        """
        self.assertEqual(self.t.interelectrode_spacing().unit, units.Unit("um"))

    def test_output_voltage(self):
        """
        output_voltage should return a value with unit V
        """
        self.assertEqual(self.t.output_voltage().unit, units.Unit("V"))

    def test_contact_potential(self):
        """
        contact_potential should return a value with unit V
        """
        self.assertEqual(self.t.contact_potential().unit, units.Unit("V"))

    def test_forward_current_density(self):
        """
        forward_current_density should return a value with unit A/cm2
        """
        self.assertEqual(self.t.forward_current_density().unit, units.Unit("A/cm2"))

    def test_back_current_density(self):
        """
        back_current_density should return a value with unit A/cm2
        """
        self.assertEqual(self.t.back_current_density().unit, units.Unit("A/cm2"))

    def test_output_current_density(self):
        """
        output_current_density should return a value with unit A/cm2
        """
        self.assertEqual(self.t.output_current_density().unit, units.Unit("A/cm2"))

    def test_output_power_density(self):
        """
        output_power_density should return a value with unit W/cm2
        """
        self.assertEqual(self.t.output_power_density().unit, units.Unit("W/cm2"))

    def test_heat_supply_rate(self):
        """
        heat_supply_rate should return a value with unit W
        """
        self.assertEqual(self.t.heat_supply_rate().unit, units.Unit("W"))

    def test_electron_cooling_rate(self):
        """
        electron_cooling_rate should return a value with unit W
        """
        self.assertEqual(self.t.electron_cooling_rate().unit, units.Unit("W"))

    def test_thermal_rad_rate(self):
        """
        thermal_rad_rate should return a value with unit W
        """
        self.assertEqual(self.t.thermal_rad_rate().unit, units.Unit("W"))


class MethodsReturnValues(Base):
    """
    Tests values of methods against known values
    """
    def test_thermal_rad_rate_emitter_emissivity_0(self):
        """
        thermal_rad_rate should return zero if the emitter emissivity is zero
        """
        self.t.emitter.emissivity = 0.
        self.t.collector.emissivity = 0.5
        self.assertEqual(self.t.thermal_rad_rate(), 0)

    def test_thermal_rad_rate_collector_emissivity_0(self):
        """
        thermal_rad_rate should return zero if the collector emissivity is zero
        """
        self.t.emitter.emissivity = 0.5
        self.t.collector.emissivity = 0.
        self.assertEqual(self.t.thermal_rad_rate(), 0)

    def test_thermal_rad_rate_electrodes_emissivity_0(self):
        """
        thermal_rad_rate should return zero if the both electrodes' emissivity is zero
        """
        self.t.emitter.emissivity = 0.
        self.t.collector.emissivity = 0.
        self.assertEqual(self.t.thermal_rad_rate(), 0)
