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
                "bandgap": 1.11,}


# Base classes
# ============
class TestBaseJustInputParams(unittest.TestCase):
    """
    Base class for tests.

    This class defines a common setUp method that features an attribute which can be used to instantiate `SC` objects.
    """
    def setUp(self):
        """
        Set up a dictionary that can properly instantiate an `SC` object.
        """
        self.input_params = copy.copy(input_params)


class TestBaseWithElectrode(unittest.TestCase):
    """
    Base class for tests.

    This class defines a common setUp method that features an attribute which is an `Electrode` object.
    """
    def setUp(self):
        """
        Set up an `SC` object.
        """
        self.El = SC(copy.copy(input_params))


# Test classes
# ============
class InstantiationInputNonDict(unittest.TestCase):
    """
    Tests instantiation when non-dict data is used.
    """
    def test_no_input_arg(self):
        """
        SC instantiation without input argument is invalid.
        """
        self.assertRaises(TypeError, SC, None)

    def test_non_dict_input_arg(self):
        """
        SC instantiation with non-dict input argument is invalid.
        """
        self.assertRaises(TypeError, SC, "this string is not a dict.")


class InstantiationInputIncomplete(TestBaseJustInputParams):
    """
    Tests instantiation when non-dict data is used.
    """
    def test_temp_missing(self):
        """
        SC instantiating dict requires `temp` key.
        """
        del(self.input_params["temp"])
        self.assertRaises(KeyError, SC, self.input_params)

    def test_barrier_missing(self):
        """
        SC instantiating dict requires `barrier` key.
        """
        del(self.input_params["barrier"])
        self.assertRaises(KeyError, SC, self.input_params)

    def test_richardson_missing(self):
        """
        SC instantiating dict requires `richardson` key.
        """
        del(self.input_params["richardson"])
        self.assertRaises(KeyError, SC, self.input_params)

    def test_electron_effective_mass_missing(self):
        """
        SC instantiating dict requires `electron_effective_mass` key.
        """
        del(self.input_params["electron_effective_mass"])
        self.assertRaises(KeyError, SC, self.input_params)

    def test_hole_effective_mass_missing(self):
        """
        SC instantiating dict requires `hole_effective_mass` key.
        """
        del(self.input_params["hole_effective_mass"])
        self.assertRaises(KeyError, SC, self.input_params)

    def test_acceptor_concentration_missing(self):
        """
        SC instantiating dict requires `acceptor_concentration` key.
        """
        del(self.input_params["acceptor_concentration"])
        self.assertRaises(KeyError, SC, self.input_params)

    def test_acceptor_ionization_energy_missing(self):
        """
        SC instantiating dict requires `acceptor_ionization_energy` key.
        """
        del(self.input_params["acceptor_ionization_energy"])
        self.assertRaises(KeyError, SC, self.input_params)

    def test_bandgap_missing(self):
        """
        SC instantiating dict requires `bandgap` key.
        """
        del(self.input_params["bandgap"])
        self.assertRaises(KeyError, SC, self.input_params)


class InstantiationInputSuperfluousKeys(TestBaseJustInputParams):
    """
    SC can be instantiated with dict with superfluous keys.
    """

    def test_SC_input_superfluous_keys(self):
        """Instantiating argument with additional key."""
        self.input_params["superfluous"] = "value not even numeric!"
        try:
            El = SC(self.input_params)
        except:
            self.fail("Superfluous key in input param dict caused failure of instantiation.")


