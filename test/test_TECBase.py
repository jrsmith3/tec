# -*- coding: utf-8 -*-
import numpy as np
from tec.electrode import Metal
from tec import TECBase
from astropy.units import Quantity
from astropy.units import Unit
import unittest
import copy

em = Metal(temp=1000., barrier=2., richardson=10.)
co = Metal(temp=300., barrier=1., richardson=10.)


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


class CalculatorsReturnType(unittest.TestCase):
    """
    Tests output types of the calculator methods
    """
    pass


class CalculatorsReturnUnits(unittest.TestCase):
    """
    Tests output units, where applicable, of the calculator methods
    """


class CalculatorsReturnValues(unittest.TestCase):
    """
    Tests values of calculator methods against known values
    """
    pass
