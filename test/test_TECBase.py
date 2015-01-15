# -*- coding: utf-8 -*-
import numpy as np
from tec.electrode import Metal
from tec import TECBase
from astropy import units
import unittest
import copy

em = Metal(temp=1000., barrier=2., richardson=10.)
co = Metal(temp=300., barrier=1., richardson=10., position=10.)


class TestBaseWithTEC(unittest.TestCase):
    """
    Provide fresh TECBase object for testing

    This class is intended to be subclassed so that I don't have to rewrite the same `setUp` method for each class containing tests.
    """
    def setUp(self):
        """
        Create new TECBase object for every test
        """
        if em.position > co.position:
            raise ValueError("Initialization em.position > co.position.")

        self.t = TECBase(em, co)


class InstantiationInputArgsWrongType(unittest.TestCase):
    """
    Test instantiation with non-`tec.electrode` args
    """
    pass


class SetAttribsWrongType(unittest.TestCase):
    """
    Tests setting attributes with non-`tec.electrode` data
    """
    pass


class CalculatorsInput(TestBaseWithTEC):
    """
    Tests calculator methods that take input
    """
    def test_i64(self):
        """
        calc_motive should exit with valid input

        Tests issue #64.
        """
        abscissae = units.Quantity([self.t.emitter.position, self.t.collector.position])
        position = abscissae.mean()

        self.t.calc_motive(position)

    def test_calc_motive_valid_quantity_array(self):
        """
        calc_motive should accept valid numpy array input

        Valid input means the values fall within the interelectrode space.
        """
        abscissae = units.Quantity([self.t.emitter.position, self.t.collector.position])

        self.t.calc_motive(abscissae)
        
    def test_calc_motive_valid_numpy_array(self):
        """
        calc_motive should accept valid numpy array input

        Valid input means the values fall within the interelectrode space.
        """
        abscissae = units.Quantity([self.t.emitter.position, self.t.collector.position])

        self.t.calc_motive(abscissae.value)
        
    def test_calc_motive_non_numeric(self):
        """
        calc_motive should raise TypeError with non-numeric, non astropy.units.Quantity input
        """
        position = "this string is non-numeric"
        self.assertRaises(TypeError, self.t.calc_motive, position)

    def test_calc_motive_num_below_interelectrode_space(self):
        """
        calc_motive should raise ValueError for numerical input below the interelectrode space
        """
        offset = units.Quantity(1., "um")
        position = -np.abs(em.position.value) - offset.value
        self.assertRaises(ValueError, self.t.calc_motive, position)

    def test_calc_motive_num_above_interelectrode_space(self):
        """
        calc_motive should raise ValueError for numerical input below the interelectrode space
        """
        offset = units.Quantity(1., "um")
        position = np.abs(co.position.value) + offset.value
        self.assertRaises(ValueError, self.t.calc_motive, position)

    def test_calc_motive_quantity_below_interelectrode_space(self):
        """
        calc_motive should raise ValueError for numerical input below the interelectrode space
        """
        offset = units.Quantity(1., "um")
        position = -np.abs(em.position) - offset
        self.assertRaises(ValueError, self.t.calc_motive, position)

    def test_calc_motive_quantity_above_interelectrode_space(self):
        """
        calc_motive should raise ValueError for numerical input below the interelectrode space
        """
        offset = units.Quantity(1., "um")
        position = np.abs(co.position) + offset
        self.assertRaises(ValueError, self.t.calc_motive, position)