class InstantiationInputFieldsWrongType(TestBaseJustInputParams):
    """
    Tests instantiating when input dict has non-numeric data items.
    """
    def test_electron_effective_mass_non_numeric(self):
        """
        SC instantiation requires numeric `electron_effective_mass` value.
        """
        self.input_params["electron_effective_mass"] = "this string is non-numeric."

        try:
            El = SC(self.input_params)
        except TypeError:
            # Instantiating an SC with a dict with key `electron_effective_mass` having a non-numeric field raised a TypeError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`electron_effective_mass` field of instantiating dict must be numeric.")

    def test_hole_effective_mass_non_numeric(self):
        """
        SC instantiation requires numeric `hole_effective_mass` value.
        """
        self.input_params["hole_effective_mass"] = "this string is non-numeric."

        try:
            El = SC(self.input_params)
        except TypeError:
            # Instantiating an SC with a dict with key `hole_effective_mass` having a non-numeric field raised a TypeError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`hole_effective_mass` field of instantiating dict must be numeric.")

    def test_acceptor_concentration_non_numeric(self):
        """
        SC instantiation requires numeric `acceptor_concentration` value.
        """
        self.input_params["acceptor_concentration"] = "this string is non-numeric."

        try:
            El = SC(self.input_params)
        except TypeError:
            # Instantiating an SC with a dict with key `acceptor_concentration` having a non-numeric field raised a TypeError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`acceptor_concentration` field of instantiating dict must be numeric.")

    def test_acceptor_ionization_energy_non_numeric(self):
        """
        SC instantiation requires numeric `acceptor_ionization_energy` value.
        """
        self.input_params["acceptor_ionization_energy"] = "this string is non-numeric."

        try:
            El = SC(self.input_params)
        except TypeError:
            # Instantiating an SC with a dict with key `acceptor_ionization_energy` having a non-numeric field raised a TypeError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`acceptor_ionization_energy` field of instantiating dict must be numeric.")

    def test_bandgap_non_numeric(self):
        """
        SC instantiation requires numeric `bandgap` value.
        """
        self.input_params["bandgap"] = "this string is non-numeric."

        try:
            El = SC(self.input_params)
        except TypeError:
            # Instantiating an SC with a dict with key `bandgap` having a non-numeric field raised a TypeError which is exactly what we wanted to do.
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
        self.assertRaises(ValueError, SC, self.input_params)

    def test_hole_effective_mass_less_than_zero(self):
        """
        SC instantiation requires `hole_effective_mass` > 0.
        """
        self.input_params["hole_effective_mass"] = -1.1
        self.assertRaises(ValueError, SC, self.input_params)

    def test_acceptor_concentration_less_than_zero(self):
        """
        SC instantiation requires `acceptor_concentration` > 0.
        """
        self.input_params["acceptor_concentration"] = -1.1
        self.assertRaises(ValueError, SC, self.input_params)

    def test_acceptor_ionization_energy_less_than_zero(self):
        """
        SC instantiation requires `acceptor_ionization_energy` > 0.
        """
        self.input_params["acceptor_ionization_energy"] = -1.1
        self.assertRaises(ValueError, SC, self.input_params)

    def test_bandgap_less_than_zero(self):
        """
        SC instantiation requires `bandgap` > 0.
        """
        self.input_params["bandgap"] = -1.1
        self.assertRaises(ValueError, SC, self.input_params)


class SetDataWrongType(TestBaseWithElectrode):
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


class SetDataOutsideConstraints(TestBaseWithElectrode):
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
    def test_calc_cb_effective_dos_type(self):
        """
        calc_cb_effective_dos should return an astropy.units.Quantity.
        """
        self.assertIsInstance(self.El.calc_cb_effective_dos(), Quantity)

    def test_calc_vb_effective_dos_type(self):
        """
        calc_vb_effective_dos should return an astropy.units.Quantity.
        """
        self.assertIsInstance(self.El.calc_vb_effective_dos(), Quantity)

    def test_calc_electron_concentration_type(self):
        """
        calc_electron_concentration should return an astropy.units.Quantity.
        """
        self.assertIsInstance(self.El.calc_electron_concentration(), Quantity)

    def test_calc_hole_concentration_type(self):
        """
        calc_hole_concentration should return an astropy.units.Quantity.
        """
        self.assertIsInstance(self.El.calc_hole_concentration(), Quantity)

    def test_calc_fermi_energy_type(self):
        """
        calc_fermi_energy should return an astropy.units.Quantity.
        """
        self.assertIsInstance(self.El.calc_fermi_energy(), Quantity)


class CalculatorsReturnUnits(TestBaseWithElectrode):
    """
    Tests output units, where applicable, of the calculator methods.
    """
    def test_calc_cb_effective_dos_unit(self):
        """
        calc_cb_effective_dos should return a value with unit 1/cm3.
        """
        self.assertEqual(self.El.calc_cb_effective_dos().unit, Unit("1/cm3"))

    def test_calc_vb_effective_dos_unit(self):
        """
        calc_vb_effective_dos should return a value with unit 1/cm3.
        """
        self.assertEqual(self.El.calc_vb_effective_dos().unit, Unit("1/cm3"))

    def test_calc_electron_concentration_unit(self):
        """
        calc_electron_concentration should return a value with unit 1/cm3.
        """
        self.assertEqual(self.El.calc_electron_concentration().unit, Unit("1/cm3"))

    def test_calc_hole_concentration_unit(self):
        """
        calc_hole_concentration should return a value with unit 1/cm3.
        """
        self.assertEqual(self.El.calc_hole_concentration().unit, Unit("1/cm3"))

    def test_calc_fermi_energy_unit(self):
        """
        calc_fermi_energy should return a value with unit eV.
        """
        self.assertEqual(self.El.calc_fermi_energy().unit, Unit("eV"))


class CalculatorsReturnValues(TestBaseWithElectrode):
    """
    Tests values of calculator methods against known values.
    """
    pass
