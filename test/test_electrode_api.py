#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Tests API of the Electrode class.
"""

__author__ = "Joshua Ryan Smith (joshua.r.smith@gmail.com)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2012 Joshua Ryan Smith"
__license__ = ""

from tec import Electrode
import unittest

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


class InstantiationInputIncomplete(unittest.TestCase):
  """
  Tests instantiating when input dict is missing required data.
  """
  
  def setUp(self):
    """
    Set up a dictionary that can properly instantiate an Electrode object.
    """

    input_params = {"temp":1,\
                   "barrier_ht":1,\
                   "voltage":1,\
                   "position":0,\
                   "richardson":10,\
                   "emissivity":0.5}
                   
    self.input_params = input_params

  def test_Electrode_input_arg_sans_temp(self):
    """Instantiating argument missing temp."""
    del(self.input_params["temp"])
    self.assertRaises(KeyError,Electrode,self.input_params)

  def test_Electrode_input_arg_sans_barrier_ht(self):
    """Instantiating argument missing barrier_ht."""
    del(self.input_params["barrier_ht"])
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
    
    
class InstantiationInputFieldsWrongType(unittest.TestCase):
  """
  Tests instantiating when input dict has non-numeric data items.
  """

  def setUp(self):
    """
    Set up a dictionary that can properly instantiate an Electrode object.
    """

    input_params = {"temp":1,\
                   "barrier_ht":1,\
                   "voltage":1,\
                   "position":0,\
                   "richardson":10,\
                   "emissivity":0.5}
                   
    self.input_params = input_params

  def test_Electrode_input_temp_non_numeric(self):
    """Instantiating argument temp is non-numeric."""
    self.input_params["temp"] = "this string is non-numeric."
    self.assertRaises(TypeError,Electrode,self.input_params)

  def test_Electrode_input_barrier_ht_non_numeric(self):
    """Instantiating argument barrier_ht is non-numeric."""
    self.input_params["barrier_ht"] = "this string is non-numeric."
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


class InstantiationInputOutsideConstraints(unittest.TestCase):
  """
  Tests instantiating when input dict values are outside their constraints.
  
  See the Electrode class docstring for information about the constraints on 
  the input data.
  """

  def setUp(self):
    """
    Set up a dictionary that can properly instantiate an Electrode object.
    """

    input_params = {"temp":1,\
                   "barrier_ht":1,\
                   "voltage":1,\
                   "position":0,\
                   "richardson":10,\
                   "emissivity":0.5}
                   
    self.input_params = input_params

  def test_Electrode_input_temp_less_than_zero(self):
    """Instantiating argument temp < 0."""
    self.input_params["temp"] = -1.1
    self.assertRaises(ValueError,Electrode,self.input_params)
  
  def test_Electrode_input_barrier_ht_less_than_zero(self):
    """Instantiating argument barrier_ht < 0."""
    self.input_params["barrier_ht"] = -1.1
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
    
class SetInputWrongType(unittest.TestCase):
  """
  Tests setting attributes when input data is non-numeric.
  """

  def setUp(self):
    """
    Set up an Electrode object for the tests.
    """

    input_params = {"temp":1,\
                   "barrier_ht":1,\
                   "voltage":1,\
                   "position":0,\
                   "richardson":10,\
                   "emissivity":0.5, \
                   "nea":1.0}
                   
    self.El = Electrode(input_params)
    
  def test_Electrode_set_temp_non_numeric(self):
    """Set argument temp non-numeric."""
    non_num = "this string is non-numeric."
    self.assertRaises(TypeError,Electrode["temp"],non_num)

  def test_Electrode_set_barrier_ht_non_numeric(self):
    """Set argument barrier_ht non-numeric."""
    non_num = "this string is non-numeric."
    self.assertRaises(TypeError,Electrode["barrier_ht"],non_num)

  def test_Electrode_set_voltage_non_numeric(self):
    """Set argument voltage non-numeric."""
    non_num = "this string is non-numeric."
    self.assertRaises(TypeError,Electrode["voltage"],non_num)

  def test_Electrode_set_position_non_numeric(self):
    """Set argument position non-numeric."""
    non_num = "this string is non-numeric."
    self.assertRaises(TypeError,Electrode["position"],non_num)

  def test_Electrode_set_richardson_non_numeric(self):
    """Set argument richardson non-numeric."""
    non_num = "this string is non-numeric."
    self.assertRaises(TypeError,Electrode["richardson"],non_num)

  def test_Electrode_set_emissivity_non_numeric(self):
    """Set argument emissivity non-numeric."""
    non_num = "this string is non-numeric."
    self.assertRaises(TypeError,Electrode["emissivity"],non_num)

  def test_Electrode_set_nea_non_numeric(self):
    """Set argument nea non-numeric."""
    non_num = "this string is non-numeric."
    self.assertRaises(TypeError,Electrode["nea"],non_num)


class SetInputOutsideConstraints(unittest.TestCase):
  """
  Tests setting attributes when input values are outside their constraints.
  
  See the Electrode class docstring for information about the constraints on 
  the data.
  """
  
  def setUp(self):
    """
    Set up an Electrode object for the tests.
    """

    input_params = {"temp":1,\
                   "barrier_ht":1,\
                   "voltage":1,\
                   "position":0,\
                   "richardson":10,\
                   "emissivity":0.5, \
                   "nea":1.0}
                   
    self.El = Electrode(input_params)
    
  def test_Electrode_set_temp_less_than_zero(self):
    """Instantiating argument temp < 0."""
    self.assertRaises(ValueError,Electrode["temp"],-1.1)
  
  def test_Electrode_set_barrier_ht_less_than_zero(self):
    """Instantiating argument barrier_ht < 0."""
    self.assertRaises(ValueError,Electrode["barrier_ht"],-1.1)
  
  def test_Electrode_set_richardson_less_than_zero(self):
    """Instantiating argument richardson < 0."""
    self.assertRaises(ValueError,Electrode["richardson"],-1.1)
  
  def test_Electrode_set_emissivity_less_than_zero(self):
    """Instantiating argument emissivity < 0."""
    self.assertRaises(ValueError,Electrode["emissivity"],-1.1)
  
  def test_Electrode_set_emissivity_greater_than_one(self):
    """Instantiating argument emissivity > 1."""
    self.assertRaises(ValueError,Electrode["emissivity"],1.1)
  
  def test_Electrode_set_nea_less_than_zero(self):
    """Instantiating argument nea < 0."""
    self.assertRaises(ValueError,Electrode["nea"],-1.1)
    

class CalculatorsReturnType(unittest.TestCase):
  """
  Tests output types of the Electrode calculator methods.
  """

  def setUp(self):
    """
    Set up an Electrode object for the tests.
    """

    input_params = {"temp":1,\
                   "barrier_ht":1,\
                   "voltage":1,\
                   "position":0,\
                   "richardson":10,\
                   "emissivity":0.5, \
                   "nea":1.0}
                   
    self.El = Electrode(input_params)
    
  def test_Electrode_calc_saturation_current_type(self):
    """calc_saturation_current should return a number."""
    self.assertIsInstance(self.El.calc_saturation_current(),(int,long,float))

  def test_Electrode_calc_vacuum_energy_type(self):
    """calc_vacuum_energy should return a number."""
    self.assertIsInstance(self.El.calc_vacuum_energy(),(int,long,float))


if __name__ == '__main__':
  unittest.main()
