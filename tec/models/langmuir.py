# -*- coding: utf-8 -*-

import numpy as np
from scipy import interpolate, optimize, integrate, special
from astropy import units, constants
from tec import TECBase


class DimensionlessLangmuirPoissonSoln(dict):
    """
    Numerical solution of Langmuir's dimensionless Poisson's equation.

    The purpose of this class is to provide an API to the solution of Langmuir's dimensionless Poisson's equation :cite:`10.1103/PhysRev.21.419` to provide the appropriate level of simplicity to the user. Via the class methods, the user can access either the dimensionless motive vs. dimensionless position or the dimensionless position vs. dimensionless motive, both of which are necessary in the Langmuir model. This class uses an ode solver to approximate the solution to the ode, then interpolation to return values at arbitrary abscissae -- see the source for details of the ode solver and interpolation algorithm.
    """

    def __init__(self):
        # Here is the algorithm:
        # 1. Set up the default ode solver parameters.
        # 2. Check to see if either the rhs or lhs params were passed as arguments. If not, use the default params.
        # 3. Cat the additional default ode solver parameters to the lhs and rhs set of params.
        # 4. Solve both the lhs and rhs odes.
        # 5. Create the lhs and rhs interpolation objects.

        self["lhs"] = self.calc_branch(-2.5538)
        self["rhs"] = self.calc_branch(100)

        # data = np.loadtxt("tec/models/kleynen_langmuir.dat")
        # rhs = data[565:-1,:]
        # self["rhs"] = {}

        # self["rhs"]["motive_v_position"] = \
        #     interpolate.InterpolatedUnivariateSpline(rhs[:,0],rhs[:,1])
        # self["rhs"]["position_v_motive"] = \
        #         interpolate.InterpolatedUnivariateSpline(rhs[:,1],rhs[:,0],k=1)

    def calc_branch(self, endpoint, num_points=1000):
        """
        Numerical solution for either side of the ode.

        :param float endpoint: Endpoint for the ode solver.
        :param int num_points: Number of points for ode solver to use.
        :rtype: Dictionary of interpolation objects.

        This method returns a dictionary with items, "motive_v_position" and "position_v_motive"; each item an interpolation of what its name describes.
        """
        ics = np.array([0, 0])
        position_array = np.linspace(0, endpoint, num_points)
        motive_array = integrate.odeint(self.langmuir_poisson_eq, ics, position_array)

        # Create the motive_v_position interpolation, but first check the abscissae (position_array) are monotonically increasing.
        if position_array[0] < position_array[-1]:
            motive_v_position = \
                interpolate.InterpolatedUnivariateSpline(position_array, motive_array[:, 0])
        else:
            motive_v_position = \
                interpolate.InterpolatedUnivariateSpline(position_array[::-1], motive_array[::-1, 0])

        # Now create the position_v_motive interpolation but first check the abscissae (motive_array in this case) are monotonically increasing. Use linear interpolation to avoid weirdness near the origin.

        # I think I don't need the following block.
        if motive_array[0, 0] < motive_array[-1, 0]:
            position_v_motive = \
                interpolate.InterpolatedUnivariateSpline(motive_array[:, 0], position_array, k=1)
        else:
            position_v_motive = \
                interpolate.InterpolatedUnivariateSpline(motive_array[::-1, 0], position_array[::-1], k=1)

        return {"motive_v_position": motive_v_position, "position_v_motive": position_v_motive}

    def position(self, motive, branch="lhs"):
        """
        Interpolation of dimensionless position at arbitrary dimensionless motive.

        :param float motive: Argument of interpolation.
        :param str branch=="lhs": Interpolate from left-hand side of solution to ode.
        :param str branch=="rhs": Interpolate from right-hand side of solution to ode.
        :returns: Interpolated position.
        :rtype: float

        The left or right hand side must be specified since the inverse of the solution to Langmuir's dimensionless Poisson's equation is not a single-valued function. Returns NaN if motive is < 0.
        """

        if type(branch) is not str:
            raise TypeError("branch must be of type str.")
        # if branch is not "lhs" or "rhs":
        # raise ValueError("branch must either be 'lhs' or 'rhs'.")

        if motive < 0:
            return np.NaN

        # if branch is "lhs" or branch is "rhs":
        if branch is "lhs" and motive > 18.7:
            return -2.55389
        else:
            return self[branch]["position_v_motive"](motive)

    def motive(self, position):
        """
        Value of motive relative to ground for given value(s) of position in J.

        :param position: float or numpy array at which motive is to be evaluated. Returns NaN if position falls outside of the interelectrode space.
        """
        if position < -2.55389:
            return np.NaN
        elif position <= 0:
            return self["lhs"]["motive_v_position"](position)
        else:
            return self["rhs"]["motive_v_position"](position)

    def langmuir_poisson_eq(self, motive, position):
        """
        Langmuir's dimensionless Poisson's equation for the ODE solver.
        """

        # Note:
        # motive[0] = motive.
        # motive[1] = motive[0]'

        if position >= 0:
            return np.array([motive[1], 0.5*np.exp(motive[0])*(1-special.erf(motive[0]**0.5))])
        if position < 0:
            return np.array([motive[1], 0.5*np.exp(motive[0])*(1+special.erf(motive[0]**0.5))])


