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
      
  def test_calc_output_voltage(self):
    """
    """
    pass
      
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
    Mostly this method has relative uncertainty ~1e-5. Exceptions listed below.
    
    The absolute uncertainty of calc_output_current_density() is given by the larger of calc_forward_current_density() or calc_back_current_density(). Care must be taken when the forward and back currents approach the same value. In this case the output current approaches zero and the uncertainty analysis becomes more nuanced.
    
    The absolute uncertainty of the output current density can be written 
    
      δJ = (δJF**2 + δJB**2)**(1/2)
	 = ( (δJF/JF * JF)**2 + (δJB/JB * JB)**2 )**(1/2)
	 
    Since the relative uncertainties of the forward and back current are equal, they can be factored out.
    
      δJ = δJF/JF * (JF**2 + JB**2)**(1/2)
      
    The relative uncertainty of the output current can be obtained by dividing by J, performing some algebra, and expanding.
    
      δJ/J = δJF/JF * ( (JF**2 + JB**2)/(JF-JB)**2 )**(1/2)
      
    In both cases (absolute and relative uncertainty), it is clear that the uncertainty of the output current is roughly the uncertainty of the forward or back current in the event that one is substantially bigger than the other. In almost every interesting case, the forward current will be substantially bigger than the back current and the uncertainty of the output current will essentially equal the uncertainty of the forward current.
    
    When the forward current and back current approach the same value, the output current approaches zero and the expression for absolute ucertainty should be used to evaluate the uncertainty of the zero.
    
      δJ = δJF/JF * (JF**2 + JB**2)**(1/2)
      
    If the magnitude of JF and JB are large, the precision of the zero of the output current will be poor. For example, say JF and JB are on the order of 1e4 A m^{-2} (1A cm^{-2}). This magnitude is not unreasonable, but in this case at best we can know the zero of the output current to only one decimal point (the relative uncertanty of the forward current is ~1e-5).
    
    If the magnitude of JF and JB are small, the precision of the zero of the output current will be good. This case is the most liekly. Why is it likely? Its likely because of the current retardation effects either due to the negative space charge effect or due to the vacuum level of the collector reaching a point where forward electrons are blocked.
    
    A good way to evaluate the worst-case-scenario of the absolute precision of the output current density is to look at the value of the saturation current of hte emitter and collector. The collector value is likely small; this small value is the upper limit and will only decrease due to effects like the negative space charge effect. The point is that this small value represents the upper limit in terms of absolute precision of the output current density.
    
    We also need to consider the relative uncertainty of the output current density.
    
      δJ/J = δJF/JF * ( (JF**2 + JB**2)/(JF - JB)**2 )**(1/2)
      
    As J approaches zero, this expression blows up. We can determine a ratio of back current to forward current for which the relative uncertanty equal to or greater than unity. In this case, the value of the quantity would be more precise than the uncertanty. We can calculate the forward and back current values that make the relative uncertanty of the output current density greater than unity.
    
      <2012.12.22 p15>
      
    The takeaway from this analysis is that there is a ratio of JB to JF for which the relative uncertainty of the output current density is nonsense. This ratio depends on the relative uncertanty of the forward/back current.
    
    It bears repeating that for most cases of interest, the output current isn't close enough to zero for this detailed analysis to apply. WHen the output current is nearly zero, the absolute precision is taill probably pretty good. There's only a very limited set of cases where the output current is nearly zero, the uncertanty is poor, and someone is interested.
    
    If the user does have an interest in the case where the ou4tput current is nearly zero, the user should first evaluate the output current of both electrodes. The smaller of the two fixes the upper limit of the absolute uncertatinty of the output current density. The user should then evaluate the magnitude of the forward or back current density at the potin where the output current is zero. If they are small, the absolute ucertainty of the otuptu current density is small. If not, then the user has a truly spacecial case and should proceed with caution.
    
    The moral of this story: use care when the output current density is nearly zero.
    """
    pass
  
  def test_calc_output_power_density(self):
    """
    In most cases, the relative uncertainty of the output power density is 1e-5.
  
    Care must be taken when the forward and back current densities approach the same value. 
  
    The relative uncertainty of the output power density can be written
  
      δw/w = ( (δJ/J)**2 + (δV/V)**2 )**(1/2)
    
    Substituting the expression for the relative uncertainty of the output current density
  
      δw/w = ( (δJF/JF)**2 * (JF**2 + JB**2)/(JF - JB)**2 + (δV/V)**2 )**(1/2)
    
    From this expression it is clear that the relative uncertainty of the output power density blows up as JF and JB approach the same value. Since the upper limit of the relative uncertainty is unity, we can calculate values of JF and JB for which the relative uncertainty is greater than unity.
  
      <2012.12.24 p2>
    
    The roots of this expression show the ratios of JB/JF for which the relative uncertainty of the output power density makes no sense.
  
    An expression for the absolute uncertainty of the output power density can be derived from the expression for the relative uncertainty.
  
      δw/w = ( (δJF/JF)**2 * (JF**2 + JB**2)/(JF - JB)**2 + (δV/V)**2 )**(1/2)
      δw = w * ( (δJF/JF)**2 * (JF**2 + JB**2)/(JF - JB)**2 + (δV/V)**2 )**(1/2)
	 = (V**2 * (δJF/JF)**2 * (JF**2 + JB**2) + J**2 * V**2 * (δV/V)**2 )**(1/2)
       
    Pretty much all the caveats about uncertainty near zero of the output current density apply to this quantity.
    """
    pass

if __name__ == '__main__':
  unittest.main()
