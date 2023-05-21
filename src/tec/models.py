# coding: utf-8
import astropy.constants
import astropy.units
import attrs
import numpy as np
import numpy.typing
import scipy.integrate
import scipy.interpolate
import scipy.optimize
import scipy.special

from . import electrode, tec


def _emitter_temperature_gt_collector_temperature(model):
    if model.emitter.temperature <= model.collector.temperature:
        raise ValueError("Emitter temperature must be greater than collector temperature")


def _emitter_barrier_gt_collector_barrier(model):
    if model.emitter.barrier <= model.collector.barrier:
        raise ValueError("Emitter barrier must be greater than collector barrier")


def _emitter_position_lt_collector_position(model):
    if model.emitter.position >= model.collector.position:
        raise ValueError("Emitter position must be greater than collector position")


def _check_default_model_constraints(model):
    """
    Convenience function to call the default constraints
    """
    _emitter_temperature_gt_collector_temperature(model)
    _emitter_barrier_gt_collector_barrier(model)
    _emitter_position_lt_collector_position(model)


@attrs.frozen
class Ideal():
    """
    Model of ideal performance TEC

    This class implements a model of electron transport which
    completely ignores the negative space charge effect, similar to
    the model described on p. 51 of :cite:`9780262080590`.


    Parameters
    ----------
    emitter:
        Emitter electrode.
    collector:
        Collector electrode.
    back_emission:
        If `False`, the TEC's back current density will equal
        zero, regardless of the collector parameters.


    Attributes
    ----------
    emitter:
        Same as constructor parameter.
    collector:
        Same as constructor parameter.
    back_emission:
        Same as constructor parameter.
    motive:
        A spline to approximate the motive within the interelectrode
        space at an arbitrary point.
    """
    emitter: electrode.Metal = attrs.field(
        converter = lambda x: x.copy()
        )
    collector: electrode.Metal = attrs.field(
        converter = lambda x: x.copy()
        )
    back_emission: bool = attrs.field(default=False)
    motive: scipy.interpolate.UnivariateSpline = attrs.field(init=False)


    def __attrs_post_init__(self):
        # Check constraints.
        _check_default_model_constraints(self)

        # Construct motive spline.
        abscissae = astropy.units.Quantity([self.emitter.position, self.collector.position], "um")
        ordinates = astropy.units.Quantity([self.emitter.motive(), self.collector.motive()], "eV")

        spl = scipy.interpolate.UnivariateSpline(abscissae, ordinates, k=1, ext="raise")

        object.__setattr__(self, "motive", spl)


    @classmethod
    def from_args(
            cls,
            emitter_temperature: float | astropy.units.Quantity[astropy.units.K],
            emitter_barrier: float | astropy.units.Quantity[astropy.units.eV],
            collector_temperature: float | astropy.units.Quantity[astropy.units.K],
            collector_barrier: float | astropy.units.Quantity[astropy.units.eV],
            collector_voltage: float | astropy.units.Quantity[astropy.units.V],
            collector_position: float | astropy.units.Quantity[astropy.units.um],
            emitter_voltage: float | astropy.units.Quantity[astropy.units.V]=0.,
            emitter_position: float | astropy.units.Quantity[astropy.units.um]=0.,
            emitter_emissivity: float | astropy.units.Quantity[astropy.units.dimensionless_unscaled]=1.,
            emitter_richardson: float | astropy.units.Quantity["A/(cm2 K2)"]=astropy.units.Quantity(120., "A/(cm2 K2)"),
            collector_emissivity: float | astropy.units.Quantity[astropy.units.dimensionless_unscaled]=1.,
            collector_richardson: float | astropy.units.Quantity["A/(cm2 K2)"]=astropy.units.Quantity(120., "A/(cm2 K2)"),
            back_emission=False,
        ) -> "tec.TEC":
        """
        Create TEC from individual arguments using this model


        Parameters
        ----------
        emitter_temperature:
            Temperature of emitter electrode.
        emitter_barrier:
            Barrier of emitter electrode.
        emitter_richardson:
            Richardson's constant of emitter electrode.
        emitter_voltage:
            Bias voltage of emitter electrode.
        emitter_position:
            Location of emitter electrode.
        emitter_emissivity:
            Radiative emissivity of emitter electrode.
        collector_temperature:
            Temperature of collector electrode.
        collector_barrier:
            Barrier of collector electrode.
        collector_richardson:
            Richardson's constant of collector electrode.
        collector_voltage:
            Bias voltage of collector electrode.
        collector_position:
            Location of collector electrode.
        collector_emissivity:
            Radiative emissivity of collector electrode.
        kwargs:
            Additional arguments passed to the constructor of this
            class.


        See also
        --------
        tec.electrode.Metal: For more details on the arguments used to
            construct the `emitter` and `collector` attributes.


        Notes
        -----
        The order of the arguments to this method is wonky; it would
        be better to list all of the emitter arguments, then list the
        collector arguments. It was impossible to achieve a sensible
        ordering *and* set sensible default values, so I decided the
        default values were more important because they are
        convenient.
        """
        emitter = electrode.Metal(
                temperature = emitter_temperature,
                barrier = emitter_barrier,
                richardson = emitter_richardson,
                voltage = emitter_voltage,
                position = emitter_position,
                emissivity = emitter_emissivity,
            )

        collector = electrode.Metal(
                temperature = collector_temperature,
                barrier = collector_barrier,
                richardson = collector_richardson,
                voltage = collector_voltage,
                position = collector_position,
                emissivity = collector_emissivity,
            )

        ideal_model = cls(emitter, collector, back_emission=back_emission)

        return tec.TEC(model=ideal_model)


    @property
    def max_motive(self) -> astropy.units.Quantity[astropy.units.eV]:
        """
        Value of maximum motive
        """
        max_motive = max(self.emitter.motive(), self.collector.motive())

        return max_motive


    @property
    def max_motive_position(self) -> astropy.units.Quantity[astropy.units.eV]:
        """
        Position of maximum motive
        """
        if self.emitter.motive() > self.collector.motive():
            max_motive_position = self.emitter.position
        else:
            max_motive_position = self.collector.position

        return max_motive_position


    def copy(self) -> "tec.models.Ideal":
        """
        Copy of `Ideal` object
        """
        args = attrs.asdict(self, recurse=False)
        del args["motive"]
        return Ideal(**args)


