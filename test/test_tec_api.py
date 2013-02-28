# -*- coding: utf-8 -*-

"""
Tests API of the TECBase class.

I will eventually need to fix this note, but here it is. I am intentionally not
testing the cases where the sub-dicts have incorrect data. The Electrode tests
deal with these cases comprehensively and there is no additional logic at the 
TECBase level. In the event that I do need to test these cases, I can always reach
back in the VCS history and grab the previous version of this file.
"""

from tec import TECBase
import unittest

class InstantiationInputNonDict(unittest.TestCase):
  """
  Tests instantiation when non-dict data is used.
  """

  def test_TECBase_no_input_arg(self):
    """Attempt to instantiate TECBase with no input argument."""
    self.assertRaises(TypeError,TECBase,None)
  
  def test_TECBase_non_dict_input_arg(self):
    """Attempt to instantiate Electrode with a non-dict input argument."""
    self.assertRaises(TypeError,TECBase,"this string is not a dict.")


class InstantiationInputIncomplete(unittest.TestCase):
  """
  Tests instantiating when input dict is missing required data.
  """
  
  def setUp(self):
    """
    Set up a dictionary that can properly instantiate a TECBase object.
    """

    em_params = {"temp":1,\
                 "barrier":1,\
                 "voltage":1,\
                 "position":0,\
                 "richardson":10,\
                 "emissivity":0.5}
                   
    co_params = {"temp":1,\
                 "barrier":1,\
                 "voltage":1,\
                 "position":0,\
                 "richardson":10,\
                 "emissivity":0.5}
                 
    input_params = {"Emitter":em_params, "Collector":co_params}
                   
    self.input_params = input_params
    
  def test_TECBase_input_arg_sans_Emitter(self):
    """Instantiating argument missing Emitter."""
    del(self.input_params["Emitter"])
    self.assertRaises(KeyError,TECBase,self.input_params)
  
  def test_TECBase_input_arg_sans_Collector(self):
    """Instantiating argument missing Emitter."""
    del(self.input_params["Collector"])
    self.assertRaises(KeyError,TECBase,self.input_params)  
  
class InstantiationInputFieldsWrongType(unittest.TestCase):
  """
  Tests instantiating when input dict has non-numeric data items.
  """

  def setUp(self):
    """
    Set up a dictionary that can properly instantiate a TECBase object.
    """

    em_params = {"temp":1,\
                 "barrier":1,\
                 "voltage":1,\
                 "position":0,\
                 "richardson":10,\
                 "emissivity":0.5}
                   
    co_params = {"temp":1,\
                 "barrier":1,\
                 "voltage":1,\
                 "position":0,\
                 "richardson":10,\
                 "emissivity":0.5}
                 
    input_params = {"Emitter":em_params, "Collector":co_params}
                   
    self.input_params = input_params

  def test_TECBase_input_Emitter_non_numeric(self):
    """Instantiating argument Emitter is non-numeric."""
    self.input_params["Emitter"] = "this string is non-numeric."
    self.assertRaises(TypeError,TECBase,self.input_params)
  
  def test_TECBase_input_Collector_non_numeric(self):
    """Instantiating argument Collector is non-numeric."""
    self.input_params["Collector"] = "this string is non-numeric."
    self.assertRaises(TypeError,TECBase,self.input_params)
  

class SetInputWrongType(unittest.TestCase):
  """
  Tests setting attributes when input data is non-numeric.
  """

  def setUp(self):
    """
    Set up a TECBase object for the tests
    """

    em_params = {"temp":1,\
                 "barrier":1,\
                 "voltage":1,\
                 "position":0,\
                 "richardson":10,\
                 "emissivity":0.5}
                   
    co_params = {"temp":1,\
                 "barrier":1,\
                 "voltage":1,\
                 "position":0,\
                 "richardson":10,\
                 "emissivity":0.5}
                 
    input_params = {"Emitter":em_params, "Collector":co_params}
                   
    self.TECBase_obj = TECBase(input_params)
    
  def test_TECBase_set_Emitter_non_numeric(self):
    """Set argument Emitter non-numeric."""
    non_num = "this string is non-numeric."
    self.assertRaises(TypeError,self.TECBase_obj["Emitter"],non_num)

  def test_TECBase_set_Collector_non_numeric(self):
    """Set argument Collector non-numeric."""
    non_num = "this string is non-numeric."
    self.assertRaises(TypeError,self.TECBase_obj["Collector"],non_num)
    
