# -*- coding: utf-8 -*-

from weakref import WeakKeyDictionary
from physicalproperty import PhysicalProperty
import constants
import numpy as np
import scipy
from astropy import units
import json

class Electrode(object):
    """
    Thermoelectron electrode.

    An Electrode is instantiated with a dict having keys identical to the class's public data attributes. Each key's value must satisfy the constraints noted with the corresponding public data attribute. Dictionary values can be some kind of numeric type or of type `astropy.units.Quantity` so long as the units are compatible with what's listed.

    All numerical methods return data of type astropy.units.Quantity.
    """
    temp = PhysicalProperty(unit = "K", lo_bnd = 0)
    """
    Temperature > 0 [K]
    """

    barrier = PhysicalProperty(unit = "eV", lo_bnd = 0)
    """
    Emission barrier >=0 [eV]. Sometimes referred to as work function. The barrier is the difference between the lowest energy for which an electron inside a material can escape and the Fermi energy.
    """

    richardson = PhysicalProperty(unit = "A/(cm2 K2)", lo_bnd = 0)
    """
    Richardson Constant >=0 [A cm^{-2} K^{-2}]
    """


    def __init__(self, params):
        for attr in self._list_PhysicalProperty_attr_names():
            setattr(self, attr, params[attr])

    def __repr__(self):
        return str(self._to_dict())

    def _list_PhysicalProperty_attr_names(self):
        """
        Return a list of public data attributes that are of type `PhysicalProperty` owned by the `Electrode` class.
        """
        physical_prop_names = []

        for attr in dir(self.__class__):
            if type(self.__class__.__dict__.get(attr)) is PhysicalProperty:
                physical_prop_names.append(attr)

        return physical_prop_names

    def _to_dict(self):
        """
        Return a dictionary representation of the current object.
        """
        physical_prop_names = self._list_PhysicalProperty_attr_names()
        physical_prop_vals = [getattr(self, prop) for prop in physical_prop_names]

        return dict(zip(physical_prop_names, physical_prop_vals))

    def calc_richardson_current_density(self):
        """
        Current density according to the Richardson eqn in [A cm^{-2}].

        J = A T^{2} \exp{ \phi / kT }

        If either temp or richardson are equal to 0, this  method returns a value of 0.
        """
        if self.temp.value == 0:
          current_density = units.Quantity(0, "A/cm2")
        else:
            exponent = (self.barrier / (constants.k * self.temp)).decompose()
            coefficient = self.richardson * self.temp**2
            current_density = coefficient * np.exp(-exponent)
        
        return current_density.to("A/cm2")
