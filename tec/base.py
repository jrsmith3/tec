import numpy as np
from scipy import interpolate, optimize
import matplotlib.pyplot as plt
import matplotlib
from astropy import units, constants


class TECBase(object):
    """
    Base thermoelectron engine class

    This class provides the base API for subclasses which implement particular models of TEC electron transport. Even though this class isn't intended to be a model, it implements a model of electron transport which completely ignores the negative space charge effect, similar to the model described on p. 51 of :cite:`9780262080590`.

    :param emitter: Object from `tec.electrode` which initializes emitter.
    :param collector: Object from `tec.electrode` which initializes collector.

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

    def __init__(self, emitter, collector):
        self.emitter = emitter
        self.collector = collector


    # Methods regarding motive ----------------------------------------
    def calc_motive(self, position):
        """
        Value of motive relative to electrical ground

        :param position: float or numpy array at which motive is to be evaluated.
        :raises: ValueError if position falls outside interelectrode space
        :returns: `astropy.units.Quantity` in units of :math:`eV`.
        :symbol: :math:`\psi`
        """
        abscissae = np.array([emitter.position, collector.position])
        ordinates = np.array([emitter.calc_motive(), collector.calc_motive()])

        spl = interpolate.UnivariateSpline(abscissae, ordinates, k=1, ext=2)

        motive = spl(position)

        return motive


    def calc_max_motive(self):
        """
        Value of maximum motive relative to electrical ground

        :returns: `astropy.units.Quantity` in units of :math:`eV`.
        :symbol: :math:`\psi_{m}`
        """
        if emitter.calc_motive() > collector.calc_motive():
            max_motive = emitter.calc_motive()
        else:
            max_motive = collector.calc_motive()

        return max_motive


    def calc_max_motive_position(self):
        """
        Position at maximum motive

        :returns: `astropy.units.Quantity` in units of :math:`um`.
        :symbol: :math:`\x_{m}`
        """
        if emitter.calc_motive() > collector.calc_motive():
            max_motive_position = emitter.position
        else:
            max_motive_position = collector.position

        return max_motive_position


    # Methods returning basic data about the TEC ----------------------
    def calc_interelectrode_spacing(self):
        """
        Distance between collector and emitter

        :returns: `astropy.units.Quantity` in units of :math:`um`.
        :symbol: :math:`d`
        """
        return self.collector.position - self.emitter.position


    def calc_output_voltage(self):
        """
        Voltage difference between collector and emitter

        :returns: `astropy.units.Quantity` in units of :math:`V`.
        :symbol: :math:`V`
        """
        return self.collector.voltage - self.emitter.voltage


    def calc_contact_potential(self):
        """
        Contact potential between collector and emitter

        The contact potential is defined as the difference in barrier height between the emitter and collector. This value should not be confused with the quantity returned by :meth:`calc_output_voltage` which is the voltage difference between the collector and emitter.
        """
        return (self.emitter.barrier - self.collector.barrier) / constants.e


    # Methods regarding current and power -----------------------------
    def calc_forward_current_density(self):
        """
        Net current moving from emitter to collector

        :returns: `astropy.units.Quantity` in units of :math:`A cm^{-2}`.
        :symbol: :math:`J_{f}`
        """
        sat_current_density = self.emitter.calc_saturation_current_density()

        if self.emitter.calc_barrier_ht() >= self.get_max_motive_ht():
            current_density = sat_current_density
        else:
            barrier = self.get_max_motive_ht() - self.emitter.calc_barrier_ht()
            kT = constants.k_B * self.emitter.temp
            exponent = (barrier / kT).decompose()

            current_density = sat_current_density * np.exp(-exponent)

        return current_density


    def calc_back_current_density(self):
        """
        Net current moving from collector to emitter

        :returns: `astropy.units.Quantity` in units of :math:`A cm^{-2}`.
        :symbol: :math:`J_{b}`
        """
        sat_current_density = self.collector.calc_saturation_current_density()

        if self.collector.calc_barrier_ht() >= self.get_max_motive_ht():
            current_density = sat_current_density
        else:
            barrier = self.get_max_motive_ht() - self.collector.calc_barrier_ht()
            kT = constants.k_B * self.emitter.temp
            exponent = (barrier/kT).decompose()

            current_density = sat_current_density * np.exp(-exponent)

        return current_density


    def calc_output_current_density(self):
        """
        Net current density flowing across device

        :returns: `astropy.units.Quantity` in units of :math:`A cm^{-2}`.
        :symbol: :math:`J`
        """
        return self.calc_forward_current_density() - self.calc_back_current_density()


    def calc_output_power_density(self):
        """
        Output power density of device

        :returns: `astropy.units.Quantity` in units of :math:`W cm^{-2}`.
        :symbol: :math:`w`
        """
        power_dens = self.calc_output_current_density() * self.calc_output_voltage()

        return power_dens.to("W/cm2")


    # Methods regarding efficiency ------------------------------------
    def calc_carnot_efficiency(self):
        """
        Carnot efficiency

        :returns: float between 0 and 1 where unity is 100% efficiency. Returns NaN if collector temperature is greater than emitter temperature.
        :symbol: :math:`J`
        """
        if self.emitter.temp >= self.collector.temp:
            efficiency = 1 - (self.collector.temp / self.emitter.temp)
        else:
            efficiency = np.NaN

        return efficiency


    def calc_efficiency(self):
        """
        Total thermal efficiency

        This method calculates the thermal efficiency of a TEC after Hatsopoulos and Gyftopoulos :cite:`97802620800590` Sec. 2.7. Efficiency, :math:`\eta`, is defined as the ratio of the output power, :math:`W_{T}`, to the rate at which heat is added to the device, :math:`Q_{in}`.

        .. math::
            \eta = \\frac{W_{T}}{Q_{in}}

        The law of conservation of energy determines the relationship between these quantities and the heat rejection rate, :math:`Q_{out}`

        .. math::
            Q_{in} = W_{T} + Q_{out}

        The quantities :math:`Q_{in}` and :math:`Q_{out}` are determined by accounting for all the flows of energy into and out of the system. For the purposes of calculating the efficiency, :math:`Q_{in}` accounts for the heat transport via electrons (see :meth:`calc_electron_cooling_rate`, denoted by :math:`Q_{E}`) and photons (see :meth:`calc_thermal_rad_rate`, denoted by :math:`Q_{r}`). This efficiency calculation *does not* presently account for heat conducted via the leads. Therefore, :math:`Q_{in}` is given by

        .. math::
            Q_{in} = Q_{E} + Q_{r}

        See :meth:`calc_heat_supply_rate` for more information about :math:`Q_{in}`.

        :returns: float between 0 and 1 where unity is 100% efficiency. Returns NaN if the output power is less than zero.
        :symbol: :math:`\eta`
        """
        if self.calc_output_power_density() > 0:
            efficiency = self.calc_output_power_density() / self.calc_heat_supply_rate()
        else:
            efficiency = np.nan

        return efficiency


    def calc_heat_supply_rate(self):
        """
        Rate at which heat enters device

        The heat supply rate is the sum of all rates of heat transferred to the emitter. Currently this method accounts for heat transferred via thermoelectrons and photons, *but not* heat transferred through the electrical leads of the device.

        .. math::
            Q_{in} = Q_{E} + Q_{r}

        where :math:`Q_{E}` and :math:`Q_{r}` are calculated using :meth:`calc_electron_cooling_rate` and :meth:`calc_thermal_rad_rate`, respectively.

        :returns: `astropy.units.Quantity` in units of :math:`W cm^{-2}`.
        :symbol: :math:`Q_{in}`
        """
        heat_supply_rate = self.calc_electron_cooling_rate() + self.calc_thermal_rad_rate()

        return heat_supply_rate


    def calc_electron_cooling_rate(self):
        """
        Electronic cooling rate of emitter

        This method calculates the net heat flow carried by electrons from the emitter according to Hatsopoulos and Gyftopoulos :cite:`97802620800590` Eq. 2.57a, repeated below

        .. math::
            Q_{E} = S J_{f} \\frac{\psi_{max} - \mu_{E} + 2kT_{E}}{e} - S J_{b}\\frac{\psi_{max} - \mu_{E} + 2kT_{C}}{e}

        The quantity :math:`S` is the area of the electrode, and taken to be unit area (1 cm^2) here.

        :returns: `astropy.units.Quantity` in units of :math:`W cm^{-2}`.
        :symbol: :math:`Q_{E}`
        """
        kT_E2 = 2 * constants.k_B * self.emitter.temp
        kT_C2 = 2 * constants.k_B * self.collector.temp

        unit_area = units.Quantity(1., "cm2")

        forward = unit_area * self.calc_forward_current_density() * (self.calc_max_motive_height + kT_E2) / constants.e
        back = unit_area * self.calc_back_current_density * (self.calc_max_motive_height + kT_C2) / constants.e

        cooling_rate = (forward - back).to("W/cm2")

        return cooling_rate


    def calc_thermal_rad_rate(self):
        """
        Interelectrode thermal radiation rate

        This method calculates the heat transfer carried across the interelectrode space via blackbody photons. Since the emitter and collector can have different values of emissivity, the TEC will have a net emissivity, accounted for by (NAME) :cite:`9780471457275` p. 793, Eq. 13.19. The thermal radiation rate is given by

        .. math::
            Q_{r} = \\frac{\sigma (T_{E}^{4} - T_{C}^{4})}{\\frac{1}{\epsilon_{E}} + \\frac{1}{\epsilon_{C}} - 1}

        :returns: `astropy.units.Quantity` in units of :math:`W cm^{-2}`.
        :symbol: :math:`Q_{r}`
        """
        ideal_rad_rate = constants.sigma_sb * (self.emitter.temp**4 - self.collector.temp**4)
        net_emissivity = (1./self.emitter.emissivity) + (1./self.collector.emissivity) - 1.

        rad_rate = ideal_rad_rate / net_emissivity

        return rad_rate
