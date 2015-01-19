# -*- coding: utf-8 -*-

import numpy as np
from scipy import optimize
from astropy import units, constants
from tec import electrode
from tec import TECBase


class Simple_TB(TECBase):
    """
    Dumb model of TEC with tunnel barrier collector

    This model is a rudimentary model of electron transport across a TEC including a collector electrode featuring a tunnel barrier with negative electron affinity (NEA). It is assumed that all thermoelectrons emitted from the emitter are monoenergetic with energy equal to the vacuum energy of the emitter. This model ignores the negative space charge effect and any thermoelectron emission from the collector back to the emitter. The output current density is determined by multiplying the thermoelectron current density from the emitter by the transmission coefficient of the tunnel barrier.

    Since the thermoelectrons from the emitter are assumed to be monoenergetic, the output current density of the TEC will be zero when the Fermi energy of the collector is coincident with the vacuum energy of the emitter.
    """

    # Methods regarding current and power -----------------------------
    def forward_current_density(self):
        """
        Net current absorbed by collector from emitter

        This quantity is the current density absorbed through the tunnel barrier of the collector into the collector's bulk. It is obtained by multiplying the emitter thermoelectron current by the transmission coefficient of the collector.

        :returns: `astropy.units.Quantity` in units of :math:`A cm^{-2}`.
        :symbol: :math:`J_{f}`
        """
        pass

    def back_current_density(self):
        """
        Net current moving from collector to emitter

        In this model, the back current density is 0 by definition.

        :returns: `astropy.units.Quantity` in units of :math:`A cm^{-2}`.
        :symbol: :math:`J_{b}`
        """
        current_density = units.Quantity(0., "A/cm2")
