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

class InstantiationBadInput(unittest.TestCase):
  """
  Tests the instantiation with bad input.
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
    

  # No input argument.
  def test_Electrode_no_input_arg(self):
    """Attempt to instantiate Electrode with no input argument."""
    self.assertRaises(TypeError,Electrode,None)
  
  # Non-dict input argument.
  def test_Electrode_non_dict_input_arg(self):
    """Attempt to instantiate Electrode with a non-dict input argument."""
    self.assertRaises(TypeError,Electrode,"this string is not a dict.")

  # Missing required fields in input dict.
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

  # Input dict values are non-numeric.
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

  # Input dict values are outside their constraints.
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
    pass
  

if __name__ == '__main__':
  unittest.main()
