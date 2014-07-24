# -*- coding: utf-8 -*-
import numpy as np
from electrode import SC_Electrode
from astropy.units import Quantity
from astropy.units import Unit
import unittest
import copy

# Values for Si taken from Streetman & Banerjee 9780130255389.
input_params = {"temp": 300.,
                "barrier": 1.0,
                "richardson": 100.0,

                "el_effective_mass": 9.84e-31,
                "ho_effective_mass": 7.38e-31,
                "accept_conc": 1e18,
                "accept_ionization_energy": 45.,
                "bandgap": 1.11,}


# Base classes
# ============
class TestBaseJustInputParams(unittest.TestCase):
    """
    Base class for tests.

    This class defines a common setUp method that features an attribute which can be used to instantiate `SC_Electrode` objects.
    """
    def setUp(self):
        """
        Set up a dictionary that can properly instantiate an `SC_Electrode` object.
        """
        self.input_params = copy.copy(input_params)


class TestBaseWithElectrode(unittest.TestCase):
    """
    Base class for tests.

    This class defines a common setUp method that features an attribute which is an `Electrode` object.
    """
    def setUp(self):
        """
        Set up an `SC_Electrode` object.
        """
        self.El = SC_Electrode(copy.copy(input_params))


# Test classes
# ============
class InstantiationInputNonDict(unittest.TestCase):
    """
    Tests instantiation when non-dict data is used.
    """
    def test_no_input_arg(self):
        """
        SC_Electrode instantiation without input argument is invalid.
        """
        self.assertRaises(TypeError, SC_Electrode, None)

    def test_non_dict_input_arg(self):
        """
        SC_Electrode instantiation with non-dict input argument is invalid.
        """
        self.assertRaises(TypeError, SC_Electrode, "this string is not a dict.")


class InstantiationInputIncomplete(TestBaseJustInputParams):
    """
    Tests instantiation when non-dict data is used.
    """
    def test_temp_missing(self):
        """
        SC_Electrode instantiating dict requires `temp` key.
        """
        del(self.input_params["temp"])
        self.assertRaises(KeyError, SC_Electrode, self.input_params)

    def test_barrier_missing(self):
        """
        SC_Electrode instantiating dict requires `barrier` key.
        """
        del(self.input_params["barrier"])
        self.assertRaises(KeyError, SC_Electrode, self.input_params)

    def test_richardson_missing(self):
        """
        SC_Electrode instantiating dict requires `richardson` key.
        """
        del(self.input_params["richardson"])
        self.assertRaises(KeyError, SC_Electrode, self.input_params)

    def test_el_effective_mass_missing(self):
        """
        SC_Electrode instantiating dict requires `el_effective_mass` key.
        """
        del(self.input_params["el_effective_mass"])
        self.assertRaises(KeyError, SC_Electrode, self.input_params)

    def test_ho_effective_mass_missing(self):
        """
        SC_Electrode instantiating dict requires `ho_effective_mass` key.
        """
        del(self.input_params["ho_effective_mass"])
        self.assertRaises(KeyError, SC_Electrode, self.input_params)

    def test_accept_conc_missing(self):
        """
        SC_Electrode instantiating dict requires `accept_conc` key.
        """
        del(self.input_params["accept_conc"])
        self.assertRaises(KeyError, SC_Electrode, self.input_params)

    def test_accept_ionization_energy_missing(self):
        """
        SC_Electrode instantiating dict requires `accept_ionization_energy` key.
        """
        del(self.input_params["accept_ionization_energy"])
        self.assertRaises(KeyError, SC_Electrode, self.input_params)

    def test_bandgap_missing(self):
        """
        SC_Electrode instantiating dict requires `bandgap` key.
        """
        del(self.input_params["bandgap"])
        self.assertRaises(KeyError, SC_Electrode, self.input_params)


class InstantiationInputSuperfluousKeys(TestBaseJustInputParams):
    """
    SC_Electrode can be instantiated with dict with superfluous keys.
    """

    def test_SC_Electrode_input_superfluous_keys(self):
        """Instantiating argument with additional key."""
        self.input_params["superfluous"] = "value not even numeric!"
        try:
            El = SC_Electrode(self.input_params)
        except:
            self.fail("Superfluous key in input param dict caused failure of instantiation.")


