# -*- coding: utf-8 -*-
import numpy as np
from astropy import units
from tec.electrode import Radioisotope_Emitter
import unittest
import copy

# Values for Si taken from Streetman & Banerjee 9780130255389.
input_params = {"temp": 300.,
                "barrier": 1.0,
                "richardson": 100.0,

                "electron_effective_mass": 9.84e-31,
                "hole_effective_mass": 7.38e-31,
                "acceptor_concentration": 1e18,
                "acceptor_ionization_energy": 45.,
                "donor_concentration": 1e18,
                "donor_ionization_energy": 45.,
                "bandgap": 1.11,

                "inner_radius": 1.,
                "shell_thickness": 1.,
                "specific_activity": 1.,
                "radioisotope_density": 1.,
                "beta_energy": 1., }


# Base classes
# ============
class Base(unittest.TestCase):
    """
    Base class for tests

    This class is intended to be subclassed so that the same `setUp` method does not have to be rewritten for each class containing tests.
    """
    def setUp(self):
        """
        Create dict attribute that can instantiate an `SC` object
        """
        self.input_params = copy.copy(input_params)
        self.el = Radioisotope_Emitter(**input_params)


# Test classes
# ============
class Instantiation(Base):
    """
    Tests all aspects of instantiation

    Tests include: instantiation with args of wrong type, instantiation with input values outside constraints, etc.
    """
    # Input arguments wrong type
    # ==========================
    def test_inner_radius_non_numeric(self):
        """
        Radioisotope_Emitter instantiation requires numeric `inner_radius` value
        """
        self.input_params["inner_radius"] = "this string is non-numeric."

        try:
            El = Radioisotope_Emitter(**self.input_params)
        except TypeError:
            # Attempting to instantiate a `tec.electrode.Radioisotope_Emitter` with a non-numeric `inner_radius` argument raised a TypeError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`inner_radius` field of instantiating dict must be numeric.")

    def test_shell_thickness_non_numeric(self):
        """
        Radioisotope_Emitter instantiation requires numeric `shell_thickness` value
        """
        self.input_params["shell_thickness"] = "this string is non-numeric."

        try:
            El = Radioisotope_Emitter(**self.input_params)
        except TypeError:
            # Attempting to instantiate a `tec.electrode.Radioisotope_Emitter` with a non-numeric `shell_thickness` argument raised a TypeError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`shell_thickness` field of instantiating dict must be numeric.")

    def test_specific_activity_non_numeric(self):
        """
        Radioisotope_Emitter instantiation requires numeric `specific_activity` value
        """
        self.input_params["specific_activity"] = "this string is non-numeric."

        try:
            El = Radioisotope_Emitter(**self.input_params)
        except TypeError:
            # Attempting to instantiate a `tec.electrode.Radioisotope_Emitter` with a non-numeric `specific_activity` argument raised a TypeError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`specific_activity` field of instantiating dict must be numeric.")

    def test_radioisotope_density_non_numeric(self):
        """
        Radioisotope_Emitter instantiation requires numeric `radioisotope_density` value
        """
        self.input_params["radioisotope_density"] = "this string is non-numeric."

        try:
            El = Radioisotope_Emitter(**self.input_params)
        except TypeError:
            # Attempting to instantiate a `tec.electrode.Radioisotope_Emitter` with a non-numeric `radioisotope_density` argument raised a TypeError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`radioisotope_density` field of instantiating dict must be numeric.")

    def test_beta_energy_non_numeric(self):
        """
        Radioisotope_Emitter instantiation requires numeric `beta_energy` value
        """
        self.input_params["beta_energy"] = "this string is non-numeric."

        try:
            El = Radioisotope_Emitter(**self.input_params)
        except TypeError:
            # Attempting to instantiate a `tec.electrode.Radioisotope_Emitter` with a non-numeric `beta_energy` argument raised a TypeError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`beta_energy` field of instantiating dict must be numeric.")


    # Input arguments outside constraints
    # ===================================
    def test_inner_radius_less_than_zero(self):
        """
        Radioisotope_Emitter instantiation requires `inner_radius` > 0.
        """
        self.input_params["inner_radius"] = -1.1
        self.assertRaises(ValueError, Radioisotope_Emitter, **self.input_params)

    def test_shell_thickness_less_than_zero(self):
        """
        Radioisotope_Emitter instantiation requires `shell_thickness` > 0.
        """
        self.input_params["shell_thickness"] = -1.1
        self.assertRaises(ValueError, Radioisotope_Emitter, **self.input_params)

    def test_specific_activity_less_than_zero(self):
        """
        Radioisotope_Emitter instantiation requires `specific_activity` > 0.
        """
        self.input_params["specific_activity"] = -1.1
        self.assertRaises(ValueError, Radioisotope_Emitter, **self.input_params)

    def test_radioisotope_density_less_than_zero(self):
        """
        Radioisotope_Emitter instantiation requires `radioisotope_density` > 0.
        """
        self.input_params["radioisotope_density"] = -1.1
        self.assertRaises(ValueError, Radioisotope_Emitter, **self.input_params)

    def test_beta_energy_less_than_zero(self):
        """
        Radioisotope_Emitter instantiation requires `beta_energy` > 0.
        """
        self.input_params["beta_energy"] = -1.1
        self.assertRaises(ValueError, Radioisotope_Emitter, **self.input_params)


