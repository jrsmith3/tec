# -*- coding: utf-8 -*-

import numpy as np
from scipy import optimize
from astropy import units, constants
from metal import Metal
from physicalproperty import PhysicalProperty, find_PhysicalProperty


class TB(Metal):
    """
    Tunnel barrier collector electrode

    A `TB` electrode consists of a thin tunnel barrier layer deposited on a metallic substrate. The tunnel barrier layer features negative electron affinity (NEA) such that the vacuum level of the surface of the tunnel barrier layer exists at a lower energy state than the conduction band minimum. Thus, an electron arriving at the electrode from a point outside the electrode can tunnel through the barrier into the bulk even if the electron's energy is below the conduction band minimum.

    :param temp: Temperature (:math:`T`).
    :param barrier: Offset from the conduction band minimum of the tunnel barrier layer to the Fermi level of the bulk. NOTE: this quantity *is not* the work function of the material.
    :param richardson: Richardson's constant. (:math:`A`)
    :param thickness: Tunnel barrier layer thickness. (:math:`t`)
    :param nea: Negative electron affinity. Note this quantity is measured from the vacuum energy to the conduction band minimum; therefore its sign is opposite of other band or motive quantities. A positive value of `nea` determines the amount by which the vacuum level is *below* the conduction band minimum. (:math:`t`)
    """

    thickness = PhysicalProperty(unit="nm", lo_bnd=0)
    nea = PhysicalProperty(unit="eV", lo_bnd=0)

    def __init__(self, temp, barrier, richardson, thickness, nea, voltage=0, position=0, emissivity=0):
        self.temp = temp
        self.barrier = barrier
        self.richardson = richardson
        self.thickness = thickness
        self.nea = nea
        self.voltage = voltage
        self.position = position
        self.emissivity = emissivity

    def transmission_coeff(self, electron_energy):
        """
        Value of transmission coefficient for a square barrier

        :param electron_energy: Energy of electron incident on the tunnel barrier in units of eV.
        """
        electron_energy = units.Quantity(electron_energy, "eV")

        if electron_energy < 0:
            raise ValueError("electron energy must be > 0.")

        exponent = (2 * self.thickness)/(constants.hbar) * np.sqrt(2 * constants.m_e * (self.barrier - electron_energy))

        return np.exp(- exponent.decompose()).value

    def motive(self):
        """
        Motive just outside electrode

        The motive just outside the electrode is the position of the vacuum energy relative to electrical ground. The motive in this case is expressed by

        .. math::
            \psi = \phi + e * V - \chi

        where :math:`\psi` is the motive just outside the electrode, :math:`\phi` is the barrier of the electrode, :math:`e` is the charge of an electron, :math:`V` is the bias of the electrode measured relative to electrical ground, and :math:`\chi` is the negative electron afffinity of the material. Note that :math:`V` is the bias voltage (represented by this class's `voltage` attribute) *and not* the output voltage of a TEC in which this electrode is an attribute.

        :returns: `astropy.units.Quantity` in units of :math:`eV`.
        :symbol: :math:`\psi_{E}` (for the emitter, for example)
        """
        # I could call the parent class's `motive` method here and modify it by subtracting `self.nea`.
        motive = self.barrier + constants.e.si * self.voltage - self.nea
        return motive.to("eV")
