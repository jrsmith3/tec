# -*- coding: utf-8 -*-

import numpy as np
from scipy import optimize
from astropy import units, constants
from metal import Metal
from physicalproperty import PhysicalProperty, find_PhysicalProperty


def transmission_coeff(thickness, barrier_height, electron_energy):
    """
    Value of transmission coefficient for a square barrier
    """
    exponent = (2 * thickness)/(constants.hbar) * np.sqrt(2 * constants.m_e * (barrier_height - electron_energy))

    return np.exp(- exponent.decompose())


class TB(Metal):
    """
    Tunnel barrier collector electrode

    :param temp: Temperature (:math:`T`).
    :param barrier: Emission barrier (a.k.a. work function). The barrier is the difference between the vacuum energy of the surface and the Fermi energy. (:math:`\phi`)
    :param richardson: Richardson's constant (:math:`A`)
    :param thickness: Barrier thickness (:math:`t`)
    """

    thickness = PhysicalProperty(unit="nm", lo_bnd=0)

    def __init__(self, temp, barrier, richardson, thickness, voltage=0, position=0, emissivity=0):
        self.temp = temp
        self.barrier = barrier
        self.richardson = richardson
        self.thickness = thickness
        self.voltage = voltage
        self.position = position
        self.emissivity = emissivity