class Set(Base):
    """
    Tests all aspects of setting attributes

    Tests include: setting attributes of wrong type, setting attributes outside their constraints, etc.
    """
    # Set attribute wrong type
    # ========================
    def test_inner_radius_non_numeric(self):
        """
        Radioisotope_Emitter can only set `inner_radius` with numeric value.
        """
        non_num = "this string is non-numeric."
        try:
            self.el.inner_radius = non_num
        except TypeError:
            # Setting `inner_radius` as a type that isn't numeric should raise a TypeError, so things are working.
            pass
        else:
            self.fail("`inner_radius` attribute can be assigned a non-numeric value.")

    def test_shell_thickness_non_numeric(self):
        """
        Radioisotope_Emitter can only set `shell_thickness` with numeric value.
        """
        non_num = "this string is non-numeric."
        try:
            self.el.shell_thickness = non_num
        except TypeError:
            # Setting `shell_thickness` as a type that isn't numeric should raise a TypeError, so things are working.
            pass
        else:
            self.fail("`shell_thickness` attribute can be assigned a non-numeric value.")

    def test_specific_activity_non_numeric(self):
        """
        Radioisotope_Emitter can only set `specific_activity` with numeric value.
        """
        non_num = "this string is non-numeric."
        try:
            self.el.specific_activity = non_num
        except TypeError:
            # Setting `specific_activity` as a type that isn't numeric should raise a TypeError, so things are working.
            pass
        else:
            self.fail("`specific_activity` attribute can be assigned a non-numeric value.")

    def test_radioisotope_density_non_numeric(self):
        """
        Radioisotope_Emitter can only set `radioisotope_density` with numeric value.
        """
        non_num = "this string is non-numeric."
        try:
            self.el.radioisotope_density = non_num
        except TypeError:
            # Setting `radioisotope_density` as a type that isn't numeric should raise a TypeError, so things are working.
            pass
        else:
            self.fail("`radioisotope_density` attribute can be assigned a non-numeric value.")

    def test_beta_energy_non_numeric(self):
        """
        Radioisotope_Emitter can only set `beta_energy` with numeric value.
        """
        non_num = "this string is non-numeric."
        try:
            self.el.beta_energy = non_num
        except TypeError:
            # Setting `beta_energy` as a type that isn't numeric should raise a TypeError, so things are working.
            pass
        else:
            self.fail("`beta_energy` attribute can be assigned a non-numeric value.")


    # Set attribute outside constraint
    # ================================
    def test_inner_radius_less_than_zero(self):
        """
        Radioisotope_Emitter must set `inner_radius` > 0.
        """
        try:
            self.el.inner_radius = -1.1
        except ValueError:
            # Attempting to set the `inner_radius` attribute with a negative value raised a ValueError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`inner_radius` attribute can be assigned a negative value.")

    def test_shell_thickness_less_than_zero(self):
        """
        Radioisotope_Emitter must set `shell_thickness` > 0.
        """
        try:
            self.el.shell_thickness = -1.1
        except ValueError:
            # Attempting to set the `shell_thickness` attribute with a negative value raised a ValueError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`shell_thickness` attribute can be assigned a negative value.")

    def test_specific_activity_less_than_zero(self):
        """
        Radioisotope_Emitter must set `specific_activity` > 0.
        """
        try:
            self.el.specific_activity = -1.1
        except ValueError:
            # Attempting to set the `specific_activity` attribute with a negative value raised a ValueError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`specific_activity` attribute can be assigned a negative value.")

    def test_radioisotope_density_less_than_zero(self):
        """
        Radioisotope_Emitter must set `radioisotope_density` > 0.
        """
        try:
            self.el.radioisotope_density = -1.1
        except ValueError:
            # Attempting to set the `radioisotope_density` attribute with a negative value raised a ValueError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`radioisotope_density` attribute can be assigned a negative value.")

    def test_beta_energy_less_than_zero(self):
        """
        Radioisotope_Emitter must set `beta_energy` > 0.
        """
        try:
            self.el.beta_energy = -1.1
        except ValueError:
            # Attempting to set the `beta_energy` attribute with a negative value raised a ValueError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`beta_energy` attribute can be assigned a negative value.")


