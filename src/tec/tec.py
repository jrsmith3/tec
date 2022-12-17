# coding: utf-8
import astropy.constants
import astropy.units
import attrs
import inspect
import numpy as np
import scipy.interpolate

from .electrode import Metal


@attrs.frozen
class TEC():
    """
    Thermoelectron energy conversion device

    Instances of the `TEC` class provide additional functionality for
    computing interesting values (e.g. output power density) beyond
    the minimal functionality provided by a `Model` object.


    Parameters
    ----------
    model:
        Object implementing a particular model of a thermoelectron
        energy conversion device.


    Attributes
    ----------
    model:
        The `tec.models.Model` object used to construct the `TEC`.
    emitter:
        Emitter electrode. Exact same object as `model.emitter`.
    collector:
        Collector electrode. Exact same object as `model.collector`.
    motive:
        A spline to approximate the motive within the interelectrode
        space at an arbitrary point. Exact same object as
        `model.motive`.
    max_motive:
        Value of maximum motive. Exact same object as
        `model.max_motive`.
    max_motive_position:
        Position of maximum motive. Exact same object as
        `model.max_motive_position`.
    back_emission:
        Boolean indicating if the model considers back emission or
        not. `False` indicates back current density will always be
        zero, regardless of the collector parameters. Exact same
        object as `model.back_emission`.
    """
    model: tec.models.Ideal = attrs.field()
    emitter: tec.electrode.Metal = attrs.field(init=False)
    collector: tec.electrode.Metal = attrs.field(init=False)
    motive = attrs.field(init=False)
    max_motive = attrs.field(init=False)
    max_motive_position = attrs.field(init=False)
    back_emission = attrs.field(init=False)


    def __attrs_post_init__(self):
        self.emitter = self.model.emitter
        self.collector = self.model.collector
        self.motive = self.model.motive
        self.max_motive = self.model.max_motive
        self.max_motive_position = self.model.max_motive_position
        self.back_emission = self.model.back_emission


    # Methods returning basic data about the TEC ----------------------
    def interelectrode_spacing(self) -> astropy.units.Quantity[astropy.units.um]:
        """
        Distance between collector and emitter
        """
        return (self.collector.position - self.emitter.position).to(astropy.units.um)


    def output_voltage(self) -> astropy.units.Quantity[astropy.units.V]:
        """
        Voltage difference between collector and emitter
        """
        return (self.collector.voltage - self.emitter.voltage).to(astropy.units.V)


    def contact_potential(self) -> astropy.units.Quantity[astropy.units.V]:
        """
        Contact potential between collector and emitter

        The contact potential is defined as the difference in barrier
        height between the emitter and collector. This value should
        not be confused with the quantity returned
        by :meth:`output_voltage` which is the voltage difference
        between the collector and emitter.

        .. math::
            V_{contact} = \\frac{\psi_{E} - \psi_{C}}{e}

        """
        contact_potential = (self.emitter.barrier - self.collector.barrier) / astropy.constants.e.si

        return contact_potential.to(astropy.units.V)


    # Methods regarding current and power -----------------------------
    def forward_current_density(self) -> astropy.units.Quantity["A/cm2"]:
        """
        Net current moving from emitter to collector
        """
        diff_barrier = self.max_motive() - self.emitter.motive()

        if diff_barrier > 0:
            kT = astropy.constants.k_B * self.emitter.temp
            exponent = (diff_barrier / kT).decompose()
            scaling_factor = np.exp(-exponent)
        else:
            scaling_factor = 1.

        current_density = self.emitter.thermoelectron_current_density() * scaling_factor

        return current_density.to("A/cm2")


    def back_current_density(self) -> astropy.units.Quantity["A/cm2"]:
        """
        Net current moving from collector to emitter
        """
        diff_barrier = self.max_motive() - self.collector.motive()

        if diff_barrier > 0:
            kT = astropy.constants.k_B * self.collector.temp
            exponent = (diff_barrier / kT).decompose()
            scaling_factor = np.exp(-exponent)
        else:
            scaling_factor = 1.

        current_density = self.collector.thermoelectron_current_density() * scaling_factor

        return current_density.to("A/cm2")


    def output_current_density(self) -> astropy.units.Quantity["A/cm2"]:
        """
        Net current density flowing across device
        """
        return self.forward_current_density() - self.back_current_density()


    def output_power_density(self) -> astropy.units.Quantity["W/cm2"]:
        """
        Output power density of device
        """
        power_density = self.output_current_density() * self.output_voltage()

        return power_density.to("W/cm2")


    # Methods regarding efficiency ------------------------------------
    def carnot_efficiency(self) -> astropy.units.Quantity[astropy.units.dimensionless_unscaled]:
        """
        Carnot efficiency
        """
        efficiency = 1 - (self.collector.temperature / self.emitter.temperature)

        return efficiency.decompose().to(astropy.units.dimensionless_unscaled)


    def efficiency(self) -> astropy.units.Quantity[astropy.units.dimensionless_unscaled]:
        """
        Total thermal efficiency

        This method calculates the thermal efficiency of a TEC after
        Hatsopoulos and Gyftopoulos :cite:`97802620800590` Sec. 2.7.
        Efficiency, :math:`\eta`, is defined as the ratio of the
        output power, :math:`W_{T}`, to the rate at which heat is
        added to the device, :math:`Q_{in}`.

        .. math::
            \eta = \\frac{W_{T}}{Q_{in}}

        The law of conservation of energy determines the relationship
        between these quantities and the heat rejection
        rate, :math:`Q_{out}`

        .. math::
            Q_{in} = W_{T} + Q_{out}

        The quantities :math:`Q_{in}` and :math:`Q_{out}` are
        determined by accounting for all the flows of energy into and
        out of the system. For the purposes of calculating the
        efficiency, :math:`Q_{in}` accounts for the heat transport
        via electrons (see :meth:`electron_cooling_rate`, denoted
        by :math:`Q_{E}`) and photons
        (see :meth:`thermal_radiation_rate`, denoted by :math:`Q_
        {r}`). This efficiency calculation *does not* presently
        account for heat conducted via the leads.
        Therefore, :math:`Q_{in}` is given by

        .. math::
            Q_{in} = Q_{E} + Q_{r}

        See :meth:`heat_supply_rate` for more information about :math:`Q_{in}`.
        """
        if self.output_power_density() > 0:
            efficiency = self.output_power_density() / self.heat_supply_rate()
            efficiency = efficiency.value
        else:
            efficiency = np.nan

        output = astropy.units.Quantity(efficiency, astropy.units.dimensionless_unscaled)

        return output


    def heat_supply_rate(self) -> astropy.units.Quantity[astropy.units.W]:
        """
        Rate at which heat enters device

        The heat supply rate is the sum of all rates of heat
        transferred to the emitter. Currently this method accounts
        for heat transferred via thermoelectrons and photons, *but
        not* heat transferred through the electrical leads of the
        device.

        .. math::
            Q_{in} = Q_{E} + Q_{r}

        where :math:`Q_{E}` and :math:`Q_{r}` are calculated
        using :meth:`electron_cooling_rate`
        and :meth:`thermal_radiation_rate`, respectively.
        """
        heat_supply_rate = self.electron_cooling_rate() + self.thermal_radiation_rate()

        return heat_supply_rate.to(astropy.units.W)


    def electron_cooling_rate(self) -> astropy.units.Quantity[astropy.units.W]:
        """
        Electronic cooling rate of emitter

        This method calculates the net heat flow carried by electrons
        from the emitter according to Hatsopoulos and
        Gyftopoulos :cite:`97802620800590` Eq. 2.57a, repeated below

        .. math::
            Q_{E} = S J_{f} \\frac{\psi_{max} - \mu_{E} + 2kT_{E}}{e} - S J_{b}\\frac{\psi_{max} - \mu_{E} + 2kT_{C}}{e}

        The quantity :math:`S` is the area of the electrode, and taken
        to be unit area (1 cm^2) here.
        """
        kT_E2 = 2 * astropy.constants.k_B * self.emitter.temp
        kT_C2 = 2 * astropy.constants.k_B * self.collector.temp
        max_motive = self.max_motive() - (astropy.constants.e.si * self.emitter.voltage)

        forward = astropy.units.Unit("cm2") * self.forward_current_density() * (max_motive + kT_E2) / astropy.constants.e.si
        back = astropy.units.Unit("cm2") * self.back_current_density() * (max_motive + kT_C2) / astropy.constants.e.si

        cooling_rate = (forward - back).to("W")

        return cooling_rate


    def thermal_radiation_rate(self) -> astropy.units.Quantity[astropy.units.W]:
        """
        Interelectrode thermal radiation rate

        This method calculates the heat transfer carried across the
        interelectrode space via blackbody photons. Since the emitter
        and collector can have different values of emissivity, the
        TEC will have a net emissivity, accounted for by
        (NAME) :cite:`9780471457275` p. 793, Eq. 13.19. The thermal
        radiation rate is given by

        .. math::
            Q_{r} = \\frac{\sigma (T_{E}^{4} - T_{C}^{4})}{\\frac{1}{\epsilon_{E}} + \\frac{1}{\epsilon_{C}} - 1}

        """
        ideal_rad_rate = astropy.constants.sigma_sb * (self.emitter.temp**4 - self.collector.temp**4)

        emissivities = np.array([self.emitter.emissivity, self.collector.emissivity])
        if any(emissivities == 0):
            net_emissivity = 0
        else:
            net_emissivity = 1. / ((1. / self.emitter.emissivity) + (1. / self.collector.emissivity) - 1.)

        rad_rate = ideal_rad_rate * net_emissivity * astropy.units.Unit("cm2")

        return rad_rate.to("W")