@attrs.frozen
class Langmuir():
    """
    Vacuum TEC with metal electrodes, space charge, no back emission

    This class implements a model of electron transport in a vacuum
    TEC with metal electrodes that accounts for the negative space
    charge effect and ignores back emission. The model was first
    described by Langmuir :cite:`10.1103/PhysRev.21.419`.


    Parameters
    ----------
    emitter:
        Emitter electrode.
    collector:
        Collector electrode.


    Attributes
    ----------
    emitter:
        Same as constructor parameter.
    collector:
        Same as constructor parameter.
    back_emission:
        Indicates the presence of back emission in the model. Always
        `False`.
    motive:
        A spline to approximate the motive within the interelectrode
        space at an arbitrary point.
    max_motive:
        Value of maximum motive. Corresponds to the
        quantity :math:`\psi_{m}` in :cite:`9780262080606` section
        10.3.1.
    max_motive_position:
        Position of maximum motive within the interelectrode space.


    Raises
    ------
    ValueError
        If a position outside the interelectrode space is passed to
        the `motive` method.
    """
    emitter: electrode.Metal = attrs.field(
        converter = lambda x: x.copy()
        )
    collector: electrode.Metal = attrs.field(
        converter = lambda x: x.copy()
        )
    back_emission: bool = attrs.field(default=False, init=False)
    motive: scipy.interpolate.UnivariateSpline = attrs.field(init=False)

    # Fix
    dimensionless_motive_vs_distance_rhs: scipy.interpolate.UnivariateSpline = attrs.field(init=False)
    dimensionless_distance_vs_motive_lhs: scipy.interpolate.UnivariateSpline = attrs.field(init=False)


    def __attrs_post_init__(self):
        # Check constraints.
        _check_default_model_constraints(self)

        # Construct motive.
        #
        # The following code is here as an example. It will need to be
        # heavily rewritten once the overall structure begins to
        # stabilize.

        initial_conditions = np.array([0, 0])

        # I need to parameterize the following calls.
        num_points = 10_000

        lhs_endpoint = -2.5538
        lhs_positions = np.linspace(0, lhs_endpoint, num_points)
        lhs_motives = scipy.integrate.odeint(self._langmuirs_dimensionless_poisson_eq, initial_conditions, lhs_positions)
        lhs_positions_vs_motives = np.array([lhs_positions, lhs_motives[:,0]])

        dimensionless_distance_vs_motive_lhs = scipy.interpolate.UnivariateSpline(lhs_motives[:,0], lhs_positions, k=1, ext="const")

        object.__setattr__(self, "dimensionless_distance_vs_motive_lhs", dimensionless_distance_vs_motive_lhs)


        rhs_endpoint = 100.
        rhs_positions = np.linspace(0, rhs_endpoint, num_points)
        rhs_motives = scipy.integrate.odeint(self._langmuirs_dimensionless_poisson_eq, initial_conditions, rhs_positions)
        rhs_positions_vs_motives = np.array([rhs_positions, rhs_motives[:,0]])

        dimensionless_motive_vs_distance_rhs = scipy.interpolate.UnivariateSpline(rhs_positions, rhs_motives[:,0])

        object.__setattr__(self, "dimensionless_motive_vs_distance_rhs", dimensionless_motive_vs_distance_rhs)


    def _langmuirs_dimensionless_poisson_eq(self, motive: np.typing.ArrayLike, position: np.typing.ArrayLike) -> np.ndarray:
        """
        Langmuir's dimensionless Poisson's equation for the ODE solver
        """

        # Note:
        # motive[0] = motive.
        # motive[1] = motive[0]'

        if position >= 0:
            result = np.array([motive[1], 0.5*np.exp(motive[0])*(1-scipy.special.erf(motive[0]**0.5))])
        if position < 0:
            result = np.array([motive[1], 0.5*np.exp(motive[0])*(1+scipy.special.erf(motive[0]**0.5))])

        return result


    def interelectrode_spacing(self) -> astropy.units.Quantity[astropy.units.um]:
        """
        Distance between collector and emitter


        Warnings
        --------
        This method is identical to `tec.TEC.interelectrode_spacing`.
        I have implemented it here because other methods rely on it.
        """
        return (self.collector.position - self.emitter.position).to(astropy.units.um)


    def output_voltage(self) -> astropy.units.Quantity[astropy.units.V]:
        """
        Voltage difference between collector and emitter

        Warnings
        --------
        This method is identical to `tec.TEC.interelectrode_spacing`.
        I have implemented it here because other methods rely on it.
        """
        return (self.collector.voltage - self.emitter.voltage).to(astropy.units.V)


    def normalization_length(self, current_density: float | astropy.units.Quantity["A/cm2"]) -> astropy.units.Quantity[astropy.units.um]:
        """
        Coefficient to convert dimensionless to dimensioned positions

        Corresponds to the quantity represented by :math:`x_{0}` in
        :cite:`9780262080606` section 10.3.1.


        Parameters
        ----------
        current_density : float | astropy.units.Quantity["A/cm2"]
            Current density of device.


        Raises
        ------
        ValueError
            If ``current_density`` param < 0
        """
        if current_density < 0:
            raise ValueError("current_density cannot be negative")

        # Coerce `current_density` to `astropy.units.Quantity`
        current_density = astropy.units.Quantity(current_density, "A cm-2")

        prefactor = ((astropy.constants.eps0**2 * astropy.constants.k_B**3)/(2 * np.pi * astropy.constants.m_e * astropy.constants.e.si**2))**(1./4.)

        if current_density == 0:
            result = astropy.units.Quantity(np.inf, "um")
        else:
            result = prefactor * self.emitter.temperature**(3./4.) / current_density**(1./2.)

        return result.to("um")


    # Probably should be an attribute.
    def saturation_point_voltage(self) -> astropy.units.Quantity[astropy.units.V]:
        """
        Saturation point voltage

        Corresponds to the quantity represented by :math:`V_{S}` in
        :cite:`9780262080606` section 10.3.1.
        """
        # The prefix "dimensionless" is implied in the following
        # calculations as is the fact that they are taking place
        # at the saturation point.
        current_density = self.emitter.thermoelectron_current_density()

        position = self.interelectrode_spacing() / self.normalization_length(current_density)

        motive = self.dimensionless_motive_vs_distance_rhs(position)

        voltage = (self.emitter.barrier - self.collector.barrier - (motive * astropy.constants.k_B * self.emitter.temperature))/astropy.constants.e.si

        return voltage.to("V")


    # Probably should be an attribute.
    def saturation_point_current_density(self) -> astropy.units.Quantity["A/cm2"]:
        """
        Saturation point current density

        Corresponds to the quantity represented by :math:`V_{S}` in
        :cite:`9780262080606` section 10.3.1.
        """
        return self.emitter.thermoelectron_current_density()


    def critical_point_voltage(self) -> astropy.units.Quantity[astropy.units.V]:
        """
        Critical point voltage

        Corresponds to the quantity represented by :math:`V_{R}` in
        :cite:`9780262080606` section 10.3.1.
        """
        # The prefix "dimensionless" is implied in the following
        # calculations.
        output_current_density = self.critical_point_current_density()

        position = -self.interelectrode_spacing() / self.normalization_length(output_current_density)

        motive = np.log(self.emitter.thermoelectron_current_density() / output_current_density)

        voltage = (self.emitter.barrier - self.collector.barrier + (motive * astropy.constants.k_B * self.emitter.temperature))/astropy.constants.e.si

        return voltage.to("V")


    def critical_point_current_density(self) -> astropy.units.Quantity["A/cm2"]:
        """
        Critical point current density

        Corresponds to the quantity represented by :math:`V_{R}` in
        :cite:`9780262080606` section 10.3.1.
        """
        # Rootfinder to get critical point output current density.
        current_density_hi_limit = self.emitter.thermoelectron_current_density()
        output_current_density = scipy.optimize.brentq(self._critical_point_target_function, current_density_hi_limit.value, 0)
        output_current_density = astropy.units.Quantity(output_current_density, "A cm-2")

        return output_current_density


    def _critical_point_target_function(self, current_density: np.typing.ArrayLike) -> np.ndarray:
        """
        Target function to determine critical point current density

        Parameters
        ----------
        current_density
            Assumed to be in units of A/cm2.
        """
        current_density = astropy.units.Quantity(current_density, "A cm-2")

        position1 = -(self.interelectrode_spacing() / self.normalization_length(current_density)).value

        if current_density == 0:
            motive = np.inf
        else:
            motive = np.log(self.emitter.thermoelectron_current_density() / current_density)

        if motive < 0:
            raise ValueError("current_density greater than tec's emitter saturation current density")

        position2 = self.dimensionless_distance_vs_motive_lhs(motive)

        difference = position1 - position2

        return difference


    @property
    def max_motive(self) -> astropy.units.Quantity[astropy.units.eV]:
        """
        Documented in class docstring
        """
        # Accelerating regime
        if self.output_voltage() < self.saturation_point_voltage():
            motive = self.emitter.motive()

        # Retarding regime
        elif self.output_voltage() > self.critical_point_voltage():
            motive = self.collector.motive()

        # Space charge limiting regime
        else:
            # Space charge limited mode.
            saturation_point_current_density = self.saturation_point_current_density().value
            critical_point_current_density = self.critical_point_current_density().value

            if saturation_point_current_density == critical_point_current_density:
                output_current_density = self.saturation_point_current_density()
            else:
                value = scipy.optimize.brentq(self._output_voltage_target_function, saturation_point_current_density, critical_point_current_density)
                output_current_density = astropy.units.Quantity(value, "A cm-2")

            barrier = astropy.constants.k_B * self.emitter.temperature * np.log(self.emitter.thermoelectron_current_density() / output_current_density)

            motive = barrier + self.emitter.motive()

        return motive.to("eV")


    def _output_voltage_target_function(self, current_density):
        """
        Target function for the output voltage rootfinder
        """
        # For brevity, "dimensionless" prefix omitted from "position" and "motive" variable names.
        current_density = astropy.units.Quantity(current_density, "A cm-2")


        # The `em_motive` calculation below could be broken into
        # its own method because its used several places.
        em_motive = np.log(self.emitter.thermoelectron_current_density() / current_density)
        em_position = self.dimensionless_distance_vs_motive_lhs(em_motive)

        normalization_length = self.normalization_length(current_density)

        co_position = self.interelectrode_spacing() / normalization_length + em_position
        co_motive = self.dimensionless_motive_vs_distance_rhs(co_position)

        target_voltage = ((self.emitter.barrier + em_motive * astropy.constants.k_B * self.emitter.temperature) - (self.collector.barrier + co_motive * astropy.constants.k_B * self.emitter.temperature)) / astropy.constants.e.si

        difference = self.output_voltage() - target_voltage

        return difference.to("V").value


    # FIXME: this is a hack, as is `tec.models.Ideal.copy`. These
    # methods should be generalized.
    def copy(self) -> "tec.models.Langmuir":
        """
        Copy of Langmuir object
        """
        args = attrs.asdict(self, recurse=False)
        return Langmuir(emitter=args["emitter"], collector=args["collector"])
