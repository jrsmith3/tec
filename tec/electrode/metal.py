# -*- coding: utf-8 -*-

import itertools
import numpy as np
from astropy import units, constants
from physicalproperty import PhysicalProperty, find_PhysicalProperty
from ibei import uibei
import tec


class Metal(object):
    """
    Metal thermoelectron electrode

    A `Metal` electrode is instantiated with values to populate its public data attributes. Each argument's value must satisfy the constraints noted with the corresponding public data attribute. Arguments can be some kind of numeric type or of type `astropy.units.Quantity` so long as the units are compatible with what's listed.

    :param temp: Temperature (:math:`T`).
    :param barrier: Emission barrier (a.k.a. work function). The barrier is the difference between the vacuum energy of the surface and the Fermi energy. (:math:`\phi`)
    :param richardson: Richardson's constant (:math:`A`)
    :param voltage: Bias voltage relative to ground (:math:`V`).
    :param position: Position (:math:`x`).
    :param emissivity: Radiative emissivity (:math:`epsilon`).
    """

    temp = PhysicalProperty(unit="K", lo_bnd=0)
    barrier = PhysicalProperty(unit="eV", lo_bnd=0)
    richardson = PhysicalProperty(unit="A/(cm2 K2)", lo_bnd=0)
    voltage = PhysicalProperty(unit="V")
    position = PhysicalProperty(unit="um")
    emissivity = PhysicalProperty(lo_bnd=0, up_bnd=1)

    def __init__(self, temp, barrier, richardson=120, voltage=0, position=0, emissivity=0):
        self.temp = temp
        self.barrier = barrier
        self.richardson = richardson
        self.voltage = voltage
        self.position = position
        self.emissivity = emissivity

    def __iter__(self):
        """
        Implement iterator functionality

        This iterator functionality returns tuples such that the data contained in the object can be converted into a dictionary. All `PhysicalProperty` attributes appear once and only once during the iteration. The order of these atttibutes are not guaranteed. Additionally, this iteration returns the following two attributes:

        * `__class__`: The object's class returned by `type(self)`.
        * `__version__`: The __version__ of the `tec` module that was used.
        """
        # Crappy implmentation -- should use iterators/iterables.
        # Construct a list of tuples to return.
        physical_prop_names = find_PhysicalProperty(self)
        physical_prop_vals = [getattr(self, prop) for prop in physical_prop_names]

        attribs = zip(physical_prop_names, physical_prop_vals)

        ext_attribs = [("__class__", type(self),),
            ("__version__", tec.__version__)]

        return itertools.chain(ext_attribs, attribs)

    def __repr__(self):
        return str(self._to_dict())

    def motive(self):
        """
        Motive just outside electrode

        The motive just outside the electrode is the position of the vacuum energy relative to electrical ground.

        :returns: `astropy.units.Quantity` in units of :math:`eV`.
        :symbol: :math:`\psi_{E}` (for the emitter, for example)
        """
        motive = self.barrier + constants.e.si * self.voltage
        return motive.to("eV")

    def thermoelectron_current_density(self):
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

    def thermoelectron_energy_flux(self):
        """
        Energy flux emitted via thermoelectrons

        The energy flux (power density) of thermoelectrons is given by 

        .. math::
            J_{RD} \\frac{\phi + 2kT}{e}

        :returns: `astropy.units.Quantity` in units of :math:`W cm^{-2}`.
        :symbol: None
        """
        kt2 = 2 * constants.k_B * self.temp
        thermal_potential = (self.barrier + kt2)/constants.e.to("C")
        energy_flux = thermal_potential * self.thermoelectron_current_density()

        return energy_flux.to("W/cm2")        

    def photon_flux(self):
        """
        Number of photons per unit time per unit area

        :returns: `astropy.units.Quantity` in units of :math:`s^{-1} cm^{-2}`.
        """
        photon_flux = self.emissivity * uibei(2, 0, self.temp, 0)
        return photon_flux.to("1/(s*cm2)")

    def photon_energy_flux(self):
        """
        Energy flux emitted by Stefan-Boltzmann radiation

        The energy flux (or power density) of Stefan-Boltzmann photons is given by

        .. math::

            j = \\frac{2 \pi^{5} k^{4}}{15 c^{2} h^{3}} T^{4}

        :returns: `astropy.units.Quantity` in units of :math:`W cm^{-2}`.
        """
        energy_flux = self.emissivity * uibei(3, 0, self.temp, 0)
        return energy_flux.to("W/cm2")
