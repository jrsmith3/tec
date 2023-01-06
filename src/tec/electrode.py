# coding: utf-8
"""
=========================
Base Library (:mod:`electrode`)
=========================

.. currentmodule:: electrode
"""

import functools

import astropy.constants
import astropy.units
import attrs
import ibei
import numpy as np


def _validate_is_scalar(instance, attribute, value):
    if not value.isscalar:
        raise TypeError("Attributes must be scalar")


def _temperature_converter(val):
    try:
        temperature = astropy.units.Quantity(val, astropy.units.K)
    except astropy.units.UnitConversionError:
        temperature = val.to(astropy.units.K, equivalencies=astropy.units.temperature())

    return temperature


@attrs.frozen
class Metal():
    """
    Planar, metal thermoelectron electrode


    Parameters
    ----------
    temperature:
        Temperature of the electrode. Corresponds to :math:`T`.
    barrier:
        Energy difference between vacuum energy of the surface and
        Fermi energy. Also known as the work function. Corresponds
        to :math:`\phi`.
    richardson:
        Richardson's constant. Corresponds to :math:`A`.
    voltage:
        Bias voltage relative to ground. Corresponds to :math:`V`.
    position:
        Location of the electrode, perpendicular to the electrode. The
        electrode is considered to be an infinite plane, so the
        system is one-dimensional. Corresponds to :math:`x`.
    emissivity:
        Radiative emissivity. Corresponds to :math:`\epsilon`.


    Attributes
    ----------
    temperature: astropy.units.Quantity[astropy.units.K]
        Same as constructor parameter.
    barrier: astropy.units.Quantity[astropy.units.eV]
        Same as constructor parameter.
    richardson: astropy.units.Quantity["A/cm2"]
        Same as constructor parameter.
    voltage: astropy.units.Quantity[astropy.units.V]
        Same as constructor parameter.
    position: astropy.units.Quantity[astropy.units.um]
        Same as constructor parameter.
    emissivity: astropy.units.Quantity[astropy.units.dimensionless_unscaled]
        Same as constructor parameter.


    Raises
    ------
    TypeError
        If non-scalar arguments are passed to the constructor.
    ValueError
        If ``temperature`` param <= 0
    ValueError
        If ``barrier`` param <= 0
    ValueError
        If ``richardson`` param <= 0
    ValueError
        If ``emissivity`` param <= 0
    ValueError
        If ``emissivity`` param > 1


    Notes
    -----
    Instance attributes of `Metal` objects are of type
    ``astropy.units.Quantity``. Computations involving units can be
    tricky, and the use of ``Quantity`` objects throughout will expose
    arithmetic implementation errors and unit conversion errors.
    """
    temperature: float | astropy.units.Quantity[astropy.units.K] = attrs.field(
        converter=_temperature_converter,
        validator=[
            _validate_is_scalar,
            attrs.validators.gt(0)
            ]
        )
    barrier: float | astropy.units.Quantity[astropy.units.eV] = attrs.field(
        converter=functools.partial(astropy.units.Quantity, unit=astropy.units.eV),
        validator=[
            _validate_is_scalar,
            attrs.validators.gt(0)
            ]
        )
    richardson: float | astropy.units.Quantity["A/(cm2 K2)"] = attrs.field(
        default=astropy.units.Quantity(120., "A/(cm2 K2)"),
        converter=functools.partial(astropy.units.Quantity, unit="A/(cm2 K2)"),
        validator=[
            _validate_is_scalar,
            attrs.validators.gt(0)
            ]
        )
    voltage: float | astropy.units.Quantity[astropy.units.V] = attrs.field(
        default=0.,
        converter=functools.partial(astropy.units.Quantity, unit=astropy.units.V),
        validator=[
            _validate_is_scalar,
            ]
        )
    position: float | astropy.units.Quantity[astropy.units.um] = attrs.field(
        default=0.,
        converter=functools.partial(astropy.units.Quantity, unit=astropy.units.um),
        validator=[
            _validate_is_scalar,
            ]
        )
    emissivity: float | astropy.units.Quantity[astropy.units.dimensionless_unscaled] = attrs.field(
        default=1.,
        converter=functools.partial(astropy.units.Quantity, unit=astropy.units.dimensionless_unscaled),
        validator=[
            _validate_is_scalar,
            attrs.validators.gt(0),
            attrs.validators.le(1),
            ]
        )


    def motive(self) -> astropy.units.Quantity[astropy.units.eV]:
        """
        Motive just outside electrode

        The motive just outside the electrode is the position of the
        vacuum energy relative to electrical ground. Corresponds to
        :math:`\psi`.
        """
        motive = self.barrier + astropy.constants.e.si * self.voltage
        return motive.to("eV")


    def thermoelectron_current_density(self) -> astropy.units.Quantity["A/cm2"]:
        """
        Thermoelectron emission current density

        This quantity is calculated according to the Richardson
        equation.

        .. math::

            J_{RD} = A T^{2} \exp \left( \\frac{\phi}{kT} \\right)

        """
        exponent = (self.barrier / (astropy.constants.k_B * self.temperature)).decompose()
        coefficient = self.richardson * self.temperature**2
        current_density = coefficient * np.exp(-exponent)

        return current_density.to("A/cm2")


    def thermoelectron_energy_flux(self) -> astropy.units.Quantity["W/cm2"]:
        """
        Energy flux emitted via thermoelectrons

        The energy flux (power density) of thermoelectrons is given by
        the following expression.

        .. math::
            J_{RD} \\frac{\phi + 2kT}{e}

        """
        kt2 = 2 * astropy.constants.k_B * self.temperature
        thermal_potential = (self.barrier + kt2) / astropy.constants.si.e
        energy_flux = thermal_potential * self.thermoelectron_current_density()

        return energy_flux.to("W/cm2")


    def photon_flux(self) -> astropy.units.Quantity["1/(cm2 s)"]:
        """
        Number of photons per unit time per unit area
        """
        photon_flux = self.emissivity * ibei.BEI(order=2, energy_bound=0, temperature=self.temperature).photon_flux()
        return photon_flux.to("1/(cm2 s)")


    def photon_energy_flux(self) -> astropy.units.Quantity["W/cm2"]:
        """
        Energy flux emitted by Stefan-Boltzmann radiation

        The energy flux (or power density) of Stefan-Boltzmann photons
        is given by the following expression.

        .. math::

            j = \\frac{2 \pi^{5} k^{4}}{15 c^{2} h^{3}} T^{4}

        """
        energy_flux = self.emissivity * ibei.BEI(order=2, energy_bound=0, temperature=self.temperature).radiant_power_flux()
        return energy_flux.to("W/cm2")


    def copy(self) -> "tec.electrode.Metal":
        """
        Copy of Metal object
        """
        return Metal(**attrs.asdict(self))
