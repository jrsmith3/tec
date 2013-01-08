#!/usr/bin/env python
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
import pickle

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
    
  def test_calc_saturation_current_values(self):
    """
    Saturation current values test.
    
    This method follows the numerical testing strategy as laid out in the README 
    document. The script 
    
      Electrode.calc_saturation_current_STANDARD.py
      
    was used to generate the standard data which can be found in the 
    corresponding .dat file.
    
    The uncertainty of this method is ~1e-5.

    Uncertainty analysis
    ====================
    
    The return value of this method is given by the Richardson Dushman equation. 
    According to Taylor (ISBN: 978-0-935702-42-2) p. 75, the uncertainty of the 
    value of the output current density is
    
      δJ/J = ( (δA/A)**2 + 2*(δT/T)**2 + 
        exp(-2ϕ/kT)((δT/T)**2 + (δϕ/ϕ)**2 + (δk/k)**2) )**(1/2)        (1)
        
    Where
      J: output current density
      A: Richardson's constant
      T: temperature
      ϕ: barrier height
      k: Boltzmann's constant
      
    The uncertainty of the output current depends on the uncertainties of the 
    quantities listed above. I assume that the Richardson's constant, 
    temperature, and barrier height all have machine precision. According to 
    NIST [1], Boltzmann's constant has a precision of ~1e-6 which I interpret as 
    I can believe the values of numerals up to and including 1e-5 places behind 
    the decimal in scientific notation.
    
    The Eq. 1 above breaks down into two parts: the sum of the first two terms, 
    and the product of the exponentiation. The uncertainty of the output current 
    depends on the value of the exponentiation. The maximum limit of the 
    exponentiation is unity. This condition implies that either ϕ -> 0 or 
    T -> inf. In this case, Eq. 1 becomes
    
      δJ/J = ( (δA/A)**2 + 3*(δT/T)**2 + (δϕ/ϕ)**2 + (δk/k)**2 )**(1/2)
    
    The largest term is the uncertainty in Boltzmann's constant. Therefore the 
    uncertainty in output current density is set by the uncertainty in 
    Boltzmann's constant.
    
    The minimum limit of exponentiation is zero. This condition implies that 
    either ϕ -> inf or T -> 0. In this case, Eq. 1 becomes
    
      δJ/J = ( (δA/A)**2 + 2*(δT/T)**2 )**(1/2)
      
    Both the Richardson's constant and temperature are assumed to have machine 
    precision, so the uncertainty in the output current is slightly worse than 
    machine precision.
    
    Since the uncertainty of Boltzmann's constant is greater than the 
    uncertainty of 64 bit floats, the output current will have a maximum 
    uncertainty given by the uncertainty of Boltzmann's constant.
    
    [1] http://physics.nist.gov/cgi-bin/cuu/Value?tkev|search_for=boltzmann
    """
    f = open("test/Electrode.calc_saturation_current_STANDARD.dat","r")
    standard_values = pickle.load(f)
    f.close()
    
    for stdparams in standard_values:
      # Concatenate the parameters from std with the dummy input_params.
      params = dict(list(self.input_params.items()) + list(stdparams.items()))
      el = Electrode(params)
      self.assertAlmostEqual(el.calc_saturation_current(),params["outpt_cur"])



  def test_calc_vacuum_energy_values(self):
    """
    Vacuum energy values test.
    
    This method follows the numerical testing strategy as laid out in the README 
    document. The script 
    
      xx.py
      
    was used to generate the standard data which can be found in the 
    corresponding .dat file.
    
    The uncertainty of this method is ~1e-7.

    Uncertainty analysis
    ====================
    
    The return value of this method is given by a simple sum of terms shown in 
    Eq. 1
    
      Evac = eV + ξ - χ         (1)
      
    Where 
      e is the fundamental charge
      V is the voltage at which the electrode is held
      ξ is the barrier height
      χ is the negative electron affinity, if one exists
      
    It is important to note that the values of ξ and χ have been converted to 
    units of joules from units of electron volts. This conversion was done by 
    multiplying the value in eV by the value of the fundamental charge. I assume 
    that ξ and χ are input to machine precision, but this conversion reduces the 
    precision since there is uncertainty in the value of the electron charge. 
    With this conversion in mind, Eq. 1 is essentially
    
      Evac = e(V + ξ - χ)         (2)
    
    Where V, ξ, and χ are all machine precision. The uncertainty analysis of 
    this case is very simple, boiling down to the product of two uncertainties 
    as
    
      δEvac/Evac = ( (δe/e)**2 + (δV/V)**2 )**(1/2)               (3)
      
    Where I have suppressed the effects of ξ and χ since they don't actually 
    make a big difference in the result. The uncertainty in Evac is therefore 
    equal to the uncertainty in e. According to NIST [1], the uncertainty in e 
    is ~1e-7.
    
    [1] http://physics.nist.gov/cgi-bin/cuu/Value?e|search_for=electron+charge
    """
    f = open("test/Electrode.calc_vacuum_energy_STANDARD.dat","r")
    standard_values = pickle.load(f)
    f.close()
    
    for params in standard_values:
      el = Electrode(params)
      self.assertAlmostEqual(el.calc_saturation_current(),params["e_vac"])
  

if __name__ == '__main__':
  unittest.main()
