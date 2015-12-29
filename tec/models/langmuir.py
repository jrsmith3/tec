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

    def get_position(self, motive, branch="lhs"):
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

    def get_motive(self, position):
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

    def back_current_density(self):
        """
        Net current moving from collector to emitter

        :returns: `astropy.units.Quantity` in units of :math:`A cm^{-2}`.
        :symbol: :math:`J_{b}`
        """
        return units.Quantity(0, "A/cm2")

    # Methods dealing with critical and saturation points
    def normalization_length(self, current_density):
        """
        Normalization length for Langmuir solution

        :param current_density: Current density in units of :math:`A cm^{-2}`.
        :returns: `astropy.units.Quantity` in units of :math:`\mu m`.
        :symbol: :math:`x_{0}`
        """
        # Coerce `current_density` to `astropy.units.Quantity`
        current_density = units.Quantity(current_density, "A cm-2")

        prefactor = ((constants.eps0**2 * constants.k_B**3)/(2 * np.pi * constants.m_e * constants.e.si**2))**(1./4.)

        result = prefactor * self.emitter.temp**(3./4.) / current_density**(1./2.)

        return result.to("um")


    # Methods dealing with critical and saturation points
    def saturation_point_voltage(self):
        """
        Saturation point voltage

        :returns: `astropy.units.Quantity` in units of :math:`V`.
        :symbol: :math:`V_{S}`
        """
        pass


    def calc_motive(self):
        """
        Calculates the motive (meta)data and populates the 'motive_data' attribute.
        """
        # Throw out any nea attributes if they exist.
        # I feel like this code needs some explanation. The model this class implements assumes that neither electrode has NEA. Therefore, it doesn't make sense to allow anyone to set an "nea" attribute for either electrode. However, it is possible to instantiate a TEC_Langmuir object without either electrode having an "nea" attribute, then later set an "nea" attribute for one of the electrodes. It would be easy to check for "nea" during instantiation, but I would have to write a lot of ugly, hacky code to prevent either of the electrodes from acquiring an "nea" attribute later on. Since the calc_motive() method is presumably called whenever the TEC_Langmuir attributes (or sub-attributes) are called, the following block of code will notice if "nea" has been added to the electrodes, and will remove it.
        for electrode in ["Emitter", "Collector"]:
            if "nea" in self[electrode]:
                del self[electrode]["nea"]

        # For brevity, "dimensionless" prefix omitted from "position" and "motive" variable names.

        self["motive_data"] = {}
        self["motive_data"]["dps"] = DimensionlessLangmuirPoissonSoln()

        self["motive_data"]["saturation_pt"] = self.calc_saturation_pt()
        self["motive_data"]["critical_pt"] = self.calc_critical_pt()

        if self.calc_output_voltage() < self["motive_data"]["saturation_pt"]["output_voltage"]:
            # Accelerating mode.
            self["motive_data"]["max_motive_ht"] = self["Emitter"].calc_motive_bc()
        elif self.calc_output_voltage() > self["motive_data"]["critical_pt"]["output_voltage"]:
            # Retarding mode.
            self["motive_data"]["max_motive_ht"] = self["Collector"].calc_motive_bc()
        else:
            # Space charge limited mode.
            output_current_density = optimize.brentq(self.output_voltage_target_function, self["motive_data"]["saturation_pt"]["output_current_density"], self["motive_data"]["critical_pt"]["output_current_density"])

            barrier = physical_constants["boltzmann"] * self["Emitter"]["temp"] * \
                np.log(self["Emitter"].calc_saturation_current_density()/output_current_density)
            self["motive_data"]["max_motive_ht"] = barrier + self["Emitter"].calc_motive_bc()

    def get_motive(self, pos):
        """
        Value of motive relative to ground for given value(s) of position in J.

        Position must be of numerical type or numpy array. Returns NaN if position
        falls outside of the interelectrode space.
        """
        # For brevity, "dimensionless" prefix omitted from "position" and "motive" variable names. The "position" and "motive" variables refer to the dimensionless quantities, while "pos" and "mot" refer to the dimensioned quantities.
        em_motive = (self.get_max_motive_ht() - self["Emitter"].calc_barrier_ht()) / \
            (physical_constants["boltzmann"] * self["Emitter"]["temp"])
        em_position = self["motive_data"]["dps"].get_position(em_motive)

        position = pos * ((2 * np.pi * physical_constants["electron_mass"] * physical_constants["electron_charge"]**2) / (physical_constants["permittivity0"]**2 * physical_constants["boltzmann"]**3))**(1.0/4) * (self.calc_output_current_density()**(1.0/2))/(self["Emitter"]["temp"]**(3.0/4)) + em_position

        # What follows is some hacky code

        motive = []

        for p in position:
            motive.append(self["motive_data"]["dps"].get_motive(p))

        # Turn the list into a numpy array
        motive = np.array(motive)

        mot = self.get_max_motive_ht() - \
            physical_constants["boltzmann"] * self["Emitter"]["temp"] * motive

        return mot

    def get_max_motive_ht(self, with_position=False):
        """
        Value of the maximum motive relative to ground in J.

        :param bool with_position: True returns the position at max motive instead.
        """
        if with_position:
            em_motive = (self.get_max_motive_ht() - self["Emitter"].calc_barrier_ht()) / \
                (physical_constants["boltzmann"] * self["Emitter"]["temp"])
            em_position = self["motive_data"]["dps"].get_position(em_motive)

            return -1 * em_position * ((physical_constants["permittivity0"]**2 * physical_constants["boltzmann"]**3) / (2*np.pi*physical_constants["electron_mass"] * physical_constants["electron_charge"]**2))**(1.0/4) * (self["Emitter"]["temp"]**(3.0/4))/(self.calc_output_current_density()**(1.0/2))
        else:
            return self["motive_data"]["max_motive_ht"]

    def calc_saturation_pt(self):
        """
        Determine saturation point condition.

        :rtype: Dictionary with keys "output_voltage" [V] and "output_current_density" [A m^-2] at the saturation point.
        """
        # For brevity, "dimensionless" prefix omitted from "position" and "motive" variable names.
        output_current_density = self["Emitter"].calc_saturation_current_density()

        position = self.calc_interelectrode_spacing() * ((2 * np.pi * physical_constants["electron_mass"] * physical_constants["electron_charge"]**2) / (physical_constants["permittivity0"]**2 * physical_constants["boltzmann"]**3))**(1.0/4) * (output_current_density**(1.0/2))/(self["Emitter"]["temp"]**(3.0/4))

        motive = self["motive_data"]["dps"].get_motive(position)

        output_voltage = (self["Emitter"]["barrier"] - self["Collector"]["barrier"] - motive * physical_constants["boltzmann"] * self["Emitter"]["temp"]) / physical_constants["electron_charge"]

        return {"output_voltage": output_voltage, "output_current_density": output_current_density}

    def calc_critical_pt(self):
        """
        Determine critical point condition.

        :rtype: Dictionary with keys "output_voltage" [V] and "output_current_density" [A m^-2] at the critical point.
        """
        # For brevity, "dimensionless" prefix omitted from "position" and "motive" variable names.

        # Rootfinder to get critical point output current density.
        output_current_density = optimize.brentq(self.critical_point_target_function, self["Emitter"].calc_saturation_current_density(), 0)

        position = -self.calc_interelectrode_spacing() * ((2 * np.pi * physical_constants["electron_mass"] * physical_constants["electron_charge"]**2) / (physical_constants["permittivity0"]**2 * physical_constants["boltzmann"]**3))**(1.0/4) * (output_current_density**(1.0/2))/(self["Emitter"]["temp"]**(3.0/4))

        motive = np.log(self["Emitter"].calc_saturation_current_density()/output_current_density)

        output_voltage = (self["Emitter"]["barrier"] - self["Collector"]["barrier"] + motive * physical_constants["boltzmann"] * self["Emitter"]["temp"]) / physical_constants["electron_charge"]

        return {"output_voltage": output_voltage, "output_current_density": output_current_density}


    def critical_point_target_function(self, output_current_density):
        """
        Target function for critical point rootfinder.
        """
        position = -self.calc_interelectrode_spacing() * ((2 * np.pi * physical_constants["electron_mass"] * physical_constants["electron_charge"]**2) / (physical_constants["permittivity0"]**2 * physical_constants["boltzmann"]**3))**(1.0/4) * (output_current_density**(1.0/2))/(self["Emitter"]["temp"]**(3.0/4))

        if output_current_density == 0:
            motive = np.inf
        else:
            motive = np.log(self["Emitter"].calc_saturation_current_density()/output_current_density)

        return position - self["motive_data"]["dps"].get_position(motive)

    def output_voltage_target_function(self, output_current_density):
        """
        Target function for the output voltage rootfinder.
        """
        # For brevity, "dimensionless" prefix omitted from "position" and "motive" variable names.
        em_motive = np.log(self["Emitter"].calc_saturation_current_density()/output_current_density)
        em_position = self["motive_data"]["dps"].get_position(em_motive)

        x0 = ((physical_constants["permittivity0"]**2 * physical_constants["boltzmann"]**3) / (2*np.pi*physical_constants["electron_mass"]*physical_constants["electron_charge"]**2))**(1./4) * self["Emitter"]["temp"]**(3./4) / output_current_density**(1./2)

        co_position = self.calc_interelectrode_spacing()/x0 + em_position
        co_motive = self["motive_data"]["dps"].get_motive(co_position)

        return self.calc_output_voltage() - ((self["Emitter"]["barrier"] + em_motive * physical_constants["boltzmann"] * self["Emitter"]["temp"]) - (self["Collector"]["barrier"] + co_motive * physical_constants["boltzmann"] * self["Emitter"]["temp"])) / physical_constants["electron_charge"]
