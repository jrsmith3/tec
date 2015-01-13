# -*- coding: utf-8 -*-

import numpy as np
from astropy import units
from astropy import constants
from physicalproperty import PhysicalProperty, find_PhysicalProperty


class Metal(object):
    """
    Metal thermoelectron electrode

    A `Metal` electrode is instantiated with a dict having keys identical to the class's public data attributes. Each key's value must satisfy the constraints noted with the corresponding public data attribute. Dictionary values can be some kind of numeric type or of type `astropy.units.Quantity` so long as the units are compatible with what's listed.
    """
    temp = PhysicalProperty(unit="K", lo_bnd=0)
    """
    Temperature

    :symbol: :math:`T`
    """

    barrier = PhysicalProperty(unit="eV", lo_bnd=0)
    """
    Emission barrier (a.k.a. work function)

    The barrier is the difference between the vacuum energy of the surface and the Fermi energy.

    :symbol: :math:`\phi`
    """

    richardson = PhysicalProperty(unit="A/(cm2 K2)", lo_bnd=0)
    """
    Richardson constant

    :symbol: :math:`A`
    """

    def __init__(self, params):
        for attr in find_PhysicalProperty(self):
            setattr(self, attr, params[attr])

    def __repr__(self):
        return str(self._to_dict())

    def _to_dict(self):
        """
        Return a dictionary representation of the current object.
        """
        physical_prop_names = find_PhysicalProperty(self)
        physical_prop_vals = [getattr(self, prop) for prop in physical_prop_names]

        return dict(zip(physical_prop_names, physical_prop_vals))

    def calc_thermoelectron_current_density(self):
        """
        Thermoelectron emission current density

        This quantity is calculated according to the Richardson equation

        .. math::

            J_{RD} = A T^{2} \exp \left( \\frac{\phi}{kT} \\right)

        If either the `temp` or `richardson` attributes are equal to 0, this  method returns a value of 0.

        :returns: `astropy.units.Quantity` in units of :math:`A cm^{-2}`.
        :symbol: :math:`J_{RD}`
        """
        if self.temp.value == 0:
            current_density = units.Quantity(0, "A/cm2")
        else:
            exponent = (self.barrier / (constants.k_B * self.temp)).decompose()
            coefficient = self.richardson * self.temp**2
            current_density = coefficient * np.exp(-exponent)

        return current_density.to("A/cm2")
