#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Tests API of the Electrode class.
"""

__author__ = "Joshua Ryan Smith (joshua.r.smith@gmail.com)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2012 Joshua Ryan Smith"
__license__ = 

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

    inputParams = {"temperature":1,\
                   "barrierHeight":1,\
                   "voltage":1,\
                   "position":0,\
                   "richardson":10,\
                   "emissivity":0.5}
                   
    self.inputParams = inputParams
    

  # No input argument.
  def test_Electrode_no_input_arg(self):
    """Attempt to instantiate Electrode with no input argument."""
    self.assertRaises(TypeError,Electrode,None)
  
  # Non-dict input argument.
  def test_Electrode_non_dict_input_arg(self):
    """Attempt to instantiate Electrode with a non-dict input argument."""
    self.assertRaises(TypeError,Electrode,"this is a string")

  # Missing required fields in input dict.
  def test_Electrode_input_arg_sans_temp(self):
    pass

  def test_Electrode_input_arg_sans_barrier_ht(self):
    pass

  def test_Electrode_input_arg_sans_voltage(self):
    pass

  def test_Electrode_input_arg_sans_position(self):
    pass

  def test_Electrode_input_arg_sans_richardson(self):
    pass

  def test_Electrode_input_arg_sans_emissivity(self):
    pass

  # Input dict values are non-numeric.
  def test_Electrode_input_temp_non_numeric(self):
    pass

  def test_Electrode_input_barrier_ht_non_numeric(self):
    pass

  def test_Electrode_input_voltage_non_numeric(self):
    pass

  def test_Electrode_input_position_non_numeric(self):
    pass

  def test_Electrode_input_richardson_non_numeric(self):
    pass

  def test_Electrode_input_emissivit_non_numeric(self):
    pass

  # Input dict values are outside their constraints.
  def test_Electrode_input_temp_less_than_zero(self):
    pass
  
  def test_Electrode_input_barrier_ht_less_than_zero(self):
    pass
  
  def test_Electrode_input_richardson_less_than_zero(self):
    pass
  
  def test_Electrode_input_emissivity_less_than_zero(self):
    pass
  
  def test_Electrode_input_emissivity_greater_than_one(self):
    pass
  
  def test_Electrode_input_nea_less_than_zero(self):
    pass
  

if __name__ == '__main__':
  unittest.main()
