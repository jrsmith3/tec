#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Tests API of the TEC class.
"""

__author__ = "Joshua Ryan Smith (joshua.r.smith@gmail.com)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2012 Joshua Ryan Smith"
__license__ = ""

from tec import TEC
import unittest

class InstantiationBadInput(unittest.TestCase):
  """
  Tests the instantiation with bad input.
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
    

  # No input argument
  # =================
  def test_TEC_no_input_arg(self):
    """Attempt to instantiate TEC with no input argument."""
    self.assertRaises(TypeError,TEC,None)
  
  # Non-dict input argument
  # =======================
  def test_TEC_non_dict_input_arg(self):
    """Attempt to instantiate Electrode with a non-dict input argument."""
    self.assertRaises(TypeError,TEC,"this string is not a dict.")

  # Missing required fields in input dict
  # =====================================
  def test_TEC_input_arg_sans_Emitter(self):
    """Instantiating argument missing Emitter."""
    del(self.input_params["Emitter"])
    self.assertRaises(KeyError,TEC,self.input_params)
  
  def test_TEC_input_arg_sans_Collector(self):
    """Instantiating argument missing Emitter."""
    del(self.input_params["Collector"])
    self.assertRaises(KeyError,TEC,self.input_params)  
  
  # Emitter
  # -------
  def test_TEC_input_arg_sans_em_temp(self):
    """Instantiating argument missing Emitter temp."""
    del(self.input_params["Emitter"]["temp"])
    self.assertRaises(KeyError,TEC,self.input_params)

  def test_TEC_input_arg_sans_em_barrier_ht(self):
    """Instantiating argument missing Emitter barrier_ht."""
    del(self.input_params["Emitter"]["barrier_ht"])
    self.assertRaises(KeyError,TEC,self.input_params)

  def test_TEC_input_arg_sans_em_voltage(self):
    """Instantiating argument missing Emitter voltage."""
    del(self.input_params["Emitter"]["voltage"])
    self.assertRaises(KeyError,TEC,self.input_params)

  def test_TEC_input_arg_sans_em_position(self):
    """Instantiating argument missing Emitter position."""
    del(self.input_params["Emitter"]["position"])
    self.assertRaises(KeyError,TEC,self.input_params)

  def test_TEC_input_arg_sans_em_richardson(self):
    """Instantiating argument missing Emitter richardson."""
    del(self.input_params["Emitter"]["richardson"])
    self.assertRaises(KeyError,TEC,self.input_params)

  def test_TEC_input_arg_sans_em_emissivity(self):
    """Instantiating argument missing Emitter emissivity."""
    del(self.input_params["Emitter"]["emissivity"])
    self.assertRaises(KeyError,TEC,self.input_params)

  # Collector
  # ---------
  def test_TEC_input_arg_sans_co_temp(self):
    """Instantiating argument missing Collector temp."""
    del(self.input_params["Collector"]["temp"])
    self.assertRaises(KeyError,TEC,self.input_params)

  def test_TEC_input_arg_sans_co_barrier_ht(self):
    """Instantiating argument missing Collector barrier_ht."""
    del(self.input_params["Collector"]["barrier_ht"])
    self.assertRaises(KeyError,TEC,self.input_params)

  def test_TEC_input_arg_sans_co_voltage(self):
    """Instantiating argument missing Collector voltage."""
    del(self.input_params["Collector"]["voltage"])
    self.assertRaises(KeyError,TEC,self.input_params)

  def test_TEC_input_arg_sans_co_position(self):
    """Instantiating argument missing Collector position."""
    del(self.input_params["Collector"]["position"])
    self.assertRaises(KeyError,TEC,self.input_params)

  def test_TEC_input_arg_sans_co_richardson(self):
    """Instantiating argument missing Collector richardson."""
    del(self.input_params["Collector"]["richardson"])
    self.assertRaises(KeyError,TEC,self.input_params)

  def test_TEC_input_arg_sans_co_emissivity(self):
    """Instantiating argument missing Collector emissivity."""
    del(self.input_params["Collector"]["emissivity"])
    self.assertRaises(KeyError,TEC,self.input_params)

  # Input dict values are non-numeric
  # =================================
  # Emitter
  # -------
  def test_TEC_input_em_temp_non_numeric(self):
    """Instantiating argument Emitter temp is non-numeric."""
    self.input_params["Emitter"]["temp"] = "this string is non-numeric."
    self.assertRaises(TypeError,TEC,self.input_params)

  def test_TEC_input_em_barrier_ht_non_numeric(self):
    """Instantiating argument Emitter barrier_ht is non-numeric."""
    self.input_params["Emitter"]["barrier_ht"] = "this string is non-numeric."
    self.assertRaises(TypeError,TEC,self.input_params)

  def test_TEC_input_em_voltage_non_numeric(self):
    """Instantiating argument Emitter voltage is non-numeric."""
    self.input_params["Emitter"]["voltage"] = "this string is non-numeric."
    self.assertRaises(TypeError,TEC,self.input_params)

  def test_TEC_input_em_position_non_numeric(self):
    """Instantiating argument Emitter position is non-numeric."""
    self.input_params["Emitter"]["position"] = "this string is non-numeric."
    self.assertRaises(TypeError,TEC,self.input_params)

  def test_TEC_input_em_richardson_non_numeric(self):
    """Instantiating argument Emitter richardson is non-numeric."""
    self.input_params["Emitter"]["richardson"] = "this string is non-numeric."
    self.assertRaises(TypeError,TEC,self.input_params)

  def test_TEC_input_em_emissivity_non_numeric(self):
    """Instantiating argument Emitter emissivity is non-numeric."""
    self.input_params["Emitter"]["emissivity"] = "this string is non-numeric."
    self.assertRaises(TypeError,TEC,self.input_params)

  def test_TEC_input_em_nea_non_numeric(self):
    """Instantiating argument Emitter nea is non-numeric."""
    self.input_params["Emitter"]["nea"] = "this string is non-numeric."
    self.assertRaises(TypeError,TEC,self.input_params)

  # Collector
  # -------
  def test_TEC_input_co_temp_non_numeric(self):
    """Instantiating argument Collector temp is non-numeric."""
    self.input_params["Collector"]["temp"] = "this string is non-numeric."
    self.assertRaises(TypeError,TEC,self.input_params)

  def test_TEC_input_co_barrier_ht_non_numeric(self):
    """Instantiating argument Collector barrier_ht is non-numeric."""
    self.input_params["Collector"]["barrier_ht"] = "this string is non-numeric."
    self.assertRaises(TypeError,TEC,self.input_params)

  def test_TEC_input_co_voltage_non_numeric(self):
    """Instantiating argument Collector voltage is non-numeric."""
    self.input_params["Collector"]["voltage"] = "this string is non-numeric."
    self.assertRaises(TypeError,TEC,self.input_params)

  def test_TEC_input_co_position_non_numeric(self):
    """Instantiating argument Collector position is non-numeric."""
    self.input_params["Collector"]["position"] = "this string is non-numeric."
    self.assertRaises(TypeError,TEC,self.input_params)

  def test_TEC_input_co_richardson_non_numeric(self):
    """Instantiating argument Collector richardson is non-numeric."""
    self.input_params["Collector"]["richardson"] = "this string is non-numeric."
    self.assertRaises(TypeError,TEC,self.input_params)

  def test_TEC_input_co_emissivity_non_numeric(self):
    """Instantiating argument Collector emissivity is non-numeric."""
    self.input_params["Collector"]["emissivity"] = "this string is non-numeric."
    self.assertRaises(TypeError,TEC,self.input_params)

  def test_TEC_input_co_nea_non_numeric(self):
    """Instantiating argument Collector nea is non-numeric."""
    self.input_params["Collector"]["nea"] = "this string is non-numeric."
    self.assertRaises(TypeError,TEC,self.input_params)



  # Input dict values are outside their constraints
  # ===============================================
  # Emitter
  # -------
  def test_TEC_input_em_temp_less_than_zero(self):
    """Instantiating argument Emitter temp < 0."""
    self.input_params["Emitter"]["temp"] = -1.1
    self.assertRaises(ValueError,TEC,self.input_params)
  
  def test_TEC_input_em_barrier_ht_less_than_zero(self):
    """Instantiating argument Emitter barrier_ht < 0."""
    self.input_params["Emitter"]["barrier_ht"] = -1.1
    self.assertRaises(ValueError,TEC,self.input_params)
  
  def test_TEC_input_em_richardson_less_than_zero(self):
    """Instantiating argument Emitter richardson < 0."""
    self.input_params["Emitter"]["richardson"] = -1.1
    self.assertRaises(ValueError,TEC,self.input_params)
  
  def test_TEC_input_em_emissivity_less_than_zero(self):
    """Instantiating argument Emitter emissivity < 0."""
    self.input_params["Emitter"]["emissivity"] = -1.1
    self.assertRaises(ValueError,TEC,self.input_params)
  
  def test_TEC_input_em_emissivity_greater_than_one(self):
    """Instantiating argument Emitter emissivity > 1."""
    self.input_params["Emitter"]["emissivity"] = 1.1
    self.assertRaises(ValueError,TEC,self.input_params)
  
  def test_TEC_input_em_nea_less_than_zero(self):
    pass

  # Collector
  # -------
  def test_TEC_input_co_temp_less_than_zero(self):
    """Instantiating argument Collector temp < 0."""
    self.input_params["Collector"]["temp"] = -1.1
    self.assertRaises(ValueError,TEC,self.input_params)
  
  def test_TEC_input_co_barrier_ht_less_than_zero(self):
    """Instantiating argument Collector barrier_ht < 0."""
    self.input_params["Collector"]["barrier_ht"] = -1.1
    self.assertRaises(ValueError,TEC,self.input_params)
  
  def test_TEC_input_co_richardson_less_than_zero(self):
    """Instantiating argument Collector richardson < 0."""
    self.input_params["Collector"]["richardson"] = -1.1
    self.assertRaises(ValueError,TEC,self.input_params)
  
  def test_TEC_input_co_emissivity_less_than_zero(self):
    """Instantiating argument Collector emissivity < 0."""
    self.input_params["Collector"]["emissivity"] = -1.1
    self.assertRaises(ValueError,TEC,self.input_params)
  
  def test_TEC_input_co_emissivity_greater_than_one(self):
    """Instantiating argument Collector emissivity > 1."""
    self.input_params["Collector"]["emissivity"] = 1.1
    self.assertRaises(ValueError,TEC,self.input_params)
  
  def test_TEC_input_co_nea_less_than_zero(self):
    pass

if __name__ == '__main__':
  unittest.main()
