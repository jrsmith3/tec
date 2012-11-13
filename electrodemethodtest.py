#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Tests methods of the Electrode class.
"""

__author__ = "Joshua Ryan Smith (joshua.r.smith@gmail.com)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2012 Joshua Ryan Smith"
__license__ = 

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

    inputParams = {"temperature":1,\
                   "barrierHeight":1,\
                   "voltage":1,\
                   "position":0,\
                   "richardson":10,\
                   "emissivity":0.5}
                   
    self.inputParams = inputParams
    
  def test_output_current_zero_temp(self):
    pass
  
  def test_output_current_zero_richardson(self):
    pass
  
class MethodsValues(unittest.TestCase):
  """
  Tests the output of the methods match some expected values.
  """
  
  def test_vacuum_energy_without_nea(self):
    """
    I still need to be able to accurately calculate the vacuum energy when there is no nea attribute.
    """
    pass
  
  def test_vacuum_energy_with_nea(self):
    pass
  
  def test_saturation_current_values(self):
    pass

if __name__ == '__main__':
  unittest.main()
