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
        TECBase.calc_motive should exit with valid input

        Tests issue #64.
        """
        abscissae = units.Quantity([self.t.emitter.position, self.t.collector.position])
        position = abscissae.mean()

        self.t.calc_motive(position)

    def test_calc_motive_num_below_interelectrode_space(self):
        """
        TECBase.calc_motive should raise ValueError for numerical input below the interelectrode space
        """
        pass

    def test_calc_motive_num_above_interelectrode_space(self):
        """
        TECBase.calc_motive should raise ValueError for numerical input below the interelectrode space
        """
        pass

    def test_calc_motive_quantity_below_interelectrode_space(self):
        """
        TECBase.calc_motive should raise ValueError for numerical input below the interelectrode space
        """
        pass

    def test_calc_motive_quantity_above_interelectrode_space(self):
        """
        TECBase.calc_motive should raise ValueError for numerical input below the interelectrode space
        """
        pass


class CalculatorsReturnType(TestBaseWithTEC):
    """
    Tests output types of the calculator methods
    """
    def test_calc_motive(self):
        """
        TECBase.calc_motive should return an astropy.units.Quantity
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
        TECBase.calc_motive should return a value with unit eV
        """
        abscissae = units.Quantity([self.t.emitter.position, self.t.collector.position])
        position = abscissae.mean()

        self.assertEqual(self.t.calc_motive(position).unit, units.Unit("eV"))


class CalculatorsReturnValues(unittest.TestCase):
    """
    Tests values of calculator methods against known values
    """
    pass