class InstantiationInputFieldsWrongType(TestBaseJustInputParams):
    """
    Tests instantiating when input dict has non-numeric data items.
    """
    def test_el_effective_mass_non_numeric(self):
        """
        SC_Electrode instantiation requires numeric `el_effective_mass` value.
        """
        self.input_params["el_effective_mass"] = "this string is non-numeric."

        try:
            El = SC_Electrode(self.input_params)
        except TypeError:
            # Instantiating an SC_Electrode with a dict with key `el_effective_mass` having a non-numeric field raised a TypeError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`el_effective_mass` field of instantiating dict must be numeric.")

    def test_ho_effective_mass_non_numeric(self):
        """
        SC_Electrode instantiation requires numeric `ho_effective_mass` value.
        """
        self.input_params["ho_effective_mass"] = "this string is non-numeric."

        try:
            El = SC_Electrode(self.input_params)
        except TypeError:
            # Instantiating an SC_Electrode with a dict with key `ho_effective_mass` having a non-numeric field raised a TypeError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`ho_effective_mass` field of instantiating dict must be numeric.")

    def test_accept_conc_non_numeric(self):
        """
        SC_Electrode instantiation requires numeric `accept_conc` value.
        """
        self.input_params["accept_conc"] = "this string is non-numeric."

        try:
            El = SC_Electrode(self.input_params)
        except TypeError:
            # Instantiating an SC_Electrode with a dict with key `accept_conc` having a non-numeric field raised a TypeError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`accept_conc` field of instantiating dict must be numeric.")

    def test_accept_ionization_energy_non_numeric(self):
        """
        SC_Electrode instantiation requires numeric `accept_ionization_energy` value.
        """
        self.input_params["accept_ionization_energy"] = "this string is non-numeric."

        try:
            El = SC_Electrode(self.input_params)
        except TypeError:
            # Instantiating an SC_Electrode with a dict with key `accept_ionization_energy` having a non-numeric field raised a TypeError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`accept_ionization_energy` field of instantiating dict must be numeric.")

    def test_bandgap_non_numeric(self):
        """
        SC_Electrode instantiation requires numeric `bandgap` value.
        """
        self.input_params["bandgap"] = "this string is non-numeric."

        try:
            El = SC_Electrode(self.input_params)
        except TypeError:
            # Instantiating an SC_Electrode with a dict with key `bandgap` having a non-numeric field raised a TypeError which is exactly what we wanted to do.
            pass
        else:
            self.fail("`bandgap` field of instantiating dict must be numeric.")


class InstantiationInputOutsideConstraints(TestBaseJustInputParams):
    """
    Tests instantiating when input dict values are outside their constraints.

    See the Electrode class docstring for information about the constraints on
    the input data.
    """
    pass


class SetDataWrongType(TestBaseWithElectrode):
    """
    Tests setting attributes when input data is non-numeric.
    """
    pass


class SetDataOutsideConstraints(TestBaseWithElectrode):
    """
    Tests setting attributes when input values are outside their constraints.

    See the Electrode class docstring for information about the constraints on
    the data.
    """
    pass


class CalculatorsReturnType(TestBaseWithElectrode):
    """
    Tests output types of the calculator methods.
    """
    def test_calc_cond_band_effective_dos_type(self):
        """
        calc_cond_band_effective_dos should return an astropy.units.Quantity.
        """
        self.assertIsInstance(self.El.calc_cond_band_effective_dos(), Quantity)

    def test_calc_val_band_effective_dos_type(self):
        """
        calc_val_band_effective_dos should return an astropy.units.Quantity.
        """
        self.assertIsInstance(self.El.calc_val_band_effective_dos(), Quantity)

    def test_calc_el_carrier_conc_type(self):
        """
        calc_el_carrier_conc should return an astropy.units.Quantity.
        """
        self.assertIsInstance(self.El.calc_el_carrier_conc(), Quantity)

    def test_calc_ho_carrier_conc_type(self):
        """
        calc_ho_carrier_conc should return an astropy.units.Quantity.
        """
        self.assertIsInstance(self.El.calc_ho_carrier_conc(), Quantity)

    def test_calc_fermi_energy_type(self):
        """
        calc_fermi_energy should return an astropy.units.Quantity.
        """
        self.assertIsInstance(self.El.calc_fermi_energy(), Quantity)


class CalculatorsReturnUnits(TestBaseWithElectrode):
    """
    Tests output units, where applicable, of the calculator methods.
    """
    def test_calc_cond_band_effective_dos_unit(self):
        """
        calc_cond_band_effective_dos should return a value with unit 1/cm3.
        """
        self.assertEqual(self.El.calc_cond_band_effective_dos().unit, Unit("1/cm3"))

    def test_calc_val_band_effective_dos_unit(self):
        """
        calc_val_band_effective_dos should return a value with unit 1/cm3.
        """
        self.assertEqual(self.El.calc_val_band_effective_dos().unit, Unit("1/cm3"))

    def test_calc_el_carrier_conc_unit(self):
        """
        calc_el_carrier_conc should return a value with unit 1/cm3.
        """
        self.assertEqual(self.El.calc_el_carrier_conc().unit, Unit("1/cm3"))

    def test_calc_ho_carrier_conc_unit(self):
        """
        calc_ho_carrier_conc should return a value with unit 1/cm3.
        """
        self.assertEqual(self.El.calc_ho_carrier_conc().unit, Unit("1/cm3"))

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
