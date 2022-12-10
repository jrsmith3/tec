# coding: utf-8

import inspect
import itertools
import numpy as np
from scipy import interpolate, optimize
from astropy import units, constants
from tec.electrode import Metal

# Optional packages
try:
    import matplotlib.pyplot as plt
    import matplotlib
except ImportError, e:
    if not e.args[0].startswith('No module named matplotlib'):
        raise


class TECBase(object):
    """
    Base thermoelectron engine class

    This class provides the base API for subclasses which implement particular models of TEC electron transport. Even though this class isn't intended to be a model, it implements a model of electron transport which completely ignores the negative space charge effect, similar to the model described on p. 51 of :cite:`9780262080590`.

    :param emitter: Object from `tec.electrode` which initializes emitter.
    :param collector: Object from `tec.electrode` which initializes collector.

    Arguments in addition to the ones listed will be ignored.

    Attributes
    ==========
    `TECBase` objects have two attributes: `emitter` and `collector`, both of which are objects from `tec.electrode`.

    Examples
    ========
    >>> from tec.electrode import Metal
    >>> from tec import TECBase
    >>> em = Metal(temp=1000, barrier=1, richardson=10, voltage=0, position=0, emissivity=0.5)
    >>> co = Metal(temp=300, barrier=0.8, richardson=10, emissivity=0.5, voltage=0, position=10,)
    >>> example_tec = TECBase(emitter = em, collector = co)
    """

    @property
    def emitter(self):
        return self._emitter

    @emitter.setter
    def emitter(self, value):
        if Metal not in inspect.getmro(value.__class__):
            raise TypeError("Cannot set 'emitter' with non-electrode type.")
        else:
            self._emitter = value

    @property
    def collector(self):
        return self._collector

    @collector.setter
    def collector(self, value):
        if Metal not in inspect.getmro(value.__class__):
            raise TypeError("Cannot set 'collector' with non-electrode type.")
        else:
            self._collector = value


    def __init__(self, emitter, collector, **kwargs):
        self.emitter = emitter
        self.collector = collector

    def __iter__(self):
        """
        Returns iterator from iterelectrodesdicts method
        """
        return self.iterelectrodesdicts()

    def __repr__(self):
        return str(dict(self))

    def iterelectrodes(self):
        """
        Iterator over object's data

        This iterator yields 2-tuples. The zeroth element of the 2-tuple will be a str.

        All of the TECBase's electrodes will appear once and only once during the iteration (i.e. the emitter and collector attributes). Specifically, the iterator will return a 2-tuple whose zeroth element is a string with the attribute name and whose first element is the electrode object itself.

        In addition, at some point during the iteration, the iterator will return a 2-tuple whose zeroth element 'max_motive' and first element the value of the max_motive method. This value will be a float; the unit is implied by the default return unit of the tec.TECBase.max_motive method.

        Finally, at some point during the iteration, the iterator will return a 2-tuple whose zeroth element is the str '__class__' and whose value is the type object returned by the object calling type(self).

        The order of the items listed above is not guaranteed.
        """
        electrodes = [("emitter", self.emitter),
                      ("collector", self.collector)]
        max_motive_tuple = [("max_motive", self.max_motive().value)]
        class_tuple = [("__class__", type(self))]

        return itertools.chain(electrodes, max_motive_tuple, class_tuple)

    def iterelectrodesdicts(self):
        """
        Iterator over object's data with dicts for electrodes

        This method will return an iterator. This iterator will yield 2-tuples. The zeroth element of the 2-tuple will be a `str`.

        All of the `TECBase`'s electrodes will appear once and only once during the iteration (i.e. the `emitter` and `collector` attributes). Specifically, the iterator will return a 2-tuple whose zeroth element is a string with the attribute name and whose first element is *a dictionary* of the electrode object itself. Note that this functionality is in contrast to the functionality of the `tec.TECBase.iterelectrodes` method. The dictionaries returned in this case will be the same as those obtained by calling `dict` on one of the `TECBase`'s electrodes.

        In addition, at some point during the iteration, the iterator will return a 2-tuple whose zeroth element `'max_motive'` and first element the value of the `TECBase.max_motive` method. This value will be a `float`; the unit is implied by the default return unit of the `tec.TECBase.max_motive` method.

        Finally, at some point during the iteration, the iterator will return a 2-tuple whose zeroth element is the `str` `'__class__'` and whose value is the `type` object returned by the object calling `type(self)`.

        The order of the items listed above is not guaranteed.
        """
        electrodes = [("emitter", dict(self.emitter)),
                      ("collector", dict(self.collector))]
        max_motive_tuple = [("max_motive", self.max_motive().value)]
        class_tuple = [("__class__", type(self))]

        return itertools.chain(electrodes, max_motive_tuple, class_tuple)


    # Methods regarding motive ----------------------------------------
    def motive(self, position):
        """
        Value of motive relative to electrical ground

        :param position: float or numpy array at which motive is to be evaluated. This argument can also be an `astropy.units.Quantity`, but it must be in units of length.
        :raises: ValueError if position falls outside interelectrode space.
        :returns: `astropy.units.Quantity` in units of :math:`eV`.
        :symbol: :math:`\psi`
        """
        # Explictly set abscissae and ordinates in um and eV, respectively
        abscissae = units.Quantity([self.emitter.position, self.collector.position], "um")
        ordinates = units.Quantity([self.emitter.motive(), self.collector.motive()], "eV")

        spl = interpolate.UnivariateSpline(abscissae, ordinates, k=1, ext=2)

        motive = spl(position) * ordinates.unit

        return motive


    def max_motive(self):
        """
        Value of maximum motive relative to electrical ground

        :returns: `astropy.units.Quantity` in units of :math:`eV`.
        :symbol: :math:`\psi_{m}`
        """
        if self.emitter.motive() > self.collector.motive():
            max_motive = self.emitter.motive()
        else:
            max_motive = self.collector.motive()

        return max_motive


    def max_motive_position(self):
        """
        Position at maximum motive

        :returns: `astropy.units.Quantity` in units of :math:`um`.
        :symbol: :math:`x_{m}`
        """
        if self.emitter.motive() > self.collector.motive():
            max_motive_position = self.emitter.position
        else:
            max_motive_position = self.collector.position

        return max_motive_position


    # Methods returning basic data about the TEC ----------------------
    def interelectrode_spacing(self):
        """
        Distance between collector and emitter

        :returns: `astropy.units.Quantity` in units of :math:`um`.
        :symbol: :math:`d`
        """
        return self.collector.position - self.emitter.position


    def output_voltage(self):
        """
        Voltage difference between collector and emitter

        :returns: `astropy.units.Quantity` in units of :math:`V`.
        :symbol: :math:`V`
        """
        return self.collector.voltage - self.emitter.voltage


    def contact_potential(self):
        """
        Contact potential between collector and emitter

        The contact potential is defined as the difference in barrier height between the emitter and collector. This value should not be confused with the quantity returned by :meth:`output_voltage` which is the voltage difference between the collector and emitter.

        .. math::
            V_{contact} = \\frac{\psi_{E} - \psi_{C}}{e}

        :returns: `astropy.units.Quantity` in units of :math:`V`.
        :symbol: :math:`V_{contact}`
        """
        contact_potential = (self.emitter.barrier - self.collector.barrier) / constants.e.si

        return contact_potential.to("V")


    # Methods regarding current and power -----------------------------
    def forward_current_density(self):
        """
        Net current moving from emitter to collector

        :returns: `astropy.units.Quantity` in units of :math:`A cm^{-2}`.
        :symbol: :math:`J_{f}`
        """
        diff_barrier = self.max_motive() - self.emitter.motive()

        if diff_barrier > 0:
            kT = constants.k_B * self.emitter.temp
            exponent = (diff_barrier / kT).decompose()
            scaling_factor = np.exp(-exponent)
        else:
            scaling_factor = 1.

        current = self.emitter.thermoelectron_current_density() * scaling_factor

        return current


    def back_current_density(self):
        """
        Net current moving from collector to emitter

        :returns: `astropy.units.Quantity` in units of :math:`A cm^{-2}`.
        :symbol: :math:`J_{b}`
        """
        diff_barrier = self.max_motive() - self.collector.motive()

        if diff_barrier > 0:
            kT = constants.k_B * self.collector.temp
            exponent = (diff_barrier / kT).decompose()
            scaling_factor = np.exp(-exponent)
        else:
            scaling_factor = 1.

        current = self.collector.thermoelectron_current_density() * scaling_factor

        return current


    def output_current_density(self):
        """
        Net current density flowing across device

        :returns: `astropy.units.Quantity` in units of :math:`A cm^{-2}`.
        :symbol: :math:`J`
        """
        return self.forward_current_density() - self.back_current_density()


    def output_power_density(self):
        """
        Output power density of device

        :returns: `astropy.units.Quantity` in units of :math:`W cm^{-2}`.
        :symbol: :math:`w`
        """
        power_dens = self.output_current_density() * self.output_voltage()

        return power_dens.to("W/cm2")


    # Methods regarding efficiency ------------------------------------
    def carnot_efficiency(self):
        """
        Carnot efficiency

        :returns: float between 0 and 1 where unity is 100% efficiency. Returns NaN if collector temperature is greater than emitter temperature.
        :symbol: :math:`\eta_{c}`
        """
        if self.emitter.temp >= self.collector.temp:
            efficiency = 1 - (self.collector.temp / self.emitter.temp)
        else:
            efficiency = np.NaN

        return efficiency.decompose().value


    def efficiency(self):
        """
        Total thermal efficiency

        This method calculates the thermal efficiency of a TEC after Hatsopoulos and Gyftopoulos :cite:`97802620800590` Sec. 2.7. Efficiency, :math:`\eta`, is defined as the ratio of the output power, :math:`W_{T}`, to the rate at which heat is added to the device, :math:`Q_{in}`.

        .. math::
            \eta = \\frac{W_{T}}{Q_{in}}

        The law of conservation of energy determines the relationship between these quantities and the heat rejection rate, :math:`Q_{out}`

        .. math::
            Q_{in} = W_{T} + Q_{out}

        The quantities :math:`Q_{in}` and :math:`Q_{out}` are determined by accounting for all the flows of energy into and out of the system. For the purposes of calculating the efficiency, :math:`Q_{in}` accounts for the heat transport via electrons (see :meth:`electron_cooling_rate`, denoted by :math:`Q_{E}`) and photons (see :meth:`thermal_rad_rate`, denoted by :math:`Q_{r}`). This efficiency calculation *does not* presently account for heat conducted via the leads. Therefore, :math:`Q_{in}` is given by

        .. math::
            Q_{in} = Q_{E} + Q_{r}

        See :meth:`heat_supply_rate` for more information about :math:`Q_{in}`.

        :returns: float between 0 and 1 where unity is 100% efficiency. Returns NaN if the output power is less than zero.
        :symbol: :math:`\eta`
        """
        if self.output_power_density() > 0:
            efficiency = self.output_power_density() / self.heat_supply_rate()
            efficiency = efficiency.value
        else:
            efficiency = np.nan

        return efficiency


    def heat_supply_rate(self):
        """
        Rate at which heat enters device

        The heat supply rate is the sum of all rates of heat transferred to the emitter. Currently this method accounts for heat transferred via thermoelectrons and photons, *but not* heat transferred through the electrical leads of the device.

        .. math::
            Q_{in} = Q_{E} + Q_{r}

        where :math:`Q_{E}` and :math:`Q_{r}` are calculated using :meth:`electron_cooling_rate` and :meth:`thermal_rad_rate`, respectively.

        :returns: `astropy.units.Quantity` in units of :math:`W`.
        :symbol: :math:`Q_{in}`
        """
        heat_supply_rate = self.electron_cooling_rate() + self.thermal_rad_rate()

        return heat_supply_rate


    def electron_cooling_rate(self):
        """
        Electronic cooling rate of emitter

        This method calculates the net heat flow carried by electrons from the emitter according to Hatsopoulos and Gyftopoulos :cite:`97802620800590` Eq. 2.57a, repeated below

        .. math::
            Q_{E} = S J_{f} \\frac{\psi_{max} - \mu_{E} + 2kT_{E}}{e} - S J_{b}\\frac{\psi_{max} - \mu_{E} + 2kT_{C}}{e}

        The quantity :math:`S` is the area of the electrode, and taken to be unit area (1 cm^2) here.

        :returns: `astropy.units.Quantity` in units of :math:`W`.
        :symbol: :math:`Q_{E}`
        """
        kT_E2 = 2 * constants.k_B * self.emitter.temp
        kT_C2 = 2 * constants.k_B * self.collector.temp
        max_motive = self.max_motive() - (constants.e.si * self.emitter.voltage)

        forward = units.Unit("cm2") * self.forward_current_density() * (max_motive + kT_E2) / constants.e.si
        back = units.Unit("cm2") * self.back_current_density() * (max_motive + kT_C2) / constants.e.si

        cooling_rate = (forward - back).to("W")

        return cooling_rate


    def thermal_rad_rate(self):
        """
        Interelectrode thermal radiation rate

        This method calculates the heat transfer carried across the interelectrode space via blackbody photons. Since the emitter and collector can have different values of emissivity, the TEC will have a net emissivity, accounted for by (NAME) :cite:`9780471457275` p. 793, Eq. 13.19. The thermal radiation rate is given by

        .. math::
            Q_{r} = \\frac{\sigma (T_{E}^{4} - T_{C}^{4})}{\\frac{1}{\epsilon_{E}} + \\frac{1}{\epsilon_{C}} - 1}

        :returns: `astropy.units.Quantity` in units of :math:`W`.
        :symbol: :math:`Q_{r}`
        """
        ideal_rad_rate = constants.sigma_sb * (self.emitter.temp**4 - self.collector.temp**4)

        emissivities = np.array([self.emitter.emissivity, self.collector.emissivity])
        if any(emissivities == 0):
            net_emissivity = 0
        else:
            net_emissivity = 1. / ((1. / self.emitter.emissivity) + (1. / self.collector.emissivity) - 1.)

        rad_rate = ideal_rad_rate * net_emissivity * units.Unit("cm2")

        return rad_rate.to("W")
