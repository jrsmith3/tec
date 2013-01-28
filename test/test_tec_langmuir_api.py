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
from scipy import interpolate
import unittest

class Instantiation(unittest.TestCase):
  """
  Tests to see if the object can even be created.
  """
  
  def setUp(self):
    """
    Set up a dictionary that can properly instantiate a TEC_Langmuir object.
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
                 "position":0,\
                 "richardson":10,\
                 "emissivity":0.5}
                 
    input_params = {"Emitter":em_params, "Collector":co_params}
                   
    self.input_params = input_params
    
  def test_TEC_Langmuir_instantiation_type(self):
    """
    Tests instantation and proper return type of TEC_Langmuir object.
    """
    TECL = TEC_Langmuir(self.input_params)
    self.assertTrue(isinstance(TECL,TEC_Langmuir))
    
class motive_dataInterface(unittest.TestCase):
  """
  TEC_Langmuir motive_data interface implements description in class docstring.
  """
  def setUp(self):
    """
    Set up a generic TEC_Langmuir object.
    """
    
    # TEC_Langmuir test object.
    em_params = {"temp":1,\
                 "barrier_ht":1,\
                 "voltage":1,\
                 "position":0,\
                 "richardson":10,\
                 "emissivity":0.5}
                   
    co_params = {"temp":1,\
                 "barrier_ht":1,\
                 "voltage":1,\
                 "position":0,\
                 "richardson":10,\
                 "emissivity":0.5}
                 
    input_params = {"Emitter":em_params, "Collector":co_params}
    self.TECL = TEC_Langmuir(input_params)
    
  def test_motive_data_exists(self):
    """
    motive_data should exist.
    """
    self.assertTrue("motive_data" in self.TECL)
  
  def test_motive_data_is_dict(self):
    """
    motive_data is a dictionary.
    """
    self.assertTrue(isinstance(self.TECL["motive_data"],dict))
    
  # What follows is possibly the jankiest way to test the interface of motive_data
  def test_motive_data_saturation_pt_exists(self):
    """
    TECL["motive_data"]["saturation_pt"] should exist.
    """
    self.assertTrue("saturation_pt",self.TECL["motive_data"])
    
  def test_motive_data_saturation_pt_is_dict(self):
    """
    TECL["motive_data"]["saturation_pt"] is a dictionary.
    """
    self.assertTrue(isinstance(self.TECL["motive_data"]["saturation_pt"],dict))
    
  def test_motive_data_saturation_pt_output_voltage_exists(self):
    """
    TECL["motive_data"]["saturation_pt"]["output_voltage"] exists.
    """
    self.assertTrue("output_voltage",self.TECL["motive_data"]["saturation_pt"])
    
  def test_motive_data_saturation_pt_output_voltage_is_num(self):
    """
    TECL["motive_data"]["saturation_pt"]["output_voltage"] is a number.
    """
    self.assertTrue(isinstance(\
      self.TECL["motive_data"]["saturation_pt"]["output_voltage"],(float,int,long)))
    
  def test_motive_data_saturation_pt_output_current_density_exists(self):
    """
    TECL["motive_data"]["saturation_pt"]["output_current_density"] exists.
    """
    self.assertTrue("output_current_density",self.TECL["motive_data"]["saturation_pt"])
    
  def test_motive_data_saturation_pt_output_current_density_is_num(self):
    """
    TECL["motive_data"]["saturation_pt"]["output_current_density"] is a number.
    """
    self.assertTrue(isinstance(\
      self.TECL["motive_data"]["saturation_pt"]["output_current_density"],(float,int,long)))
    
  def test_motive_data_saturation_pt_co_motive_exists(self):
    """
    TECL["motive_data"]["saturation_pt"]["co_motive"] exists.
    """
    self.assertTrue("co_motive",self.TECL["motive_data"]["saturation_pt"])
    
  def test_motive_data_saturation_pt_co_motive_is_num(self):
    """
    TECL["motive_data"]["saturation_pt"]["co_motive"] is a number.
    """
    self.assertTrue(isinstance(\
      self.TECL["motive_data"]["saturation_pt"]["co_motive"],(float,int,long)))
    
  def test_motive_data_saturation_pt_co_position_exists(self):
    """
    TECL["motive_data"]["saturation_pt"]["co_position"] exists.
    """
    self.assertTrue("co_position",self.TECL["motive_data"]["saturation_pt"])
    
  def test_motive_data_saturation_pt_co_position_is_num(self):
    """
    TECL["motive_data"]["saturation_pt"]["co_position"] is a number.
    """
    self.assertTrue(isinstance(\
      self.TECL["motive_data"]["saturation_pt"]["co_position"],(float,int,long)))
    


if __name__ == '__main__':
  unittest.main()
