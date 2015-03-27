# -*- coding: utf-8 -*-
import numpy as np
from tec.electrode import SC
from astropy import units
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
                "bandgap": 1.11}


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
        self.el = SC(**input_params)


# Test classes
# ============
class Instantiation(Base):
    """
    Tests all aspects of instantiation

    Tests include: instantiation with args of wrong type, instantiation with input values outside constraints, etc.
    """
    # Input arguments wrong type
    # ==========================
    def test_electron_effective_mass_non_numeric(self):
        """
        SC instantiation requires numeric `electron_effective_mass` value
        """
        self.input_params["electron_effective_mass"] = "this string is non-numeric."

        try:
            El = SC(**self.input_params)
        except TypeError:
            # Attempting to instantiate a `tec.electrode.SC` with a non-numeric `electron_effective_mass` argument raised a TypeError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`electron_effective_mass` field of instantiating dict must be numeric.")

    def test_hole_effective_mass_non_numeric(self):
        """
        SC instantiation requires numeric `hole_effective_mass` value
        """
        self.input_params["hole_effective_mass"] = "this string is non-numeric."

        try:
            El = SC(**self.input_params)
        except TypeError:
            # Attempting to instantiate a `tec.electrode.SC` with a non-numeric `hole_effective_mass` argument raised a TypeError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`hole_effective_mass` field of instantiating dict must be numeric.")

    def test_acceptor_concentration_non_numeric(self):
        """
        SC instantiation requires numeric `acceptor_concentration` value
        """
        self.input_params["acceptor_concentration"] = "this string is non-numeric."

        try:
            El = SC(**self.input_params)
        except TypeError:
            # Attempting to instantiate a `tec.electrode.SC` with a non-numeric `acceptor_concentration` argument raised a TypeError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`acceptor_concentration` field of instantiating dict must be numeric.")

    def test_acceptor_ionization_energy_non_numeric(self):
        """
        SC instantiation requires numeric `acceptor_ionization_energy` value
        """
        self.input_params["acceptor_ionization_energy"] = "this string is non-numeric."

        try:
            El = SC(**self.input_params)
        except TypeError:
            # Attempting to instantiate a `tec.electrode.SC` with a non-numeric `acceptor_ionization_energy` argument raised a TypeError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`acceptor_ionization_energy` field of instantiating dict must be numeric.")

    def test_donor_concentration_non_numeric(self):
        """
        SC instantiation requires numeric `donor_concentration` value
        """
        self.input_params["donor_concentration"] = "this string is non-numeric."

        try:
            El = SC(**self.input_params)
        except TypeError:
            # Attempting to instantiate a `tec.electrode.SC` with a non-numeric `donor_concentration` argument raised a TypeError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`donor_concentration` field of instantiating dict must be numeric.")

    def test_donor_ionization_energy_non_numeric(self):
        """
        SC instantiation requires numeric `donor_ionization_energy` value
        """
        self.input_params["donor_ionization_energy"] = "this string is non-numeric."

        try:
            El = SC(**self.input_params)
        except TypeError:
            # Attempting to instantiate a `tec.electrode.SC` with a non-numeric `donor_ionization_energy` argument raised a TypeError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`donor_ionization_energy` field of instantiating dict must be numeric.")

    def test_bandgap_non_numeric(self):
        """
        SC instantiation requires numeric `bandgap` value
        """
        self.input_params["bandgap"] = "this string is non-numeric."

        try:
            El = SC(**self.input_params)
        except TypeError:
            # Attempting to instantiate a `tec.electrode.SC` with a non-numeric `bandgap` argument raised a TypeError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`bandgap` field of instantiating dict must be numeric.")

    # Input arguments outside constraints
    # ===================================
    def test_electron_effective_mass_less_than_zero(self):
        """
        SC instantiation requires `electron_effective_mass` > 0.
        """
        self.input_params["electron_effective_mass"] = -1.1
        self.assertRaises(ValueError, SC, **self.input_params)

    def test_hole_effective_mass_less_than_zero(self):
        """
        SC instantiation requires `hole_effective_mass` > 0.
        """
        self.input_params["hole_effective_mass"] = -1.1
        self.assertRaises(ValueError, SC, **self.input_params)

    def test_acceptor_concentration_less_than_zero(self):
        """
        SC instantiation requires `acceptor_concentration` > 0.
        """
        self.input_params["acceptor_concentration"] = -1.1
        self.assertRaises(ValueError, SC, **self.input_params)

    def test_acceptor_ionization_energy_less_than_zero(self):
        """
        SC instantiation requires `acceptor_ionization_energy` > 0.
        """
        self.input_params["acceptor_ionization_energy"] = -1.1
        self.assertRaises(ValueError, SC, **self.input_params)

    def test_donor_concentration_less_than_zero(self):
        """
        SC instantiation requires `donor_concentration` > 0.
        """
        self.input_params["donor_concentration"] = -1.1
        self.assertRaises(ValueError, SC, **self.input_params)

    def test_donor_ionization_energy_less_than_zero(self):
        """
        SC instantiation requires `donor_ionization_energy` > 0.
        """
        self.input_params["donor_ionization_energy"] = -1.1
        self.assertRaises(ValueError, SC, **self.input_params)

    def test_bandgap_less_than_zero(self):
        """
        SC instantiation requires `bandgap` > 0.
        """
        self.input_params["bandgap"] = -1.1
        self.assertRaises(ValueError, SC, **self.input_params)