class CalculatorsReturnType(unittest.TestCase):
  """
  Tests output types of the TECBase calculator methods.
  """

  def setUp(self):
    """
    Set up a TECBase object for the tests
    """

    em_params = {"temp":1,\
                 "barrier":1,\
                 "voltage":1,\
                 "position":0,\
                 "richardson":10,\
                 "emissivity":0.5}
                   
    co_params = {"temp":1,\
                 "barrier":1,\
                 "voltage":1,\
                 "position":1,\
                 "richardson":10,\
                 "emissivity":0.5}
                 
    input_params = {"Emitter":em_params, "Collector":co_params}
                   
    self.TECBase_obj = TECBase(input_params)
    
  #def test_get_motive_numeric(self):
    #"""
    #get_motive returns numeric type.
    #"""
    #self.assertTrue(isinstance(self.TECBase_obj.get_motive(0.5),float))
  
  #def test_get_motive_numpy_array(self):
    #"""
    #get_motive returns numpy array type.
    #"""
    #pass
  
  def test_get_max_motive_ht(self):
    """
    get_max_motive_ht returns numeric type.
    """
    self.assertTrue(isinstance(self.TECBase_obj.get_max_motive_ht(),float))
  
  def test_get_max_motive_ht_with_position(self):
    """
    get_max_motive_ht returns tuple.
    """
    self.assertTrue(isinstance(self.TECBase_obj.get_max_motive_ht(with_position=1),tuple))
  
  def test_get_max_motive_ht_with_position_tuple_items(self):
    """
    get_max_motive_ht returns tuple with numeric items.
    """
    tup = self.TECBase_obj.get_max_motive_ht(with_position=1)
    self.assertTrue(all( isinstance(indx,float) for indx in tup ))
  
  def test_calc_interelectrode_spacing(self):
    """
    calc_interelectrode_spacing returns numeric.
    """
    self.assertTrue(isinstance(self.TECBase_obj.calc_interelectrode_spacing(),float))

  def test_calc_output_voltage(self):
    """
    calc_output_voltage returns numeric.
    """
    self.assertTrue(isinstance(self.TECBase_obj.calc_output_voltage(),float))

  def test_calc_contact_potential(self):
    """
    calc_contact_potential returns numeric.
    """
    self.assertTrue(isinstance(self.TECBase_obj.calc_contact_potential(),float))

  def test_calc_forward_current_density(self):
    """
    calc_forward_current_density returns numeric.
    """
    self.assertTrue(isinstance(self.TECBase_obj.calc_forward_current_density(),float))

  def test_calc_back_current_density(self):
    """
    calc_back_current_density returns numeric.
    """
    self.assertTrue(isinstance(self.TECBase_obj.calc_back_current_density(),float))

  def test_calc_output_current_density(self):
    """
    calc_output_current_density returns numeric.
    """
    self.assertTrue(isinstance(self.TECBase_obj.calc_output_current_density(),float))

  def test_calc_output_power_density(self):
    """
    calc_output_power_density returns numeric.
    """
    self.assertTrue(isinstance(self.TECBase_obj.calc_output_power_density(),float))

  def test_calc_load_resistance(self):
    """
    calc_load_resistance returns numeric.
    """
    self.assertTrue(isinstance(self.TECBase_obj.calc_load_resistance(),float))

  def test_calc_carnot_efficiency(self):
    """
    calc_carnot_efficiency returns numeric.
    """
    self.assertTrue(isinstance(self.TECBase_obj.calc_carnot_efficiency(),float))

  def test_calc_radiation_efficiency(self):
    """
    calc_radiation_efficiency returns numeric.
    """
    self.assertTrue(isinstance(self.TECBase_obj.calc_radiation_efficiency(),float))

  def test_calc_electronic_efficiency(self):
    """
    calc_electronic_efficiency returns numeric.
    """
    self.assertTrue(isinstance(self.TECBase_obj.calc_electronic_efficiency(),float))

  def test_calc_total_efficiency(self):
    """
    calc_total_efficiency returns numeric.
    """
    self.assertTrue(isinstance(self.TECBase_obj.calc_total_efficiency(),float))
