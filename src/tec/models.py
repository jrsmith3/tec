# coding: utf-8
import astropy.constants
import astropy.units
import attrs
import numpy as np
import scipy.integrate
import scipy.interpolate
import scipy.optimize
import scipy.special

from . import electrode, tec


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


    def _emitter_temperature_gt_collector_temperature(self):
        if self.emitter.temperature <= self.collector.temperature:
            raise ValueError("Emitter temperature must be greater than collector temperature")


    def _emitter_barrier_gt_collector_barrier(self):
        if self.emitter.barrier <= self.collector.barrier:
            raise ValueError("Emitter barrier must be greater than collector barrier")


    def _emitter_position_lt_collector_position(self):
        if self.emitter.position >= self.collector.position:
            raise ValueError("Emitter position must be greater than collector position")


    def __attrs_post_init__(self):
        # Check constraints.
        self._emitter_temperature_gt_collector_temperature()
        self._emitter_barrier_gt_collector_barrier()
        self._emitter_position_lt_collector_position()

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
        Copy of Metal object
        """
        args = attrs.asdict(self, recurse=False)
        del args["motive"]
        return Ideal(**args)
