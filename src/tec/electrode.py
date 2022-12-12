# coding: utf-8
"""
=========================
Base Library (:mod:`electrode`)
=========================

.. currentmodule:: electrode
"""

import astropy.constants
import astropy.units
import attrs
import functools
import ibei
import itertools
import numpy as np
import scipy.optimize


def _temperature_converter(val):
    try:
        temperature = astropy.units.Quantity(val, astropy.units.K)
    except astropy.units.UnitConversionError:
        temperature = val.to(astropy.units.K, equivalencies=astropy.units.temperature())

    return temperature


@attrs.frozen
class Metal():
    """
    Metal thermoelectron electrode

    A `Metal` electrode is instantiated with values to populate its
    public data attributes. Each argument's value must satisfy the
    constraints noted with the corresponding public data attribute.
    Arguments can be some kind of numeric type or of type
    `astropy.units.Quantity` so long as the units are compatible with
    what's listed.

    Arguments in addition to the ones listed will be ignored.

    :param temp: Temperature (:math:`T`).
    :param barrier: Emission barrier (a.k.a. work function). The
      barrier is the difference between the vacuum energy of the
      surface and the Fermi energy. (:math:`\phi`)
    :param richardson: Richardson's constant (:math:`A`)
    :param voltage: Bias voltage relative to ground (:math:`V`).
    :param position: Position (:math:`x`).
    :param emissivity: Radiative emissivity (:math:`epsilon`).
    """
    temperature: float | astropy.units.Quantity[astropy.units.K] = attrs.field(
        converter=_temperature_converter,
        validator=[
            attrs.validators.gt(0)
            ]
        )
    barrier: float | astropy.units.Quantity[astropy.units.eV] = attrs.field(
        converter=functools.partial(astropy.units.Quantity, unit=astropy.units.eV),
        validator=[
            attrs.validators.gt(0)
            ]
        )
    richardson: float | astropy.units.Quantity["A/(cm2 K2)"] = attrs.field(
        converter=functools.partial(astropy.units.Quantity, unit="A/(cm2 K2)"),
        validator=[
            attrs.validators.gt(0)
            ]
        )
    voltage: float | astropy.units.Quantity[astropy.units.V] = attrs.field(
        default=0.,
        converter=functools.partial(astropy.units.Quantity, unit=astropy.units.V),
        )
    position: float | astropy.units.Quantity[astropy.units.um] = attrs.field(
        default=0.,
        converter=functools.partial(astropy.units.Quantity, unit=astropy.units.um),
        )
    emissivity: float | astropy.units.Quantity[astropy.units.dimensionless_unscaled] = attrs.field(
        default=1.,
        converter=functools.partial(astropy.units.Quantity, unit=astropy.units.dimensionless_unscaled),
        validator=[
            attrs.validators.gt(0),
            attrs.validators.le(1),
            ]
        )


    def motive(self):
        """
        Motive just outside electrode

        The motive just outside the electrode is the position of the
        vacuum energy relative to electrical ground.

        :returns: `astropy.units.Quantity` in units of :math:`eV`.
        :symbol: :math:`\psi_{E}` (for the emitter, for example)
        """
        motive = self.barrier + astropy.constants.e.si * self.voltage
        return motive.to("eV")


    def thermoelectron_current_density(self):
        """
        Thermoelectron emission current density

        This quantity is calculated according to the Richardson
        equation

        .. math::

            J_{RD} = A T^{2} \exp \left( \\frac{\phi}{kT} \\right)

        If either the `temp` or `richardson` attributes are equal to
        0, this  method returns a value of 0.

        :returns: `astropy.units.Quantity` in units of :math:`A cm^{-2}`.
        :symbol: :math:`J_{RD}`
        """
        if self.temp.value == 0:
            current_density = astropy.units.Quantity(0, "A/cm2")
        else:
            exponent = (self.barrier / (astropy.constants.k_B * self.temp)).decompose()
            coefficient = self.richardson * self.temp**2
            current_density = coefficient * np.exp(-exponent)

        return current_density.to("A/cm2")


    def thermoelectron_energy_flux(self):
        """
        Energy flux emitted via thermoelectrons

        The energy flux (power density) of thermoelectrons is given by

        .. math::
            J_{RD} \\frac{\phi + 2kT}{e}

        :returns: `astropy.units.Quantity` in units of
          :math:`W cm^{-2}`.
        :symbol: None
        """
        kt2 = 2 * astropy.constants.k_B * self.temp
        thermal_potential = (self.barrier + kt2) / astropy.constants.e.to("C")
        energy_flux = thermal_potential * self.thermoelectron_current_density()

        return energy_flux.to("W/cm2")


    def photon_flux(self):
        """
        Number of photons per unit time per unit area

        :returns: `astropy.units.Quantity` in units of
          :math:`s^{-1} cm^{-2}`.
        """
        photon_flux = self.emissivity * ibei.uibei(2, 0, self.temp, 0)
        return photon_flux.to("1/(s*cm2)")


    def photon_energy_flux(self):
        """
        Energy flux emitted by Stefan-Boltzmann radiation

        The energy flux (or power density) of Stefan-Boltzmann photons
        is given by

        .. math::

            j = \\frac{2 \pi^{5} k^{4}}{15 c^{2} h^{3}} T^{4}

        :returns: `astropy.units.Quantity` in units of
          :math:`W cm^{-2}`.
        """
        energy_flux = self.emissivity * ibei.uibei(3, 0, self.temp, 0)
        return energy_flux.to("W/cm2")


