# -*- coding: utf-8 -*-

import inspect
import numpy as np
from scipy import optimize
from astropy import units, constants
from tec.electrode import Metal, TB
from tec import TECBase


class Simple_TB(TECBase):
    """
    Dumb model of TEC with tunnel barrier collector

    This model is a rudimentary model of electron transport across a TEC including a collector electrode featuring a tunnel barrier with negative electron affinity (NEA). It is assumed that all thermoelectrons emitted from the emitter are monoenergetic with energy equal to the vacuum energy of the emitter. This model ignores the negative space charge effect and any thermoelectron emission from the collector back to the emitter. The output current density is determined by multiplying the thermoelectron current density from the emitter by the transmission coefficient of the tunnel barrier.

    Since the thermoelectrons from the emitter are assumed to be monoenergetic, the output current density of the TEC will be zero when the Fermi energy of the collector is coincident with the vacuum energy of the emitter.


    :param tec.electrode.Metal emitter: Emitter electrode.
    :param tec.electrode.TB collector: Collector electrode.
    """

    @property
    def collector(self):
        return self._collector

    @collector.setter
    def collector(self, value):
        if TB not in inspect.getmro(value.__class__):
            raise TypeError("Cannot set 'collector' with non-TB electrode.")
        else:
            self._collector = value

    # Methods regarding current and power -----------------------------
    def forward_current_density(self):
        """
        Net current absorbed by collector from emitter

        This quantity is the current density absorbed through the tunnel barrier of the collector into the collector's bulk. It is obtained by multiplying the emitter thermoelectron current by the transmission coefficient of the collector.

        :returns: `astropy.units.Quantity` in units of :math:`A cm^{-2}`.
        :symbol: :math:`J_{f}`
        """
        electron_energy = self.emitter.motive() - self.collector.motive()

        if electron_energy < 0:
            current_density = units.Quantity(0, "A/cm2")
        else:
            current_density = self.emitter.thermoelectron_current_density() * self.collector.transmission_coeff(electron_energy)

        return current_density

    def back_current_density(self):
        """
        Net current moving from collector to emitter

        In this model, the back current density is 0 by definition.

        :returns: `astropy.units.Quantity` in units of :math:`A cm^{-2}`.
        :symbol: :math:`J_{b}`
        """
        current_density = units.Quantity(0., "A/cm2")