class Set(Base):
    """
    Tests all aspects of setting attributes

    Tests include: setting attributes of wrong type, setting attributes outside their constraints, etc.
    """
    # Set attribute wrong type
    # ========================
    def test_electron_effective_mass_non_numeric(self):
        """
        SC can only set `electron_effective_mass` with numeric value.
        """
        non_num = "this string is non-numeric."
        try:
            self.el.electron_effective_mass = non_num
        except TypeError:
            # Setting `electron_effective_mass` as a type that isn't numeric should raise a TypeError, so things are working.
            pass
        else:
            self.fail("`electron_effective_mass` attribute can be assigned a non-numeric value.")

    def test_hole_effective_mass_non_numeric(self):
        """
        SC can only set `hole_effective_mass` with numeric value.
        """
        non_num = "this string is non-numeric."
        try:
            self.el.hole_effective_mass = non_num
        except TypeError:
            # Setting `hole_effective_mass` as a type that isn't numeric should raise a TypeError, so things are working.
            pass
        else:
            self.fail("`hole_effective_mass` attribute can be assigned a non-numeric value.")

    def test_acceptor_concentration_non_numeric(self):
        """
        SC can only set `acceptor_concentration` with numeric value.
        """
        non_num = "this string is non-numeric."
        try:
            self.el.acceptor_concentration = non_num
        except TypeError:
            # Setting `acceptor_concentration` as a type that isn't numeric should raise a TypeError, so things are working.
            pass
        else:
            self.fail("`acceptor_concentration` attribute can be assigned a non-numeric value.")

    def test_acceptor_ionization_energy_non_numeric(self):
        """
        SC can only set `acceptor_ionization_energy` with numeric value.
        """
        non_num = "this string is non-numeric."
        try:
            self.el.acceptor_ionization_energy = non_num
        except TypeError:
            # Setting `acceptor_ionization_energy` as a type that isn't numeric should raise a TypeError, so things are working.
            pass
        else:
            self.fail("`acceptor_ionization_energy` attribute can be assigned a non-numeric value.")

    def test_donor_concentration_non_numeric(self):
        """
        SC can only set `donor_concentration` with numeric value.
        """
        non_num = "this string is non-numeric."
        try:
            self.el.donor_concentration = non_num
        except TypeError:
            # Setting `donor_concentration` as a type that isn't numeric should raise a TypeError, so things are working.
            pass
        else:
            self.fail("`donor_concentration` attribute can be assigned a non-numeric value.")

    def test_donor_ionization_energy_non_numeric(self):
        """
        SC can only set `donor_ionization_energy` with numeric value.
        """
        non_num = "this string is non-numeric."
        try:
            self.el.donor_ionization_energy = non_num
        except TypeError:
            # Setting `donor_ionization_energy` as a type that isn't numeric should raise a TypeError, so things are working.
            pass
        else:
            self.fail("`donor_ionization_energy` attribute can be assigned a non-numeric value.")

    def test_bandgap_non_numeric(self):
        """
        SC can only set `bandgap` with numeric value.
        """
        non_num = "this string is non-numeric."
        try:
            self.el.bandgap = non_num
        except TypeError:
            # Setting `bandgap` as a type that isn't numeric should raise a TypeError, so things are working.
            pass
        else:
            self.fail("`bandgap` attribute can be assigned a non-numeric value.")

    # Set attribute outside constraint
    # ================================
    def test_electron_effective_mass_less_than_zero(self):
        """
        SC must set `electron_effective_mass` > 0.
        """
        try:
            self.el.electron_effective_mass = -1.1
        except ValueError:
            # Attempting to set the `electron_effective_mass` attribute with a negative value raised a ValueError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`electron_effective_mass` attribute can be assigned a negative value.")

    def test_hole_effective_mass_less_than_zero(self):
        """
        SC must set `hole_effective_mass` > 0.
        """
        try:
            self.el.hole_effective_mass = -1.1
        except ValueError:
            # Attempting to set the `hole_effective_mass` attribute with a negative value raised a ValueError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`hole_effective_mass` attribute can be assigned a negative value.")

    def test_acceptor_concentration_less_than_zero(self):
        """
        SC must set `acceptor_concentration` > 0.
        """
        try:
            self.el.acceptor_concentration = -1.1
        except ValueError:
            # Attempting to set the `acceptor_concentration` attribute with a negative value raised a ValueError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`acceptor_concentration` attribute can be assigned a negative value.")

    def test_acceptor_ionization_energy_less_than_zero(self):
        """
        SC must set `acceptor_ionization_energy` > 0.
        """
        try:
            self.el.acceptor_ionization_energy = -1.1
        except ValueError:
            # Attempting to set the `acceptor_ionization_energy` attribute with a negative value raised a ValueError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`acceptor_ionization_energy` attribute can be assigned a negative value.")

    def test_donor_concentration_less_than_zero(self):
        """
        SC must set `donor_concentration` > 0.
        """
        try:
            self.el.donor_concentration = -1.1
        except ValueError:
            # Attempting to set the `donor_concentration` attribute with a negative value raised a ValueError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`donor_concentration` attribute can be assigned a negative value.")

    def test_donor_ionization_energy_less_than_zero(self):
        """
        SC must set `donor_ionization_energy` > 0.
        """
        try:
            self.el.donor_ionization_energy = -1.1
        except ValueError:
            # Attempting to set the `donor_ionization_energy` attribute with a negative value raised a ValueError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`donor_ionization_energy` attribute can be assigned a negative value.")

    def test_bandgap_less_than_zero(self):
        """
        SC must set `bandgap` > 0.
        """
        try:
            self.el.bandgap = -1.1
        except ValueError:
            # Attempting to set the `bandgap` attribute with a negative value raised a ValueError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`bandgap` attribute can be assigned a negative value.")


