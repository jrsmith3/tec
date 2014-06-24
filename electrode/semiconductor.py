# -*- coding: utf-8 -*-
from weakref import WeakKeyDictionary
import constants
import numpy as np
from scipy import optimize
from astropy import units
from electrode import Electrode
from physicalproperty import PhysicalProperty, find_PhysicalProperty

class Semiconductor(object):
    """
    Implements basic semiconductor calculations for p-type Si.
    """

    temp = PhysicalProperty(unit = "K", lo_bnd = 0)
    """
    Temperature of material >0 [K].
    """

    el_effective_mass = PhysicalProperty(unit = "kg", lo_bnd = 0)
    """
    Effective mass of electrons >0 [kg].
    """

    ho_effective_mass = PhysicalProperty(unit = "kg", lo_bnd = 0)
    """
    Effective mass of holes >0 [kg].
    """

    accept_conc = PhysicalProperty(unit = "1/cm3", lo_bnd = 0)
    """
    Acceptor dopant concentration >0 [cm^{-3}]
    """

    accept_ionization_energy = PhysicalProperty(unit = "meV", lo_bnd = 0)
    """
    Acceptor dopant ionization energy >0 [eV]
    """

    bandgap = PhysicalProperty(unit = "eV", lo_bnd = 0)
    """
    Bandgap of semiconductor at 300K. >0 [eV].
    """

    def __init__(self, params):
        for attr in find_PhysicalProperty(self):
            setattr(self, attr, params[attr])

    def calc_cond_band_effective_dos(self):
        """
        Effective density of states in conduction band in [cm^-3].
        """
        dos = 2 * \
            ((2 * np.pi * self.el_effective_mass * constants.k * self.temp) / \
            (constants.h ** 2))**(3./2)

        return dos.to("1/cm3")

    def calc_val_band_effective_dos(self):
        """
        Effective density of states in conduction band in [cm^-3].
        """
        dos = 2 * \
            ((2 * np.pi * self.ho_effective_mass * constants.k * self.temp) / \
            (constants.h ** 2))**(3./2)

        return dos.to("1/cm3")

    def calc_el_carrier_conc(self):
        """
        Equilibrium electron carrier concentration in [cm^-3].
        """
        exponent = ((self.bandgap - self.calc_fermi_energy()) / \
            (constants.k * self.temp)).decompose()

        return self.calc_cond_band_effective_dos() * np.exp(-exponent)

    def calc_ho_carrier_conc(self):
        """
        Equilibrium hole carrier concentration in [cm^-3].
        """
        exponent = (self.calc_fermi_energy() / \
            (constants.k * self.temp)).decompose()

        return self.calc_val_band_effective_dos() * np.exp(-exponent)

    def calc_fermi_energy(self):
        """
        Value of Fermi energy relative to valence band max in [eV].
        """
        lo = 0
        hi = self.bandgap.value

        fermi_energy = optimize.brentq(self._charge_neutrality_target_fcn, lo, hi)

        return units.Quantity(fermi_energy, "eV")

    def _charge_neutrality_target_fcn(self, fermi_energy):
        """
        Target function of charge neutrality condition.
        """
        fermi_energy = units.Quantity(fermi_energy, "eV")

        exponent_1 = ((self.bandgap - fermi_energy) / \
            (constants.k * self.temp)).decompose()
        exponent_2 = (fermi_energy / (constants.k * self.temp)).decompose()
        exponent_3 = ((self.accept_ionization_energy - fermi_energy) / \
            (constants.k * self.temp)).decompose()

        el_carrier_conc = self.calc_cond_band_effective_dos() * np.exp(-exponent_1)
        ho_carrier_conc = self.calc_val_band_effective_dos() * np.exp(-exponent_2)

        ret_val =  el_carrier_conc - ho_carrier_conc + \
            self.accept_conc / (1 + 4 * np.exp(exponent_3))

        return ret_val.value
