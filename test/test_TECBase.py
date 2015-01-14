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


class CalculatorsReturnValues(unittest.TestCase):
    """
    Tests values of calculator methods against known values
    """
    pass
