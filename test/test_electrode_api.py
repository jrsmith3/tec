# -*- coding: utf-8 -*-

from tec import Electrode
from input_params import electrode_input_params as el_input
import unittest
import copy

# ============
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
    self.input_params = copy.copy(el_input)

class ElectrodeAPITestBaseWithElectrode(unittest.TestCase):
  """
  Base class for API tests.

  This class defines a common setUp method that all the tests in this suite use.
  """
  def setUp(self):
    """
    Set up a dictionary that can properly instantiate an Electrode object.
    """
    self.El = Electrode(copy.copy(el_input))


# ============
# Test classes
# ============
class InstantiationInputNonDict(unittest.TestCase):
  """
  Tests instantiation when non-dict data is used.
  """
  def test_Electrode_no_input_arg(self):
    """Attempt to instantiate Electrode with no input argument."""
    self.assertRaises(TypeError,Electrode,None)
  
  def test_Electrode_non_dict_input_arg(self):
    """Attempt to instantiate Electrode with a non-dict input argument."""
    self.assertRaises(TypeError,Electrode,"this string is not a dict.")


class InstantiationInputIncomplete(ElectrodeAPITestBaseJustInputParams):
  """
  Tests instantiating when input dict is missing required data.
  """
  def test_Electrode_input_arg_sans_temp(self):
    """Instantiating argument missing temp."""
    del(self.input_params["temp"])
    self.assertRaises(KeyError,Electrode,self.input_params)

  def test_Electrode_input_arg_sans_barrier(self):
    """Instantiating argument missing barrier."""
    del(self.input_params["barrier"])
    self.assertRaises(KeyError,Electrode,self.input_params)

  def test_Electrode_input_arg_sans_voltage(self):
    """Instantiating argument missing voltage."""
    del(self.input_params["voltage"])
    self.assertRaises(KeyError,Electrode,self.input_params)

  def test_Electrode_input_arg_sans_position(self):
    """Instantiating argument missing position."""
    del(self.input_params["position"])
    self.assertRaises(KeyError,Electrode,self.input_params)

  def test_Electrode_input_arg_sans_richardson(self):
    """Instantiating argument missing richardson."""
    del(self.input_params["richardson"])
    self.assertRaises(KeyError,Electrode,self.input_params)

  def test_Electrode_input_arg_sans_emissivity(self):
    """Instantiating argument missing emissivity."""
    del(self.input_params["emissivity"])
    self.assertRaises(KeyError,Electrode,self.input_params)
    
    
class InstantiationInputFieldsWrongType(ElectrodeAPITestBaseJustInputParams):
  """
  Tests instantiating when input dict has non-numeric data items.
  """
  def test_Electrode_input_temp_non_numeric(self):
    """Instantiating argument temp is non-numeric."""
    self.input_params["temp"] = "this string is non-numeric."
    self.assertRaises(TypeError,Electrode,self.input_params)

  def test_Electrode_input_barrier_non_numeric(self):
    """Instantiating argument barrier is non-numeric."""
    self.input_params["barrier"] = "this string is non-numeric."
    self.assertRaises(TypeError,Electrode,self.input_params)

  def test_Electrode_input_voltage_non_numeric(self):
    """Instantiating argument voltage is non-numeric."""
    self.input_params["voltage"] = "this string is non-numeric."
    self.assertRaises(TypeError,Electrode,self.input_params)

  def test_Electrode_input_position_non_numeric(self):
    """Instantiating argument position is non-numeric."""
    self.input_params["position"] = "this string is non-numeric."
    self.assertRaises(TypeError,Electrode,self.input_params)

  def test_Electrode_input_richardson_non_numeric(self):
    """Instantiating argument richardson is non-numeric."""
    self.input_params["richardson"] = "this string is non-numeric."
    self.assertRaises(TypeError,Electrode,self.input_params)

  def test_Electrode_input_emissivity_non_numeric(self):
    """Instantiating argument emissivity is non-numeric."""
    self.input_params["emissivity"] = "this string is non-numeric."
    self.assertRaises(TypeError,Electrode,self.input_params)

  def test_Electrode_input_nea_non_numeric(self):
    """Instantiating argument nea is non-numeric."""
    self.input_params["nea"] = "this string is non-numeric."
    self.assertRaises(TypeError,Electrode,self.input_params)


