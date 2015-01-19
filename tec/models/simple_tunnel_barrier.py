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
    pass