@attrs.frozen
class SC():
    """
    P-type semiconductor thermoelectron electrode

    A `SC` electrode is instantiated with values to populate its
    public data attributes. Each argument's value must satisfy the
    constraints noted with the corresponding public data attribute.
    Arguments can be some kind of numeric type or of type
    `astropy.units.Quantity` so long as the units are compatible with
    what's listed.

    Arguments in addition to the ones listed will be ignored.

    :param temp: Temperature (:math:`T`).
    :param barrier: Emission barrier (a.k.a. work function). The
      barrier is the difference between the vacuum energy of the
      surface and the Fermi energy. (:math:`\phi`)
    :param richardson: Richardson's constant (:math:`A`)
    :param electron_effective_mass: Density-of-states electron
      effective mass (:math:`m_{n}^{*}`).
    :param hole_effective_mass: Density-of-states hole effective mass
      (:math:`m_{p}^{*}`).
    :param acceptor_concentration: Acceptor dopant concentration
      (:math:`N_{A}`).
    :param acceptor_ionization_energy: Acceptor ionization energy
      relative to valence band edge (:math:`E_{A}`).
    :param bandgap: Bandgap of semiconductor at 300K
      (:math:`E_{g}`). Note that this quantity is expressed as
      .. math::
          E_{g} = E_{C} - E_{V}
    :param voltage: Bias voltage relative to ground (:math:`V`).
    :param position: Position (:math:`x`).
    :param emissivity: Radiative emissivity (:math:`epsilon`).
    """
    electron_effective_mass: float | astropy.units.Quantity[astropy.units.kg] = attrs.field()
    hole_effective_mass: float | astropy.units.Quantity[astropy.units.kg] = attrs.field()
    acceptor_concentration: float | astropy.units.Quantity["1/cm3"] = attrs.field()
    acceptor_ionization_energy: float | astropy.units.Quantity[astropy.units.meV] = attrs.field()
    donor_concentration: float | astropy.units.Quantity["1/cm3"] = attrs.field()
    donor_ionization_energy: float | astropy.units.Quantity[astropy.units.meV] = attrs.field()
    bandgap: float | astropy.units.Quantity[astropy.units.eV] = attrs.field()


    def __init__(self, temp, barrier, richardson, bandgap, electron_effective_mass=astropy.constants.m_e, hole_effective_mass=astropy.constants.m_e, acceptor_concentration=0, acceptor_ionization_energy=0, donor_concentration=0, donor_ionization_energy=0, voltage=0, position=0, emissivity=0, **kwargs):
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

        According to Streetman and Banerjee :cite:`9780130255389`, the
        conduction band effective density of states can be expressed
        as

        .. math::
            N_{C} = 2 \left( \\frac{2 \pi m_{n}^{*}kT}{h^{2}} \\right)^{3/2}

        :returns: `astropy.units.Quantity` in units of :math:`cm^{-3}`
        :symbol: :math:`N_{C}`
        """
        dos = 2 * ((2 * np.pi * self.electron_effective_mass * astropy.constants.k_B * self.temp) / (astropy.constants.h ** 2))**(3. / 2)

        return dos.to("1/cm3")

    def vb_effective_dos(self):
        """
        Valence band effective density of states

        According to Streetman and Banerjee :cite:`9780130255389`, the
        valence band effective density of states can be expressed as

        .. math::
            N_{V} = 2 \left( \\frac{2 \pi m_{p}^{*}kT}{h^{2}} \\right)^{3/2}

        :returns: `astropy.units.Quantity` in units of :math:`cm^{-3}`
        :symbol: :math:`N_{V}`
        """
        dos = 2 * ((2 * np.pi * self.hole_effective_mass * astropy.constants.k_B * self.temp) / (astropy.constants.h ** 2))**(3. / 2)

        return dos.to("1/cm3")

    def electron_concentration(self):
        """
        Equlibrium conduction band electron concentration

        The equlibrium conduction band electron concentration can be
        expressed as

        .. math::
            n_{0} = N_{C} \exp \left( -\\frac{E_{C} - E_{F}}{kT} \\right)

        :returns: `astropy.units.Quantity` in units of :math:`cm^{-3}`
        :symbol: :math:`n_{0}`
        """
        exponent = ((self.bandgap - self.fermi_energy()) / (astropy.constants.k_B * self.temp)).decompose()

        return self.cb_effective_dos() * np.exp(-exponent)

    def hole_concentration(self):
        """
        Equlibrium valence band hole concentration

        The equlibrium valence band hole concentration can be
        expressed as

        .. math::
            p_{0} = N_{V} \exp \left( -\\frac{E_{F} - E_{V}}{kT} \\right)

        :returns: `astropy.units.Quantity` in units of :math:`cm^{-3}`
        :symbol: :math:`p_{0}`
        """
        exponent = (self.fermi_energy() / (astropy.constants.k_B * self.temp)).decompose()

        return self.vb_effective_dos() * np.exp(-exponent)

    def fermi_energy(self):
        """
        Value of Fermi energy relative to valence band maximum

        The Fermi energy is calculated by solving the charge
        neutrality condition

        .. math::
            n_{0} + N_{A}^{-} = p_{0} + N_{D}^{+}

        Expanding and moving the terms to the same side, this method
        solves for :math:`E_{F}` in the following equation:

        .. math::
            0 = N_{C} \exp \left( -\\frac{E_{C} - E_{F}}{kT} \\right) -
            N_{V} \exp \left( -\\frac{E_{F} - E_{V}}{kT} \\right) +
            N_{A} \left( 1 + g_{A} \exp \left( \\frac{E_{A} - E_{F}}{kT} \\right) \\right)^{-1} -
            N_{D} \left( 1 + g_{D} \exp \left( \\frac{E_{F} - E_{D}}{kT} \\right) \\right)^{-1}


        Strictly speaking, this method returns the difference between
        the Fermi energy and the valence band maximum:

        .. math::
            E_{F} - E_{V}

        :returns: `astropy.units.Quantity` in units of :math:`eV`
        :symbol: :math:`E_{F}`
        """
        lo = 0
        hi = self.bandgap.value

        fermi_energy = scipy.optimize.brentq(self._charge_neutrality_target_fcn, lo, hi)

        return astropy.units.Quantity(fermi_energy, "eV")

    def _charge_neutrality_target_fcn(self, fermi_energy):
        """
        Target function of charge neutrality condition.
        """
        fermi_energy = astropy.units.Quantity(fermi_energy, "eV")

        exponent_1 = ((self.bandgap - fermi_energy) / (astropy.constants.k_B * self.temp)).decompose()
        exponent_2 = (fermi_energy / (astropy.constants.k_B * self.temp)).decompose()
        exponent_3 = ((self.acceptor_ionization_energy - fermi_energy) / (astropy.constants.k_B * self.temp)).decompose()

        el_carrier_conc = self.cb_effective_dos() * np.exp(-exponent_1)
        ho_carrier_conc = self.vb_effective_dos() * np.exp(-exponent_2)

        ret_val = el_carrier_conc - ho_carrier_conc + self.acceptor_concentration / (1 + 4 * np.exp(exponent_3))

        return ret_val.value

    def photon_flux(self):
        """
        Number of photons per unit time per unit area

        :returns: `astropy.units.Quantity` in units of
          :math:`s^{-1} cm^{-2}`.
        """
        photon_flux = self.emissivity * ibei.uibei(2, self.bandgap, self.temp, 0)
        return photon_flux.to("1/(s*cm2)")

    def photon_energy_flux(self):
        """
        Energy flux emitted by Stefan-Boltzmann radiation

        The energy flux (or power density) of Stefan-Boltzmann photons
        is given by

        .. math::

            j = \\frac{2 \pi^{5} k^{4}}{15 c^{2} h^{3}} T^{4}

        :returns: `astropy.units.Quantity` in units of
          :math:`W cm^{-2}`.
        """
        energy_flux = self.emissivity * ibei.uibei(3, self.bandgap, self.temp, 0)
        return energy_flux.to("W/cm2")
