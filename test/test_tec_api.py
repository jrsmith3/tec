#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Tests API of the TEC class.

I will eventually need to fix this note, but here it is. I am intentionally not
testing the cases where the sub-dicts have incorrect data. The Electrode tests
deal with these cases comprehensively and there is no additional logic at the 
TEC level. In the event that I do need to test these cases, I can always reach
back in the VCS history and grab the previous version of this file.
"""

__author__ = "Joshua Ryan Smith (joshua.r.smith@gmail.com)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2012 Joshua Ryan Smith"
__license__ = ""

from tec import TEC
import unittest

class InstantiationInputNonDict(unittest.TestCase):
  """
  Tests instantiation when non-dict data is used.
  """

  def test_TEC_no_input_arg(self):
    """Attempt to instantiate TEC with no input argument."""
    self.assertRaises(TypeError,TEC,None)
  
  def test_TEC_non_dict_input_arg(self):
    """Attempt to instantiate Electrode with a non-dict input argument."""
    self.assertRaises(TypeError,TEC,"this string is not a dict.")


class InstantiationInputIncomplete(unittest.TestCase):
  """
  Tests instantiating when input dict is missing required data.
  """
  
  def setUp(self):
    """
    Set up a dictionary that can properly instantiate a TEC object.
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
    
  def test_TEC_input_arg_sans_Emitter(self):
    """Instantiating argument missing Emitter."""
    del(self.input_params["Emitter"])
    self.assertRaises(KeyError,TEC,self.input_params)
  
  def test_TEC_input_arg_sans_Collector(self):
    """Instantiating argument missing Emitter."""
    del(self.input_params["Collector"])
    self.assertRaises(KeyError,TEC,self.input_params)  
  
class InstantiationInputFieldsWrongType(unittest.TestCase):
  """
  Tests instantiating when input dict has non-numeric data items.
  """

  def setUp(self):
    """
    Set up a dictionary that can properly instantiate a TEC object.
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

  def test_TEC_input_Emitter_non_numeric(self):
    """Instantiating argument Emitter is non-numeric."""
    self.input_params["Emitter"] = "this string is non-numeric."
    self.assertRaises(TypeError,TEC,self.input_params)
  
  def test_TEC_input_Collector_non_numeric(self):
    """Instantiating argument Collector is non-numeric."""
    self.input_params["Collector"] = "this string is non-numeric."
    self.assertRaises(TypeError,TEC,self.input_params)
  

class SetInputWrongType(unittest.TestCase):
  """
  Tests setting attributes when input data is non-numeric.
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
                 "position":0,\
                 "richardson":10,\
                 "emissivity":0.5}
                 
    input_params = {"Emitter":em_params, "Collector":co_params}
                   
    self.TEC_obj = TEC(input_params)
    
  def test_TEC_set_Emitter_non_numeric(self):
    """Set argument Emitter non-numeric."""
    non_num = "this string is non-numeric."
    self.assertRaises(TypeError,self.TEC_obj["Emitter"],non_num)

  def test_TEC_set_Collector_non_numeric(self):
    """Set argument Collector non-numeric."""
    non_num = "this string is non-numeric."
    self.assertRaises(TypeError,self.TEC_obj["Collector"],non_num)
    
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
                 "position":0,\
                 "richardson":10,\
                 "emissivity":0.5}
                 
    input_params = {"Emitter":em_params, "Collector":co_params}
                   
    self.TEC_obj = TEC(input_params)
    

if __name__ == '__main__':
  unittest.main()
