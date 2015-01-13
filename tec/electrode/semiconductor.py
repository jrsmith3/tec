# -*- coding: utf-8 -*-

import numpy as np
from scipy import optimize
from astropy import units
from astropy import constants
from metal import Metal
from physicalproperty import PhysicalProperty, find_PhysicalProperty


class SC(Metal):
    """
    P-type semiconductor thermoelectron electrode
    """

    electron_effective_mass = PhysicalProperty(unit="kg", lo_bnd=0)
    """
    Density-of-states electron effective mass

    :symbol: :math:`m_{n}^{*}`
    """

    hole_effective_mass = PhysicalProperty(unit="kg", lo_bnd=0)
    """
    Density-of-states hole effective mass

    :symbol: :math:`m_{p}^{*}`
    """

    acceptor_concentration = PhysicalProperty(unit="1/cm3", lo_bnd=0)
    """
    Acceptor dopant concentration

    :symbol: :math:`N_{A}`
    """

    acceptor_ionization_energy = PhysicalProperty(unit="meV", lo_bnd=0)
    """
    Acceptor ionization energy relative to valence band edge

    :symbol: :math:`E_{A}`
    """

    bandgap = PhysicalProperty(unit="eV", lo_bnd=0)
    """
    Bandgap of semiconductor at 300K

    .. math::
        E_{g} = E_{C} - E_{V}

    :symbol: :math:`E_{g}`
    """

    def __init__(self, params):
        for attr in find_PhysicalProperty(self):
            setattr(self, attr, params[attr])

    def calc_cb_effective_dos(self):
        """
        Conduction band effective density of states

        According to Streetman and Banerjee :cite:`9780130255389`, the conduction band effective density of states can be expressed as

        .. math::
            N_{C} = 2 \left( \\frac{2 \pi m_{n}^{*}kT}{h^{2}} \\right)^{3/2}

        :returns: `astropy.units.Quantity` in units of :math:`cm^{-3}`
        :symbol: :math:`N_{C}`
        """
        dos = 2 * ((2 * np.pi * self.electron_effective_mass * constants.k_B * self.temp) / (constants.h ** 2))**(3./2)

        return dos.to("1/cm3")

    def calc_vb_effective_dos(self):
        """
        Valence band effective density of states

        According to Streetman and Banerjee :cite:`9780130255389`, the valence band effective density of states can be expressed as

        .. math::
            N_{V} = 2 \left( \\frac{2 \pi m_{p}^{*}kT}{h^{2}} \\right)^{3/2}

        :returns: `astropy.units.Quantity` in units of :math:`cm^{-3}`
        :symbol: :math:`N_{V}`
        """
        dos = 2 * ((2 * np.pi * self.hole_effective_mass * constants.k_B * self.temp) / (constants.h ** 2))**(3./2)

        return dos.to("1/cm3")

    def calc_electron_concentration(self):
        """
        Equlibrium conduction band electron concentration

        The equlibrium conduction band electron concentration can be expressed as

        .. math::
            n_{0} = N_{C} \exp \left( -\\frac{E_{C} - E_{F}}{kT} \\right)

        :returns: `astropy.units.Quantity` in units of :math:`cm^{-3}`
        :symbol: :math:`n_{0}`
        """
        exponent = ((self.bandgap - self.calc_fermi_energy()) / (constants.k_B * self.temp)).decompose()

        return self.calc_cb_effective_dos() * np.exp(-exponent)

    def calc_hole_concentration(self):
        """
        Equlibrium valence band hole concentration

        The equlibrium valence band hole concentration can be expressed as

        .. math::
            p_{0} = N_{V} \exp \left( -\\frac{E_{F} - E_{V}}{kT} \\right)

        :returns: `astropy.units.Quantity` in units of :math:`cm^{-3}`
        :symbol: :math:`p_{0}`
        """
        exponent = (self.calc_fermi_energy() / (constants.k_B * self.temp)).decompose()

        return self.calc_vb_effective_dos() * np.exp(-exponent)

    def calc_fermi_energy(self):
        """
        Value of Fermi energy relative to valence band maximum

        The Fermi energy is calculated by solving the charge neutrality condition

        .. math::
            n_{0} + N_{A}^{-} = p_{0} + N_{D}^{+}

        Expanding and moving the terms to the same side, this method solves for :math:`E_{F}` in the following equation:

        .. math::
            0 = N_{C} \exp \left( -\\frac{E_{C} - E_{F}}{kT} \\right) - N_{V} \exp \left( -\\frac{E_{F} - E_{V}}{kT} \\right) + N_{A} \left( 1 + g_{A} \exp \left( \\frac{E_{A} - E_{F}}{kT} \\right) \\right)^{-1} - N_{D} \left( 1 + g_{D} \exp \left( \\frac{E_{F} - E_{D}}{kT} \\right) \\right)^{-1}


        Strictly speaking, this method returns the difference between the Fermi energy and the valence band maximum:

        .. math::
            E_{F} - E_{V}

        :returns: `astropy.units.Quantity` in units of :math:`eV`
        :symbol: :math:`E_{F}`
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

        exponent_1 = ((self.bandgap - fermi_energy) / (constants.k_B * self.temp)).decompose()
        exponent_2 = (fermi_energy / (constants.k_B * self.temp)).decompose()
        exponent_3 = ((self.acceptor_ionization_energy - fermi_energy) / (constants.k_B * self.temp)).decompose()

        el_carrier_conc = self.calc_cb_effective_dos() * np.exp(-exponent_1)
        ho_carrier_conc = self.calc_vb_effective_dos() * np.exp(-exponent_2)

        ret_val = el_carrier_conc - ho_carrier_conc + self.acceptor_concentration / (1 + 4 * np.exp(exponent_3))

        return ret_val.value
