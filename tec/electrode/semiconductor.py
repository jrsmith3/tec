# -*- coding: utf-8 -*-

import numpy as np
from scipy import optimize
from astropy import units
from astropy import constants
from metal import Metal
from tec import PhysicalProperty, find_PhysicalProperty

class SC(Metal):
    """
    Implements basic semiconductor calculations for p-type Si.
    """

    electron_effective_mass = PhysicalProperty(unit = "kg", lo_bnd = 0)
    """
    Effective mass of electrons

    Symbol: :math:`m_{n}^{*}`
    """

    hole_effective_mass = PhysicalProperty(unit = "kg", lo_bnd = 0)
    """
    Effective mass of holes

    Symbol: :math:`m_{p}^{*}`
    """

    acceptor_concentration = PhysicalProperty(unit = "1/cm3", lo_bnd = 0)
    """
    Acceptor dopant concentration

    Symbol: :math:`N_{A}`
    """

    acceptor_ionization_energy = PhysicalProperty(unit = "meV", lo_bnd = 0)
    """
    Acceptor dopant ionization energy

    Symbol: :math:`E_{A}`
    """

    bandgap = PhysicalProperty(unit = "eV", lo_bnd = 0)
    """
    Bandgap of semiconductor at 300K

    Symbol: :math:`E_{g}`
    """

    def __init__(self, params):
        for attr in find_PhysicalProperty(self):
            setattr(self, attr, params[attr])

    def calc_cb_effective_dos(self):
        """
        Effective density of states in conduction band

        :returns: `astropy.units.Quantity` in units of :math:`cm^{-3}`
        """
        dos = 2 * \
            ((2 * np.pi * self.electron_effective_mass * constants.k_B * self.temp) / \
            (constants.h ** 2))**(3./2)

        return dos.to("1/cm3")

    def calc_vb_effective_dos(self):
        """
        Effective density of states in valence band

        :returns: `astropy.units.Quantity` in units of :math:`cm^{-3}`
        """
        dos = 2 * \
            ((2 * np.pi * self.hole_effective_mass * constants.k_B * self.temp) / \
            (constants.h ** 2))**(3./2)

        return dos.to("1/cm3")

    def calc_electron_concentration(self):
        """
        Equilibrium electron carrier concentration

        :returns: `astropy.units.Quantity` in units of :math:`cm^{-3}`

        Symbol: :math:`n_{0}`
        """
        exponent = ((self.bandgap - self.calc_fermi_energy()) / \
            (constants.k_B * self.temp)).decompose()

        return self.calc_cb_effective_dos() * np.exp(-exponent)

    def calc_hole_concentration(self):
        """
        Equilibrium hole carrier concentration

        :returns: `astropy.units.Quantity` in units of :math:`cm^{-3}`

        Symbol: :math:`p_{0}`
        """
        exponent = (self.calc_fermi_energy() / \
            (constants.k_B * self.temp)).decompose()

        return self.calc_vb_effective_dos() * np.exp(-exponent)

    def calc_fermi_energy(self):
        """
        Value of Fermi energy relative to valence band maximum

        :returns: `astropy.units.Quantity` in units of :math:`eV`

        Symbol: :math:`E_{F}`
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
            (constants.k_B * self.temp)).decompose()
        exponent_2 = (fermi_energy / (constants.k_B * self.temp)).decompose()
        exponent_3 = ((self.acceptor_ionization_energy - fermi_energy) / \
            (constants.k_B * self.temp)).decompose()

        el_carrier_conc = self.calc_cb_effective_dos() * np.exp(-exponent_1)
        ho_carrier_conc = self.calc_vb_effective_dos() * np.exp(-exponent_2)

        ret_val =  el_carrier_conc - ho_carrier_conc + \
            self.acceptor_concentration / (1 + 4 * np.exp(exponent_3))

        return ret_val.value
