#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Tests methods of the Electrode class.
"""

__author__ = "Joshua Ryan Smith (joshua.r.smith@gmail.com)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2012 Joshua Ryan Smith"
__license__ = ""

from tec import Electrode
import unittest

class MethodsSpecialCase(unittest.TestCase):
  """
  Tests the special cases of the methods.
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
    
  def test_output_current_zero_temp(self):
    """Set temp=0 and verify calc_saturation_current() returns value of 0."""
    self.input_params["temp"] = 0
    el = Electrode(self.input_params)
    self.assertEqual(el.calc_saturation_current(),0)
  
  def test_output_current_zero_richardson(self):
    """Set richardson=0 and verify calc_saturation_current() returns value of 0."""
    self.input_params["richardson"] = 0
    el = Electrode(self.input_params)
    self.assertEqual(el.calc_saturation_current(),0)
  
class MethodsValues(unittest.TestCase):
  """
  Tests the output of the methods match some expected values.
  """
  
  def test_vacuum_energy_without_nea(self):
    """
    I still need to be able to accurately calculate the vacuum energy when there is no nea attribute.
    """
    print "test not implemented."
  
  def test_vacuum_energy_with_nea(self):
    print "test not implemented."
  
  def test_saturation_current_values(self):
    print "test not implemented."

if __name__ == '__main__':
  unittest.main()
