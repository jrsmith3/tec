# -*- coding: utf-8 -*-
import numpy as np
from astropy import units
import unittest
from tec.electrode import Metal
from tec.models import Langmuir

em = Metal(temp=1000., barrier=2., richardson=10.)
co = Metal(temp=300., barrier=1., richardson=10., position=10.)


class Base(unittest.TestCase):
    """
    Base class for tests

    This class is intended to be subclassed so that I don't have to rewrite the same `setUp` method for each class containing tests.
    """
    def setUp(self):
        """
        Create new Langmuir object for every test
        """
        if em.position > co.position:
            raise ValueError("Initialization em.position > co.position.")

        self.t = Langmuir(em, co)

        self.em = em
        self.co = co


class MethodsInput(Base):
    """
    Tests methods which take input parameters

    Tests include: passing invalid input, etc.
    """
    pass


class MethodsReturnType(Base):
    """
    Tests methods' output types
    """
    pass
    

class MethodsReturnUnits(Base):
    """
    Tests methods' output units where applicable
    """
    pass


class MethodsReturnValues(Base):
    """
    Tests values of methods against known values
    """
    pass