class CalculatorsReturnType(TestBaseWithTEC):
    """
    Tests output types of the calculator methods
    """
    def test_calc_motive(self):
        """
        calc_motive should return an astropy.units.Quantity
        """
        abscissae = units.Quantity([self.t.emitter.position, self.t.collector.position])
        position = abscissae.mean()

        self.assertIsInstance(self.t.calc_motive(position), units.Quantity)

    def test_calc_max_motive(self):
        """
        calc_max_motive should return an astropy.units.Quantity
        """
        self.assertIsInstance(self.t.calc_max_motive(), units.Quantity)

    def test_calc_max_motive_position(self):
        """
        calc_max_motive_position should return astropy.units.Quantity
        """
        self.assertIsInstance(self.t.calc_max_motive_position(), units.Quantity)

    def test_calc_interelectrode_spacing(self):
        """
        calc_interelectrode_spacing should return astropy.units.Quantity
        """
        self.assertIsInstance(self.t.calc_interelectrode_spacing(), units.Quantity)

    def test_calc_output_voltage(self):
        """
        calc_output_voltage should return astropy.units.Quantity
        """
        self.assertIsInstance(self.t.calc_output_voltage(), units.Quantity)

    def test_calc_contact_potential(self):
        """
        calc_contact_potential should return astropy.units.Quantity
        """
        self.assertIsInstance(self.t.calc_contact_potential(), units.Quantity)

    def test_calc_forward_current_density(self):
        """
        calc_forward_current_density should return astropy.units.Quantity
        """
        self.assertIsInstance(self.t.calc_forward_current_density(), units.Quantity)

    def test_calc_back_current_density(self):
        """
        calc_back_current_density should return astropy.units.Quantity
        """
        self.assertIsInstance(self.t.calc_back_current_density(), units.Quantity)

    def test_calc_output_current_density(self):
        """
        calc_output_current_density should return astropy.units.Quantity
        """
        self.assertIsInstance(self.t.calc_output_current_density(), units.Quantity)

    def test_calc_output_power_density(self):
        """
        calc_output_power_density should return astropy.units.Quantity
        """
        self.assertIsInstance(self.t.calc_output_power_density(), units.Quantity)

    def test_calc_carnot_efficiency(self):
        """
        calc_carnot_efficiency should return float
        """
        self.assertIsInstance(self.t.calc_carnot_efficiency(), float)

    def test_calc_efficiency(self):
        """
        calc_efficiency should return float
        """
        self.t.collector.voltage = 0.1
        self.assertIsInstance(self.t.calc_efficiency(), float)

    def test_calc_heat_supply_rate(self):
        """
        calc_heat_supply_rate should return astropy.units.Quantity
        """
        self.assertIsInstance(self.t.calc_heat_supply_rate(), units.Quantity)

    def test_calc_electron_cooling_rate(self):
        """
        calc_electron_cooling_rate should return astropy.units.Quantity
        """
        self.assertIsInstance(self.t.calc_electron_cooling_rate(), units.Quantity)

    def test_calc_thermal_rad_rate(self):
        """
        calc_thermal_rad_rate should return astropy.units.Quantity
        """
        self.assertIsInstance(self.t.calc_thermal_rad_rate(), units.Quantity)


class CalculatorsReturnUnits(TestBaseWithTEC):
    """
    Tests output units, where applicable, of the calculator methods
    """
    def test_calc_motive(self):
        """
        calc_motive should return a value with unit eV
        """
        abscissae = units.Quantity([self.t.emitter.position, self.t.collector.position])
        position = abscissae.mean()

        self.assertEqual(self.t.calc_motive(position).unit, units.Unit("eV"))

    def test_calc_max_motive(self):
        """
        calc_max_motive should return a value with unit eV
        """
        self.assertEqual(self.t.calc_max_motive().unit, units.Unit("eV"))

    def test_calc_max_motive_position(self):
        """
        calc_max_motive_position should return a value with unit um
        """
        self.assertEqual(self.t.calc_max_motive_position().unit, units.Unit("um"))

    def test_calc_interelectrode_spacing(self):
        """
        calc_interelectrode_spacing should return a value with unit um
        """
        self.assertEqual(self.t.calc_interelectrode_spacing().unit, units.Unit("um"))

    def test_calc_output_voltage(self):
        """
        calc_output_voltage should return a value with unit V
        """
        self.assertEqual(self.t.calc_output_voltage().unit, units.Unit("V"))

    def test_calc_contact_potential(self):
        """
        calc_contact_potential should return a value with unit V
        """
        self.assertEqual(self.t.calc_contact_potential().unit, units.Unit("V"))

    def test_calc_forward_current_density(self):
        """
        calc_forward_current_density should return a value with unit A/cm2
        """
        self.assertEqual(self.t.calc_forward_current_density().unit, units.Unit("A/cm2"))

    def test_calc_back_current_density(self):
        """
        calc_back_current_density should return a value with unit A/cm2
        """
        self.assertEqual(self.t.calc_back_current_density().unit, units.Unit("A/cm2"))

    def test_calc_output_current_density(self):
        """
        calc_output_current_density should return a value with unit A/cm2
        """
        self.assertEqual(self.t.calc_output_current_density().unit, units.Unit("A/cm2"))

    def test_calc_output_power_density(self):
        """
        calc_output_power_density should return a value with unit W/cm2
        """
        self.assertEqual(self.t.calc_output_power_density().unit, units.Unit("W/cm2"))


class CalculatorsReturnValues(TestBaseWithTEC):
    """
    Tests values of calculator methods against known values
    """
    def test_calc_thermal_rad_rate_emitter_emissivity_0(self):
        """
        calc_thermal_rad_rate should return zero if the emitter emissivity is zero
        """
        self.t.emitter.emissivity = 0.
        self.t.collector.emissivity = 0.5
        self.assertEqual(self.t.calc_thermal_rad_rate(), 0)

    def test_calc_thermal_rad_rate_collector_emissivity_0(self):
        """
        calc_thermal_rad_rate should return zero if the collector emissivity is zero
        """
        self.t.emitter.emissivity = 0.5
        self.t.collector.emissivity = 0.
        self.assertEqual(self.t.calc_thermal_rad_rate(), 0)

    def test_calc_thermal_rad_rate_electrodes_emissivity_0(self):
        """
        calc_thermal_rad_rate should return zero if the both electrodes' emissivity is zero
        """
        self.t.emitter.emissivity = 0.
        self.t.collector.emissivity = 0.
        self.assertEqual(self.t.calc_thermal_rad_rate(), 0)
