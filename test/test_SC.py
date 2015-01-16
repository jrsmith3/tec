# -*- coding: utf-8 -*-
import numpy as np
from tec.electrode import SC
from astropy.units import Quantity
from astropy.units import Unit
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
                "bandgap": 1.11}


# Base classes
# ============
class TestBaseJustInputParams(unittest.TestCase):
    """
    Base class for tests

    This class defines a common setUp method that features an attribute which can be used to instantiate `SC` objects.
    """
    def setUp(self):
        """
        Create dict attribute that can instantiate an `SC` object
        """
        self.input_params = copy.copy(input_params)


class TestBaseWithElectrode(unittest.TestCase):
    """
    Base class for tests

    This class defines a common setUp method that features an attribute which is an `SC` object.
    """
    def setUp(self):
        """
        Set up an `SC` object
        """
        self.El = SC(**input_params)


# Test classes
# ============
class InstantiationInputArgsWrongType(TestBaseJustInputParams):
    """
    Test instantiation with non-numeric args
    """
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


class InstantiationInputOutsideConstraints(TestBaseJustInputParams):
    """
    Tests instantiating when input dict values are outside their constraints.

    See the Electrode class docstring for information about the constraints on
    the input data.
    """
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

    def test_bandgap_less_than_zero(self):
        """
        SC instantiation requires `bandgap` > 0.
        """
        self.input_params["bandgap"] = -1.1
        self.assertRaises(ValueError, SC, **self.input_params)


class SetAttribsWrongType(TestBaseWithElectrode):
    """
    Tests setting attributes when input data is non-numeric.
    """
    def test_electron_effective_mass_non_numeric(self):
        """
        SC can only set `electron_effective_mass` with numeric value.
        """
        non_num = "this string is non-numeric."
        try:
            self.El.electron_effective_mass = non_num
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
            self.El.hole_effective_mass = non_num
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
            self.El.acceptor_concentration = non_num
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
            self.El.acceptor_ionization_energy = non_num
        except TypeError:
            # Setting `acceptor_ionization_energy` as a type that isn't numeric should raise a TypeError, so things are working.
            pass
        else:
            self.fail("`acceptor_ionization_energy` attribute can be assigned a non-numeric value.")

    def test_bandgap_non_numeric(self):
        """
        SC can only set `bandgap` with numeric value.
        """
        non_num = "this string is non-numeric."
        try:
            self.El.bandgap = non_num
        except TypeError:
            # Setting `bandgap` as a type that isn't numeric should raise a TypeError, so things are working.
            pass
        else:
            self.fail("`bandgap` attribute can be assigned a non-numeric value.")


class SetAttribsOutsideConstraints(TestBaseWithElectrode):
    """
    Tests setting attributes when input values are outside their constraints.

    See the Electrode class docstring for information about the constraints on
    the data.
    """
    def test_electron_effective_mass_less_than_zero(self):
        """
        SC must set `electron_effective_mass` > 0.
        """
        try:
            self.El.electron_effective_mass = -1.1
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
            self.El.hole_effective_mass = -1.1
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
            self.El.acceptor_concentration = -1.1
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
            self.El.acceptor_ionization_energy = -1.1
        except ValueError:
            # Attempting to set the `acceptor_ionization_energy` attribute with a negative value raised a ValueError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`acceptor_ionization_energy` attribute can be assigned a negative value.")

    def test_bandgap_less_than_zero(self):
        """
        SC must set `bandgap` > 0.
        """
        try:
            self.El.bandgap = -1.1
        except ValueError:
            # Attempting to set the `bandgap` attribute with a negative value raised a ValueError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`bandgap` attribute can be assigned a negative value.")


class CalculatorsReturnType(TestBaseWithElectrode):
    """
    Tests output types of the calculator methods.
    """
    def test_cb_effective_dos_type(self):
        """
        cb_effective_dos should return an astropy.units.Quantity.
        """
        self.assertIsInstance(self.El.cb_effective_dos(), Quantity)

    def test_vb_effective_dos_type(self):
        """
        vb_effective_dos should return an astropy.units.Quantity.
        """
        self.assertIsInstance(self.El.vb_effective_dos(), Quantity)

    def test_electron_concentration_type(self):
        """
        electron_concentration should return an astropy.units.Quantity.
        """
        self.assertIsInstance(self.El.electron_concentration(), Quantity)

    def test_hole_concentration_type(self):
        """
        hole_concentration should return an astropy.units.Quantity.
        """
        self.assertIsInstance(self.El.hole_concentration(), Quantity)

    def test_fermi_energy_type(self):
        """
        fermi_energy should return an astropy.units.Quantity.
        """
        self.assertIsInstance(self.El.fermi_energy(), Quantity)


class CalculatorsReturnUnits(TestBaseWithElectrode):
    """
    Tests output units, where applicable, of the calculator methods.
    """
    def test_cb_effective_dos_unit(self):
        """
        cb_effective_dos should return a value with unit 1/cm3.
        """
        self.assertEqual(self.El.cb_effective_dos().unit, Unit("1/cm3"))

    def test_vb_effective_dos_unit(self):
        """
        vb_effective_dos should return a value with unit 1/cm3.
        """
        self.assertEqual(self.El.vb_effective_dos().unit, Unit("1/cm3"))

    def test_electron_concentration_unit(self):
        """
        electron_concentration should return a value with unit 1/cm3.
        """
        self.assertEqual(self.El.electron_concentration().unit, Unit("1/cm3"))

    def test_hole_concentration_unit(self):
        """
        hole_concentration should return a value with unit 1/cm3.
        """
        self.assertEqual(self.El.hole_concentration().unit, Unit("1/cm3"))

    def test_fermi_energy_unit(self):
        """
        fermi_energy should return a value with unit eV.
        """
        self.assertEqual(self.El.fermi_energy().unit, Unit("eV"))


class CalculatorsReturnValues(TestBaseWithElectrode):
    """
    Tests values of calculator methods against known values.
    """
    pass