class InstantiationInputOutsideConstraints(ElectrodeAPITestBaseJustInputParams):
  """
  Tests instantiating when input dict values are outside their constraints.
  
  See the Electrode class docstring for information about the constraints on 
  the input data.
  """
  def test_Electrode_input_temp_less_than_zero(self):
    """Instantiating argument temp < 0."""
    self.input_params["temp"] = -1.1
    self.assertRaises(ValueError,Electrode,self.input_params)
  
  def test_Electrode_input_barrier_less_than_zero(self):
    """Instantiating argument barrier < 0."""
    self.input_params["barrier"] = -1.1
    self.assertRaises(ValueError,Electrode,self.input_params)
  
  def test_Electrode_input_richardson_less_than_zero(self):
    """Instantiating argument richardson < 0."""
    self.input_params["richardson"] = -1.1
    self.assertRaises(ValueError,Electrode,self.input_params)
  
  def test_Electrode_input_emissivity_less_than_zero(self):
    """Instantiating argument emissivity < 0."""
    self.input_params["emissivity"] = -1.1
    self.assertRaises(ValueError,Electrode,self.input_params)
  
  def test_Electrode_input_emissivity_greater_than_one(self):
    """Instantiating argument emissivity > 1."""
    self.input_params["emissivity"] = 1.1
    self.assertRaises(ValueError,Electrode,self.input_params)
  
  def test_Electrode_input_nea_less_than_zero(self):
    """Instantiating argument nea < 0."""
    self.input_params["nea"] = -1.0
    self.assertRaises(ValueError,Electrode,self.input_params)


class SetInputWrongType(ElectrodeAPITestBaseWithElectrode):
  """
  Tests setting attributes when input data is non-numeric.
  """
  def test_Electrode_set_temp_non_numeric(self):
    """Set argument temp non-numeric."""
    non_num = "this string is non-numeric."
    self.assertRaises(TypeError,self.El["temp"],non_num)

  def test_Electrode_set_barrier_non_numeric(self):
    """Set argument barrier non-numeric."""
    non_num = "this string is non-numeric."
    self.assertRaises(TypeError,self.El["barrier"],non_num)

  def test_Electrode_set_voltage_non_numeric(self):
    """Set argument voltage non-numeric."""
    non_num = "this string is non-numeric."
    self.assertRaises(TypeError,self.El["voltage"],non_num)

  def test_Electrode_set_position_non_numeric(self):
    """Set argument position non-numeric."""
    non_num = "this string is non-numeric."
    self.assertRaises(TypeError,self.El["position"],non_num)

  def test_Electrode_set_richardson_non_numeric(self):
    """Set argument richardson non-numeric."""
    non_num = "this string is non-numeric."
    self.assertRaises(TypeError,self.El["richardson"],non_num)

  def test_Electrode_set_emissivity_non_numeric(self):
    """Set argument emissivity non-numeric."""
    non_num = "this string is non-numeric."
    self.assertRaises(TypeError,self.El["emissivity"],non_num)

  def test_Electrode_set_nea_non_numeric(self):
    """Set argument nea non-numeric."""
    non_num = "this string is non-numeric."
    self.assertRaises(TypeError,self.El["nea"],non_num)


class SetInputOutsideConstraints(ElectrodeAPITestBaseWithElectrode):
  """
  Tests setting attributes when input values are outside their constraints.
  
  See the Electrode class docstring for information about the constraints on 
  the data.
  """
  def test_Electrode_set_temp_less_than_zero(self):
    """Set argument temp < 0."""
    self.assertRaises(ValueError,self.El.__setitem__, "temp", -1.1)
  
  def test_Electrode_set_barrier_less_than_zero(self):
    """Set argument barrier < 0."""
    self.assertRaises(ValueError,self.El.__setitem__,"barrier",-1.1)
  
  def test_Electrode_set_richardson_less_than_zero(self):
    """Set argument richardson < 0."""
    self.assertRaises(ValueError,self.El.__setitem__,"richardson",-1.1)
  
  def test_Electrode_set_emissivity_less_than_zero(self):
    """Set argument emissivity < 0."""
    self.assertRaises(ValueError,self.El.__setitem__,"emissivity",-1.1)
  
  def test_Electrode_set_emissivity_greater_than_one(self):
    """Set argument emissivity > 1."""
    self.assertRaises(ValueError,self.El.__setitem__,"emissivity",1.1)
  
  def test_Electrode_set_nea_less_than_zero(self):
    """Set argument nea < 0."""
    self.assertRaises(ValueError,self.El.__setitem__,"nea",-1.1)
    