class Langmuir(TECBase):
    """
    Considers space charge, ignores NEA and back emission.

    This class explicitly ignores the fact that either electrode may have NEA and determines the vacuum level of an electrode at the barrier. The model is based on :cite:`10.1103/PhysRev.21.419`.

    Attributes
    ----------
    :class:`Langmuir` objects have the same attributes as :class:`tec.TECBase`; "motive_data" is structured specifically for this model and contains the following data. For brevity, "dimensionless" prefix omitted from "position" and "motive" variable names.

    * saturation_pt: Dictionary with keys "output_voltage" [V] and "output_current_density" [A m^-2] at the saturation point.
    * critical_pt: Dictionary with keys "output_voltage" [V] and "output_current_density" [A m^-2] at the critical point.
    * dps: Langmuir's dimensionless Poisson's equation solution object.

    Examples and interface testing
    ------------------------------
    >>> from tec_langmuir import TEC_Langmuir
    >>> em_dict = {"temp":1000,
    ...                        "barrier":1,
    ...                        "voltage":0,
    ...                        "position":0,
    ...                        "richardson":10,
    ...                        "emissivity":0.5}
    >>> co_dict = {"temp":300,
    ...                        "barrier":0.8,
    ...                        "voltage":0,
    ...                        "position":10,
    ...                        "richardson":10,
    ...                        "emissivity":0.5}
    >>> input_dict = {"Emitter":em_dict, "Collector":co_dict}
    >>> example_tec = TEC_Langmuir(input_dict)
    >>> isinstance(example_tec["motive_data"]["saturation_pt"]["output_voltage"],float)
    True
    >>> isinstance(example_tec["motive_data"]["saturation_pt"]["output_current_density"],float)
    True
    >>> isinstance(example_tec["motive_data"]["critical_pt"]["output_voltage"],float)
    True
    >>> isinstance(example_tec["motive_data"]["critical_pt"]["output_current_density"],float)
    True
    >>> type(example_tec["motive_data"]["dps"])
    <class 'tec.dimensionlesslangmuirpoissonsoln.DimensionlessLangmuirPoissonSoln'>
    """

    def __init__(self, emitter, collector, **kwargs):
        self.emitter = emitter
        self.collector = collector
        self._dps = DimensionlessLangmuirPoissonSoln()


    # Methods regarding critical and saturation points ---------------
    def normalization_length(self, current_density):
        """
        Normalization length for Langmuir solution

        :param current_density: Current density in units of :math:`A cm^{-2}`.
        :returns: `astropy.units.Quantity` in units of :math:`\mu m`.
        :symbol: :math:`x_{0}`
        """
        # Coerce `current_density` to `astropy.units.Quantity`
        current_density = units.Quantity(current_density, "A cm-2")

        if current_density < 0:
            raise ValueError("current_density cannot be negative")

        prefactor = ((constants.eps0**2 * constants.k_B**3)/(2 * np.pi * constants.m_e * constants.e.si**2))**(1./4.)

        if current_density == 0:
            result = units.Quantity(np.inf, "um")
        else:
            result = prefactor * self.emitter.temp**(3./4.) / current_density**(1./2.)

        return result.to("um")

    def saturation_point_voltage(self):
        """
        Saturation point voltage

        :returns: `astropy.units.Quantity` in units of :math:`V`.
        :symbol: :math:`V_{S}`
        """
        # The prefix "dimensionless" is implied in the following
        # calculations as is the fact that they are taking place
        # at the saturation point.
        current_density = self.emitter.thermoelectron_current_density()

        position = self.interelectrode_spacing() / self.normalization_length(current_density)

        motive = self._dps.motive(position)

        voltage = (self.emitter.barrier - self.collector.barrier - (motive * constants.k_B * self.emitter.temp))/constants.e.si

        return voltage.to("V")

    def saturation_point_current_density(self):
        """
        Saturation point current density

        :returns: `astropy.units.Quantity` in units of :math:`A cm^{-2}`.
        :symbol: :math:`J_{S}`
        """
        return self.emitter.thermoelectron_current_density()

    def critical_point_voltage(self):
        """
        Critical point voltage

        :returns: `astropy.units.Quantity` in units of :math:`V`.
        :symbol: :math:`V_{R}`
        """
        # The prefix "dimensionless" is implied in the following
        # calculations.
        output_current_density = self.critical_point_current_density()

        position = -self.interelectrode_spacing() / self.normalization_length(output_current_density)

        motive = np.log(self.emitter.thermoelectron_current_density() / output_current_density)

        voltage = (self.emitter.barrier - self.collector.barrier + (motive * constants.k_B * self.emitter.temp))/constants.e.si

        return voltage.to("V")

    def critical_point_current_density(self):
        """
        Critical point current density

        :returns: `astropy.units.Quantity` in units of :math:`A cm^{-2}`.
        :symbol: :math:`J_{R}`
        """
        # Rootfinder to get critical point output current density.
        current_density_hi_limit = self.emitter.thermoelectron_current_density()
        output_current_density = optimize.brentq(self.critical_point_target_function, current_density_hi_limit.value, 0)
        output_current_density = units.Quantity(output_current_density, "A cm-2")

        return output_current_density

    def critical_point_target_function(self, current_density):
        """
        Difference between two methods of calculating dimensionless distance

        :returns: `float`.
        """
        current_density = units.Quantity(current_density, "A cm-2")

        # The prefix "dimensionless" is implied in the following
        # calculations.
        position1 = -self.interelectrode_spacing() / self.normalization_length(current_density)
        position1 = position1.value

        if current_density == 0:
            motive = np.inf
        else:
            motive = np.log(self.emitter.thermoelectron_current_density() / current_density)

        if motive < 0:
            raise ValueError("current_density greater than tec's emitter saturation current density")

        position2 = self._dps.position(motive)

        difference = position1 - position2

        return difference

    def operating_regime(self):
        """
        String describing regime of electron transport

        This method evaluates the TEC and returns either "accelerating", "space charge limited", or "retarding" to indicate the regime in which the TEC is operating.

        :returns: `string`.
        """
        if self.output_voltage() < self.saturation_point_voltage():
            regime = "accelerating"
        elif self.output_voltage() > self.critical_point_voltage():
            regime = "retarding"
        else:
            regime = "space charge limited"

        return regime


    # Methods regarding motive ---------------------------------------
    def max_motive(self):
        """
        Value of maximum motive relative to electrical ground

        :returns: `astropy.units.Quantity` in units of :math:`eV`.
        :symbol: :math:`\psi_{m}`
        """
        regime = self.operating_regime()
        if regime == "accelerating":
            motive = self.emitter.motive()
        elif regime == "retarding":
            motive = self.collector.motive()
        else:
            # Space charge limited mode.
            spcd = self.saturation_point_current_density()
            spcd = spcd.value

            cpcd = self.critical_point_current_density()
            cpcd = cpcd.value

            output_current_density = optimize.brentq(self.output_voltage_target_function, spcd, cpcd)
            output_current_density = units.Quantity(output_current_density, "A cm-2")

            barrier = constants.k_B * self.emitter.temp * np.log(self.emitter.thermoelectron_current_density() / output_current_density)

            motive = barrier + self.emitter.motive()

        return motive.to("eV")

    def output_voltage_target_function(self, current_density):
        """
        Target function for the output voltage rootfinder.
        """
        # For brevity, "dimensionless" prefix omitted from "position" and "motive" variable names.
        current_density = units.Quantity(current_density, "A cm-2")


        # The `em_motive` calculation below could be broken into
        # its own method because its used several places.
        em_motive = np.log(self.emitter.thermoelectron_current_density() / current_density)
        em_position = self._dps.position(em_motive)

        normalization_length = self.normalization_length(current_density)

        co_position = self.interelectrode_spacing() / normalization_length + em_position
        co_motive = self._dps.motive(co_position)

        target_voltage = ((self.emitter.barrier + em_motive * constants.k_B * self.emitter.temp) - (self.collector.barrier + co_motive * constants.k_B * self.emitter.temp)) / constants.e.si

        difference = self.output_voltage() - target_voltage

        return difference.to("V").value


    # Methods regarding current and power -----------------------------
    def back_current_density(self):
        """
        Net current moving from collector to emitter

        :returns: `astropy.units.Quantity` in units of :math:`A cm^{-2}`.
        :symbol: :math:`J_{b}`
        """
        return units.Quantity(0, "A/cm2")
