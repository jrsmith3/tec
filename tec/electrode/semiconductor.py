# -*- coding: utf-8 -*-

import numpy as np
from scipy import optimize
from astropy import units, constants
from metal import Metal
from physicalproperty import PhysicalProperty, find_PhysicalProperty
from ibei import uibei


class SC(Metal):
    """
    P-type semiconductor thermoelectron electrode

    A `SC` electrode is instantiated with values to populate its public data attributes. Each argument's value must satisfy the constraints noted with the corresponding public data attribute. Arguments can be some kind of numeric type or of type `astropy.units.Quantity` so long as the units are compatible with what's listed.

    :param temp: Temperature (:math:`T`).
    :param barrier: Emission barrier (a.k.a. work function). The barrier is the difference between the vacuum energy of the surface and the Fermi energy. (:math:`\phi`)
    :param richardson: Richardson's constant (:math:`A`)
    :param electron_effective_mass: Density-of-states electron effective mass (:math:`m_{n}^{*}`).
    :param hole_effective_mass: Density-of-states hole effective mass (:math:`m_{p}^{*}`).
    :param acceptor_concentration: Acceptor dopant concentration (:math:`N_{A}`).
    :param acceptor_ionization_energy: Acceptor ionization energy relative to valence band edge (:math:`E_{A}`).
    :param bandgap: Bandgap of semiconductor at 300K (:math:`E_{g}`). Note that this quantity is expressed as
    .. math::
        E_{g} = E_{C} - E_{V}
    :param voltage: Bias voltage relative to ground (:math:`V`).
    :param position: Position (:math:`x`).
    :param emissivity: Radiative emissivity (:math:`epsilon`).
    """

    electron_effective_mass = PhysicalProperty(unit="kg", lo_bnd=0)
    hole_effective_mass = PhysicalProperty(unit="kg", lo_bnd=0)
    acceptor_concentration = PhysicalProperty(unit="1/cm3", lo_bnd=0)
    acceptor_ionization_energy = PhysicalProperty(unit="meV", lo_bnd=0)
    donor_concentration = PhysicalProperty(unit="1/cm3", lo_bnd=0)
    donor_ionization_energy = PhysicalProperty(unit="meV", lo_bnd=0)
    bandgap = PhysicalProperty(unit="eV", lo_bnd=0)

    def __init__(self, temp, barrier, richardson, bandgap, electron_effective_mass=constants.m_e, hole_effective_mass=constants.m_e, acceptor_concentration=0, acceptor_ionization_energy=0, donor_concentration=0, donor_ionization_energy=0, voltage=0, position=0, emissivity=0):
        self.temp = temp
        self.barrier = barrier
        self.richardson = richardson
        self.electron_effective_mass = electron_effective_mass
        self.hole_effective_mass = hole_effective_mass
        self.acceptor_concentration = acceptor_concentration
        self.acceptor_ionization_energy = acceptor_ionization_energy
        self.donor_concentration = donor_concentration
        self.donor_ionization_energy = donor_ionization_energy
        self.bandgap = bandgap
        self.voltage = voltage
        self.position = position
        self.emissivity = emissivity

    def cb_effective_dos(self):
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

    def vb_effective_dos(self):
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

    def electron_concentration(self):
        """
        Equlibrium conduction band electron concentration

        The equlibrium conduction band electron concentration can be expressed as

        .. math::
            n_{0} = N_{C} \exp \left( -\\frac{E_{C} - E_{F}}{kT} \\right)

        :returns: `astropy.units.Quantity` in units of :math:`cm^{-3}`
        :symbol: :math:`n_{0}`
        """
        exponent = ((self.bandgap - self.fermi_energy()) / (constants.k_B * self.temp)).decompose()

        return self.cb_effective_dos() * np.exp(-exponent)

    def hole_concentration(self):
        """
        Equlibrium valence band hole concentration

        The equlibrium valence band hole concentration can be expressed as

        .. math::
            p_{0} = N_{V} \exp \left( -\\frac{E_{F} - E_{V}}{kT} \\right)

        :returns: `astropy.units.Quantity` in units of :math:`cm^{-3}`
        :symbol: :math:`p_{0}`
        """
        exponent = (self.fermi_energy() / (constants.k_B * self.temp)).decompose()

        return self.vb_effective_dos() * np.exp(-exponent)

    def fermi_energy(self):
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

        el_carrier_conc = self.cb_effective_dos() * np.exp(-exponent_1)
        ho_carrier_conc = self.vb_effective_dos() * np.exp(-exponent_2)

        ret_val = el_carrier_conc - ho_carrier_conc + self.acceptor_concentration / (1 + 4 * np.exp(exponent_3))

        return ret_val.value

    def photon_flux(self):
        """
        Number of photons per unit time per unit area

        :returns: `astropy.units.Quantity` in units of :math:`s^{-1} cm^{-2}`.
        """
        photon_flux = self.emissivity * uibei(2, self.bandgap, self.temp, 0)
        return photon_flux.to("1/(s*cm2)")

    def photon_energy_flux(self):
        """
        Energy flux emitted by Stefan-Boltzmann radiation

        The energy flux (or power density) of Stefan-Boltzmann photons is given by

        .. math::

            j = \\frac{2 \pi^{5} k^{4}}{15 c^{2} h^{3}} T^{4}

        :returns: `astropy.units.Quantity` in units of :math:`W cm^{-2}`.
        """
        energy_flux = self.emissivity * uibei(3, self.bandgap, self.temp, 0)
        return energy_flux.to("W/cm2")
