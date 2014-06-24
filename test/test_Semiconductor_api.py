# -*- coding: utf-8 -*-
import numpy as np
from electrode import Semiconductor
from astropy.units import Quantity
from astropy.units import Unit
import unittest
import copy

# Values for Si taken from Streetman & Banerjee 9780130255389.
input_params = {"temp": 300.,
                "el_effective_mass": 9.84e-31,
                "ho_effective_mass": 7.38e-31,
                "accept_conc": 1e18,
                "accept_ionization_energy": 45.,
                "bandgap": 1.11,}

# Base classes
# ============
class ElectrodeAPITestBaseJustInputParams(unittest.TestCase):
    """
    Base class for API tests.

    This class defines a common setUp method that all the tests in this suite use.
    """

    def setUp(self):
        """
        Set up a dictionary that can properly instantiate an Electrode object.
        """
        self.input_params = copy.copy(input_params)


class ElectrodeAPITestBaseWithElectrode(unittest.TestCase):
    """
    Base class for API tests.

    This class defines a common setUp method that all the tests in this suite use.
    """

    def setUp(self):
        """
        Set up a dictionary that can properly instantiate an Electrode object.
        """
        self.El = Semiconductor(copy.copy(input_params))


# Test classes
# ============
class InstantiationInputIncomplete(ElectrodeAPITestBaseJustInputParams):
    """
    Tests instantiating when input dict is missing required data.
    """
    pass


class InstantiationInputSuperfluousKeys(ElectrodeAPITestBaseJustInputParams):
    """
    Semiconductor can be instantiated with dict with superfluous keys.
    """

    def test_Semiconductor_input_superfluous_keys(self):
        """Instantiating argument with additional key."""
        self.input_params["superfluous"] = "value not even numeric!"
        try:
            El = Semiconductor(self.input_params)
        except:
            self.fail("Superfluous key in input param dict caused failure of instantiation.")


class InstantiationInputFieldsWrongType(ElectrodeAPITestBaseJustInputParams):
    """
    Tests instantiating when input dict has non-numeric data items.
    """
    pass


class InstantiationInputOutsideConstraints(ElectrodeAPITestBaseJustInputParams):
    """
    Tests instantiating when input dict values are outside their constraints.

    See the Electrode class docstring for information about the constraints on
    the input data.
    """
    pass


class SetDataWrongType(ElectrodeAPITestBaseWithElectrode):
    """
    Tests setting attributes when input data is non-numeric.
    """
    pass


class SetDataOutsideConstraints(ElectrodeAPITestBaseWithElectrode):
    """
    Tests setting attributes when input values are outside their constraints.

    See the Electrode class docstring for information about the constraints on
    the data.
    """
    pass


class CalculatorsReturnTypeAndUnits(ElectrodeAPITestBaseWithElectrode):
    """
    Tests output types and units (where applicable) of the Electrode calculator methods.
    """

    def test_calc_cond_band_effective_dos_type(self):
        """
        calc_cond_band_effective_dos should return an astropy.units.Quantity.
        """
        self.assertIsInstance(self.El.calc_cond_band_effective_dos(), Quantity)

    def test_calc_cond_band_effective_dos_unit(self):
        """
        calc_cond_band_effective_dos should return a value with unit 1/cm3.
        """
        self.assertEqual(self.El.calc_cond_band_effective_dos().unit, Unit("1/cm3"))

    def test_calc_val_band_effective_dos_type(self):
        """
        calc_val_band_effective_dos should return an astropy.units.Quantity.
        """
        self.assertIsInstance(self.El.calc_val_band_effective_dos(), Quantity)

    def test_calc_val_band_effective_dos_unit(self):
        """
        calc_val_band_effective_dos should return a value with unit 1/cm3.
        """
        self.assertEqual(self.El.calc_val_band_effective_dos().unit, Unit("1/cm3"))

    def test_calc_el_carrier_conc_type(self):
        """
        calc_el_carrier_conc should return an astropy.units.Quantity.
        """
        self.assertIsInstance(self.El.calc_el_carrier_conc(), Quantity)

    def test_calc_el_carrier_conc_unit(self):
        """
        calc_el_carrier_conc should return a value with unit 1/cm3.
        """
        self.assertEqual(self.El.calc_el_carrier_conc().unit, Unit("1/cm3"))

    def test_calc_ho_carrier_conc_type(self):
        """
        calc_ho_carrier_conc should return an astropy.units.Quantity.
        """
        self.assertIsInstance(self.El.calc_ho_carrier_conc(), Quantity)

    def test_calc_ho_carrier_conc_unit(self):
        """
        calc_ho_carrier_conc should return a value with unit 1/cm3.
        """
        self.assertEqual(self.El.calc_ho_carrier_conc().unit, Unit("1/cm3"))

    def test_calc_fermi_energy_type(self):
        """
        calc_fermi_energy should return an astropy.units.Quantity.
        """
        self.assertIsInstance(self.El.calc_fermi_energy(), Quantity)

    def test_calc_fermi_energy_unit(self):
        """
        calc_fermi_energy should return a value with unit eV.
        """
        self.assertEqual(self.El.calc_fermi_energy().unit, Unit("eV"))

if __name__ == "__main__":
    sc = Semiconductor(input_params)
    print "Conduction band dos", str(sc.calc_cond_band_effective_dos())
    print "Valence band dos", str(sc.calc_val_band_effective_dos())

    print "Fermi energy", str(sc.calc_fermi_energy())
    print "Electron concentration", str(sc.calc_el_carrier_conc())
    print "Hole concentration", str(sc.calc_ho_carrier_conc())
