#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests methods of the TEC class.
"""

__author__ = "Joshua Ryan Smith (joshua.r.smith@gmail.com)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2012 Joshua Ryan Smith"
__license__ = ""

from tec import TEC
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
  
  def test_calc_interelectrode_spacing(self):
    """
    Compares the output against a list of standard values.
    
    This method has machine precision since it is a difference between to machine precise values.
    """
    f = open("test/TEC.calc_interelectrode_spacing_STANDARD.dat","r")
    standard_values = pickle.load(f)
    f.close()
    
    for params in standard_values:
      tec = TEC(params)
      self.assertAlmostEqual(tec.calc_interelectrode_spacing(),params["d"])
      
  def test_calc_contact_potential(self):
    """
    Compares the output against a list of standard values.
    
    This method has machine precision. When the barrier_ht attribute of an Electrode object is set, the quantity is converted from eV to J by multiplying by the value of the fundamental charge. Even though the machine does a machine precision multiplication, the value of  the fundamental charge has a lower relative precision than the mahcine. So there are a bunch of digits that get carried around that are insignificant. However, this calc_contact_potential calculation, the result is divided by the value of the fundamental charge to get the result in V. This division recovers the original precision of  the values of barrier_ht and therefore the result is of machine precision.
    """
    pass
  
  def test_calc_forward_current_density(self):
    """
    This method has uncertainty equivalent to Electrode.calc_output_current() via an analogous argument.
    """
    pass
  
  def test_calc_back_current_density(self):
    """
    This method has uncertainty equivalent to Electrode.calc_output_current() via an analogous argument.
    """
    pass
  
  def test_calc_output_current_density(self):
    """
    This method has uncertainty equivalent to Electrode.calc_output_current().
    
      J = JF - JB
      δJ = (δJF**2 + δJB**2)**(1/2)
         = ((δJF/JF * JF)**2 + (δJB/JB * JB)**2)**(1/2)
         
    know
    
      δJF/JF = δJB/JB
      
    thus
    
      δJ = δJF/JF * (JF**2 + JB**2)**(1/2)
      
    divide by J
    
      δJ/J = (1/J) * δJF/JF * (JF**2 + JB**2)**(1/2)
           = δJF/JF * ((JF**2 + JB**2) / J**2)**(1/2)
           = δJF/JF * ((JF**2 + JB**2) / (JF - JB)**2)**(1/2)
    """
    pass
  

if __name__ == '__main__':
  unittest.main()