# None of the following works on Python 2.6.6 which is what is on my work computer.
class CalculatorsReturnType(ElectrodeAPITestBaseWithElectrode):
  """
  Tests output types of the Electrode calculator methods.
  """
  def test_Electrode_calc_saturation_current_type(self):
    """calc_saturation_current should return a number."""
    self.assertIsInstance(self.El.calc_saturation_current(),(int,long,float))

  def test_Electrode_calc_vacuum_energy_type(self):
    """calc_vacuum_energy should return a number."""
    self.assertIsInstance(self.El.calc_vacuum_energy(),(int,long,float))

  def test_Electrode_calc_barrier_ht_type(self):
    """calc_barrier_ht should return a number."""
    self.assertIsInstance(self.El.calc_barrier_ht(),(int,long,float))

  def test_Electrode_calc_motive_bc(self):
    """calc_vacuum_energy should return a number."""
    self.assertIsInstance(self.El.calc_motive_bc(),(int,long,float))

class ParamChanged(ElectrodeAPITestBaseWithElectrode):
  """
  Functionality of method param_changed_and_reset
  """
  def test_usually_false(self):
    """
    param_changed_and_reset should be 0 by default
    """
    self.assertFalse(self.El.param_changed_and_reset())

  def test_true_immediately_after_temp_change(self):
    """
    param_changed_and_reset should switch to 1 if temp changes
    """
    self.El["temp"] = 0.7
    self.assertTrue(self.El.param_changed_and_reset())

  def test_true_immediately_after_barrier_change(self):
    """
    param_changed_and_reset should switch to 1 if barrier changes
    """
    self.El["barrier"] = 0.7
    self.assertTrue(self.El.param_changed_and_reset())

  def test_true_immediately_after_voltage_change(self):
    """
    param_changed_and_reset should switch to 1 if voltage changes
    """
    self.El["voltage"] = 0.7
    self.assertTrue(self.El.param_changed_and_reset())

  def test_true_immediately_after_position_change(self):
    """
    param_changed_and_reset should switch to 1 if position changes
    """
    self.El["position"] = 0.7
    self.assertTrue(self.El.param_changed_and_reset())

  def test_true_immediately_after_richardson_change(self):
    """
    param_changed_and_reset should switch to 1 if richardson changes
    """
    self.El["richardson"] = 0.7
    self.assertTrue(self.El.param_changed_and_reset())

  def test_true_immediately_after_emissivity_change(self):
    """
    param_changed_and_reset should be 0 if emissivity changes
    """
    self.El["emissivity"] = 0.7
    self.assertFalse(self.El.param_changed_and_reset())

  def test_true_immediately_after_nea_change(self):
    """
    param_changed_and_reset should switch to 1 if nea changes
    """
    self.El["nea"] = 0.7
    self.assertTrue(self.El.param_changed_and_reset())

  def test_reset_to_false_after_temp_change(self):
    """
    param_changed_and_reset should switch to 0 after checking temp
    """
    self.El["temp"] = 0.7
    self.El.param_changed_and_reset()
    self.assertFalse(self.El.param_changed_and_reset())

  def test_reset_to_false_after_barrier_change(self):
    """
    param_changed_and_reset should switch to 0 after checking barrier
    """
    self.El["barrier"] = 0.7
    self.El.param_changed_and_reset()
    self.assertFalse(self.El.param_changed_and_reset())

  def test_reset_to_false_after_voltage_change(self):
    """
    param_changed_and_reset should switch to 0 after checking voltage
    """
    self.El["voltage"] = 0.7
    self.El.param_changed_and_reset()
    self.assertFalse(self.El.param_changed_and_reset())

  def test_reset_to_false_after_position_change(self):
    """
    param_changed_and_reset should switch to 0 after checking position
    """
    self.El["position"] = 0.7
    self.El.param_changed_and_reset()
    self.assertFalse(self.El.param_changed_and_reset())

  def test_reset_to_false_after_richardson_change(self):
    """
    param_changed_and_reset should switch to 0 after checking richardson
    """
    self.El["richardson"] = 0.7
    self.El.param_changed_and_reset()
    self.assertFalse(self.El.param_changed_and_reset())

  def test_reset_to_false_after_nea_change(self):
    """
    param_changed_and_reset should switch to 0 after checking nea
    """
    self.El["nea"] = 0.7
    self.El.param_changed_and_reset()
    self.assertFalse(self.El.param_changed_and_reset())
