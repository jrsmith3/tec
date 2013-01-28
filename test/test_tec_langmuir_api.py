#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Tests API of the TEC_Langmuir class.

These tests can be considered "logical testing" as described in the README. The definition of "logical testing" define the scope and purpose of these tests.

Please note that TEC objects (and their children) have attributes of type "Electrode." These tests do not test functionality of these Electrode attributes -- for example attempting to set illegal values for the temp of the Emitter attribute.
"""

__author__ = "Joshua Ryan Smith (joshua.r.smith@gmail.com)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2013 Joshua Ryan Smith"
__license__ = ""

from tec import TEC_Langmuir
import unittest

    
class CalculatorsReturnType(unittest.TestCase):
  """
  Tests output types of the TEC calculator methods.
  """

  def setUp(self):
    """
    Set up a TEC object for the tests
    """

    em_params = {"temp":1,\
                 "barrier_ht":1,\
                 "voltage":1,\
                 "position":0,\
                 "richardson":10,\
                 "emissivity":0.5}
                   
    co_params = {"temp":1,\
                 "barrier_ht":1,\
                 "voltage":1,\
                 "position":1,\
                 "richardson":10,\
                 "emissivity":0.5}
                 
    input_params = {"Emitter":em_params, "Collector":co_params}
                   
    self.TEC_obj = TEC_Langmuir(input_params)
    
  #def test_get_motive_numeric(self):
    #"""
    #get_motive returns numeric type.
    #"""
    #self.assertTrue(isinstance(self.TEC_obj.get_motive(0.5),float))
  
  #def test_get_motive_numpy_array(self):
    #"""
    #get_motive returns numpy array type.
    #"""
    #pass
  
  def test_get_max_motive(self):
    """
    get_max_motive returns numeric type.
    """
    self.assertTrue(isinstance(self.TEC_obj.get_max_motive(),float))
  
  def test_get_max_motive_with_position(self):
    """
    get_max_motive returns tuple.
    """
    self.assertTrue(isinstance(self.TEC_obj.get_max_motive(with_position=1),tuple))
  
  def test_get_max_motive_with_position_tuple_items(self):
    """
    get_max_motive returns tuple with numeric items.
    """
    tup = self.TEC_obj.get_max_motive(with_position=1)
    self.assertTrue(all( isinstance(indx,float) for indx in tup ))
  
  def test_calc_interelectrode_spacing(self):
    """
    calc_interelectrode_spacing returns numeric.
    """
    self.assertTrue(isinstance(self.TEC_obj.calc_interelectrode_spacing(),float))

  def test_calc_output_voltage(self):
    """
    calc_output_voltage returns numeric.
    """
    self.assertTrue(isinstance(self.TEC_obj.calc_output_voltage(),float))

  def test_calc_contact_potential(self):
    """
    calc_contact_potential returns numeric.
    """
    self.assertTrue(isinstance(self.TEC_obj.calc_contact_potential(),float))

  def test_calc_forward_current_density(self):
    """
    calc_forward_current_density returns numeric.
    """
    self.assertTrue(isinstance(self.TEC_obj.calc_forward_current_density(),float))

  def test_calc_back_current_density(self):
    """
    calc_back_current_density returns numeric.
    """
    self.assertTrue(isinstance(self.TEC_obj.calc_back_current_density(),float))

  def test_calc_output_current_density(self):
    """
    calc_output_current_density returns numeric.
    """
    self.assertTrue(isinstance(self.TEC_obj.calc_output_current_density(),float))

  def test_calc_output_power_density(self):
    """
    calc_output_power_density returns numeric.
    """
    self.assertTrue(isinstance(self.TEC_obj.calc_output_power_density(),float))

  def test_calc_load_resistance(self):
    """
    calc_load_resistance returns numeric.
    """
    self.assertTrue(isinstance(self.TEC_obj.calc_load_resistance(),float))

  def test_calc_carnot_efficiency(self):
    """
    calc_carnot_efficiency returns numeric.
    """
    self.assertTrue(isinstance(self.TEC_obj.calc_carnot_efficiency(),float))

  def test_calc_radiation_efficiency(self):
    """
    calc_radiation_efficiency returns numeric.
    """
    self.assertTrue(isinstance(self.TEC_obj.calc_radiation_efficiency(),float))

  def test_calc_electronic_efficiency(self):
    """
    calc_electronic_efficiency returns numeric.
    """
    self.assertTrue(isinstance(self.TEC_obj.calc_electronic_efficiency(),float))

  def test_calc_total_efficiency(self):
    """
    calc_total_efficiency returns numeric.
    """
    self.assertTrue(isinstance(self.TEC_obj.calc_total_efficiency(),float))

if __name__ == '__main__':
  unittest.main()