class MethodsReturnType(Base):
    """
    Tests methods' output types
    """
    def test_cb_effective_dos(self):
        """
        cb_effective_dos should return an astropy.units.Quantity.
        """
        self.assertIsInstance(self.el.cb_effective_dos(), units.Quantity)

    def test_vb_effective_dos(self):
        """
        vb_effective_dos should return an astropy.units.Quantity.
        """
        self.assertIsInstance(self.el.vb_effective_dos(), units.Quantity)

    def test_electron_concentration(self):
        """
        electron_concentration should return an astropy.units.Quantity.
        """
        self.assertIsInstance(self.el.electron_concentration(), units.Quantity)

    def test_hole_concentration(self):
        """
        hole_concentration should return an astropy.units.Quantity.
        """
        self.assertIsInstance(self.el.hole_concentration(), units.Quantity)

    def test_fermi_energy(self):
        """
        fermi_energy should return an astropy.units.Quantity.
        """
        self.assertIsInstance(self.el.fermi_energy(), units.Quantity)

    def test_photon_flux(self):
        """
        Metal.photon_flux should return an astropy.units.Quantity
        """
        self.assertIsInstance(self.el.photon_flux(), units.Quantity)

    def test_photon_energy_flux(self):
        """
        Metal.photon_energy_flux should return an astropy.units.Quantity
        """
        self.assertIsInstance(self.el.photon_energy_flux(), units.Quantity)


class MethodsReturnUnits(Base):
    """
    Tests methods' output units where applicable
    """
    def test_cb_effective_dos(self):
        """
        cb_effective_dos should return a value with unit 1/cm3.
        """
        self.assertEqual(self.el.cb_effective_dos().unit, units.Unit("1/cm3"))

    def test_vb_effective_dos(self):
        """
        vb_effective_dos should return a value with unit 1/cm3.
        """
        self.assertEqual(self.el.vb_effective_dos().unit, units.Unit("1/cm3"))

    def test_electron_concentration(self):
        """
        electron_concentration should return a value with unit 1/cm3.
        """
        self.assertEqual(self.el.electron_concentration().unit, units.Unit("1/cm3"))

    def test_hole_concentration(self):
        """
        hole_concentration should return a value with unit 1/cm3.
        """
        self.assertEqual(self.el.hole_concentration().unit, units.Unit("1/cm3"))

    def test_fermi_energy(self):
        """
        fermi_energy should return a value with unit eV.
        """
        self.assertEqual(self.el.fermi_energy().unit, units.Unit("eV"))

    def test_photon_flux(self):
        """
        SC.photon_flux should return a value with unit W/cm2
        """
        self.assertEqual(self.el.photon_flux().unit, units.Unit("1/(s*cm2)"))

    def test_photon_energy_flux(self):
        """
        SC.photon_energy_flux should return a value with unit 1/(s*cm2)
        """
        self.assertEqual(self.el.photon_energy_flux().unit, units.Unit("W/cm2"))


class MethodsReturnValues(Base):
    """
    Tests values of methods against known values
    """
    pass
