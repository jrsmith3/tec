# -*- coding: utf-8 -*-

import numpy as np
from astropy import units, constants
from semiconductor import SC
from tec.utils import units, geometry
from physicalproperty import PhysicalProperty, find_PhysicalProperty
from ibei import uibei


class Radioisotope_Emitter(SC):
    """
    Spherical radioisotope emitter

    This class models a spherical radioisotope emitter. The emitter is comprised of a spherical mass of radioisotope surrounded by a spherical shell of uniform thickness and composed of semiconductor material. The radioisotope and shell are in good thermal contact and are at the same temperature. The radioisotope experiences beta decay, and the beta electrons lose energy to the combination of radioisotope and semiconductor shell. The shell is sufficiently thick to capture all of the energy carried by the beta electrons.
    """

    inner_radius = PhysicalProperty(unit="um", lo_bnd=0)
    shell_thickness = PhysicalProperty(unit="um", lo_bnd=0)
    specific_activity = PhysicalProperty(unit="Bq/g", lo_bnd=0)
    radioisotope_density = PhysicalProperty(unit="g/cm3", lo_bnd=0)
    beta_energy = PhysicalProperty(unit="keV", lo_bnd=0)

    def __init__(self, temp, barrier, bandgap, inner_radius, shell_thickness, specific_activity, radioisotope_density, beta_energy, richardson=120, electron_effective_mass=constants.m_e, hole_effective_mass=constants.m_e, acceptor_concentration=0, acceptor_ionization_energy=0, donor_concentration=0, donor_ionization_energy=0, voltage=0, position=0, emissivity=0): 
        # `Metal` attributes
        self.temp = temp
        self.barrier = barrier
        self.richardson = richardson
        self.voltage = voltage
        self.position = position
        self.emissivity = emissivity    

        # `SC` attributes
        self.electron_effective_mass = electron_effective_mass
        self.hole_effective_mass = hole_effective_mass
        self.acceptor_concentration = acceptor_concentration
        self.acceptor_ionization_energy = acceptor_ionization_energy
        self.donor_concentration = donor_concentration
        self.donor_ionization_energy = donor_ionization_energy
        self.bandgap = bandgap

        # `Radioisotope_Emitter` attributes
        self.inner_radius = inner_radius
        self.shell_thickness = shell_thickness
        self.specific_activity = specific_activity
        self.radioisotope_density = radioisotope_density
        self.beta_energy = beta_energy

    def radioisotope_volume(self):
        """
        Volume of radioisotope
        """
        vol = geometry.sphere_volume(self.inner_radius)
        return vol.to("um3")

    def radioisotope_surface_area(self):
        """
        Surface area of radioisotope
        """
        area = geometry.sphere_surface_area(self.inner_radius)
        return area.to("um2")

    def shell_surface_area(self):
        """
        Surface area of shell
        """
        radius = self.inner_radius + self.shell_thickness
        area = geometry.sphere_surface_area(radius)
        return area.to("um2")

    def beta_power(self):
        """
        Power carried by beta electrons
        """
        power = self.specific_activity * self.radioisotope_density * self.radioisotope_volume() * self.beta_energy
        return power.to("W")

    def radioisotope_photopower(self):
        """
        Power emitted from radioisotope via thermal photons

        The radioisotope emits thermal photons. Since the radioisotope is surrounded by a semiconductor shell, the thermal photons with energy above the bandgap of the semiconductor are absorbed while photons with energy below the semiconductor bandgap are transmitted through the shell.

        This method calculates the total power radiated from the radioisotope via below-bandgap thermal photons.
        """
        total_photon_energy_flux = uibei(3, 0, self.temp, 0)
        above_bandgap_photon_energy_flux = self.photon_energy_flux()

        below_bandgap_photon_energy_flux = total_photon_energy_flux - above_bandgap_photon_energy_flux

        photopower = below_bandgap_photon_energy_flux * self.radioisotope_surface_area()

        return photopower.to("W")

    def shell_photopower(self):
        """
        Power emitted from shell via thermal photons
        """
        energy_flux = self.photon_energy_flux()
        photopower = energy_flux * self.shell_surface_area()

        return photopower.to("W")

    def photopower(self):
        """
        Power emitted from electrode via thermal photons
        """
        photopower = self.radioisotope_photopower() + self.shell_photopower()
        return photopower.to("W")

    def thermoelectron_power(self):
        """
        Power emitted from the emitter via thermoelectrons
        """
        kt2 = 2 * constants.k_B * self.temp
        thermal_potential = (self.barrier + kt2)/constants.e.to("C")
        power_density = thermal_potential * self.thermoelectron_current_density()
        power = power_density * self.shell_surface_area()

        return power.to("W")

    def beta_efficiency(self):
        """
        Ratio of power lost via thermoelectrons to power added via betas

        The efficiency is the ratio of power emitted from the electrode via thermoelectrons to the power added to the electrode via beta electrons as a result of beta decay. This quantity is a good measure of the efficiency of the process because the photons emitted from the emitter are considered to be lost.
        """
        efficiency = self.thermoelectron_power() / self.beta_power()
        return efficiency.value