class MethodsReturnType(Base):
    """
    Tests methods' output types
    """
    def test_radioisotope_volume(self):
        """
        radioisotope_volume should return an astropy.units.Quantity
        """
        self.assertIsInstance(self.el.radioisotope_volume(), units.Quantity)

    def test_radioisotope_surface_area(self):
        """
        radioisotope_surface_area should return an astropy.units.Quantity
        """
        self.assertIsInstance(self.el.radioisotope_surface_area(), units.Quantity)

    def test_shell_surface_area(self):
        """
        shell_surface_area should return an astropy.units.Quantity
        """
        self.assertIsInstance(self.el.shell_surface_area(), units.Quantity)

    def test_beta_power(self):
        """
        beta_power should return an astropy.units.Quantity
        """
        self.assertIsInstance(self.el.beta_power(), units.Quantity)

    def test_radioisotope_photopower(self):
        """
        radioisotope_photopower should return an astropy.units.Quantity
        """
        self.assertIsInstance(self.el.radioisotope_photopower(), units.Quantity)

    def test_shell_photopower(self):
        """
        shell_photopower should return an astropy.units.Quantity
        """
        self.assertIsInstance(self.el.shell_photopower(), units.Quantity)

    def test_photopower(self):
        """
        photopower should return an astropy.units.Quantity
        """
        self.assertIsInstance(self.el.photopower(), units.Quantity)

    def test_thermoelectron_power(self):
        """
        thermoelectron_power should return an astropy.units.Quantity
        """
        self.assertIsInstance(self.el.thermoelectron_power(), units.Quantity)

    def test_beta_efficiency(self):
        """
        beta_efficiency should return a float
        """
        self.assertIsInstance(self.el.beta_efficiency(), float)


class MethodsReturnUnits(Base):
    """
    Tests methods' output units where applicable
    """
    def test_radioisotope_volume(self):
        """
        radioisotope_volume should return a value with unit um3
        """
        self.assertEqual(self.el.radioisotope_volume().unit, units.Unit("um3"))

    def test_radioisotope_surface_area(self):
        """
        radioisotope_surface_area should return a value with unit um2
        """
        self.assertEqual(self.el.radioisotope_surface_area().unit, units.Unit("um2"))

    def test_shell_surface_area(self):
        """
        shell_surface_area should return a value with unit um2
        """
        self.assertEqual(self.el.shell_surface_area().unit, units.Unit("um2"))

    def test_beta_power(self):
        """
        beta_power should return a value with unit W
        """
        self.assertEqual(self.el.beta_power().unit, units.Unit("W"))

    def test_radioisotope_photopower(self):
        """
        radioisotope_photopower should return a value with unit W
        """
        self.assertEqual(self.el.radioisotope_photopower().unit, units.Unit("W"))

    def test_shell_photopower(self):
        """
        shell_photopower should return a value with unit W
        """
        self.assertEqual(self.el.shell_photopower().unit, units.Unit("W"))

    def test_photopower(self):
        """
        photopower should return a value with unit W
        """
        self.assertEqual(self.el.photopower().unit, units.Unit("W"))

    def test_thermoelectron_power(self):
        """
        thermoelectron_power should return a value with unit W
        """
        self.assertEqual(self.el.thermoelectron_power().unit, units.Unit("W"))


class MethodsReturnValues(Base):
    """
    Tests values of methods against known values
    """
    pass
