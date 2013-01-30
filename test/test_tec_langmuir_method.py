#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests methods of the TEC_Langmuir class.
"""

__author__ = "Joshua Ryan Smith (joshua.r.smith@gmail.com)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2013 Joshua Ryan Smith"
__license__ = ""

from tec import TEC_Langmuir
import unittest
import pickle

class MethodsSpecialCase(unittest.TestCase):
  """
  Tests the special cases of the methods.
  """
  pass
  
class MethodsValues(unittest.TestCase):
  """
  Tests the output of the methods match some expected values.
  """
  
  def setUp(self):
    """
    Unpickle the standard data for use in the tests.
    """
    
    self.std = pickle.load(open("test/TEC_Langmuir_temporary_STANDARD.dat","r"))
  
  def test_calc_saturation_pt_output_voltage(self):
    """
    calc_saturation_pt output_voltage matches standard values.
    """
    TECL = TEC_Langmuir(std[0])
    output_params = TECL.calc_saturation_pt()
    output_voltage = output_params["output_voltage"]
    # Set the following to a very low precision.
    self.assertAlmostEqual(self.std[0]["Collector"]["Voltage"],output_voltage)

  def test_calc_saturation_pt_output_current_density(self):
    """
    calc_saturation_pt output_current_density matches standard values.
    """
    TECL = TEC_Langmuir(std[0])
    output_params = TECL.calc_saturation_pt()
    output_current_density = output_params["output_current_density"]
    # Set the following to a very low precision.
    self.assertAlmostEqual(self.std[0]["output_current_density"],output_current_density)

  def test_calc_critical_pt_output_voltage(self):
    """
    calc_critical_pt output_voltage matches standard values.
    """
    TECL = TEC_Langmuir(std[-1])
    output_params = TECL.calc_critical_pt()
    output_voltage = output_params["output_voltage"]
    # Set the following to a very low precision.
    self.assertAlmostEqual(self.std[-1]["Collector"]["Voltage"],output_voltage)

  def test_calc_critical_pt_output_current_density(self):
    """
    calc_critical_pt output_current_density matches standard values.
    """
    TECL = TEC_Langmuir(std[-1])
    output_params = TECL.calc_critical_pt()
    output_current_density = output_params["output_current_density"]
    # Set the following to a very low precision.
    self.assertAlmostEqual(self.std[-1]["output_current_density"],output_current_density)
    
  def test_calc_output_current_density(self):
    """
    calc_output_current_density matches standard values.
    """
    for data in std:
      TECL = TEC_Langmuir(data)
      # Set the following to a very low precision.
      self.assertAlmostEqual(TECL.calc_output_current_density(),\
	data["output_current_density"])