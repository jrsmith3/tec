# -*- coding: utf-8 -*-

from electrode import Electrode
from constants import physical_constants
from tec import TEC
import numpy as np
from scipy import interpolate,optimize,integrate,special

class DimensionlessLangmuirPoissonSoln(dict):
  """
  Approximation of solution of Langmuir's dimensionless Poisson's equation.
  """
  
  def __init__(self):
    
    # Here is the algorithm:
    # 1. Set up the default ode solver parameters.
    # 2. Check to see if either the rhs or lhs params were passed as arguments. If not, use the default params.
    # 3. Cat the additional default ode solver parameters to the lhs and rhs set of params.
    # 4. Solve both the lhs and rhs odes.
    # 5. Create the lhs and rhs interpolation objects.
    
    self["lhs"] = self.calc_branch(-2.5538,"lhs")
    self["rhs"] = self.calc_branch(100.,"rhs")
      
  def calc_branch(self, endpoint, side, num_points = 1000):
    """
    Calculates data for either the left or right hand side of the ode solution.
    """
    ics = np.array([0,0])
    position_array = np.linspace(0, endpoint, num_points)
    motive_array = integrate.odeint(self.langmuir_poisson_eq,ics,position_array)
    
    # Create the motive_v_position interpolation, but first check the abscissae (position_array) are monotonically increasing.
    if position_array[0] < position_array[-1]:
      motive_v_position = \
        interpolate.InterpolatedUnivariateSpline(position_array,motive_array[:,0])
    else:
      motive_v_position = \
        interpolate.InterpolatedUnivariateSpline(position_array[::-1],motive_array[::-1,0])
      
    # Now create the position_v_motive interpolation but first check the abscissae (motive_array in this case) are monotonically increasing. Use linear interpolation to avoid weirdness near the origin.
    
    # I think I don't need the following block.
    if motive_array[0,0] < motive_array[-1,0]:
      position_v_motive = \
        interpolate.InterpolatedUnivariateSpline(motive_array[:,0],position_array,k=1)
    else:
      position_v_motive = \
        interpolate.InterpolatedUnivariateSpline(motive_array[::-1,0],position_array[::-1],k=1)
      
    return {"motive_v_position": motive_v_position, 
            "position_v_motive": position_v_motive}
  
  def get_position(self, motive, branch = "lhs"):
    """
    Return position, default negative, given a value of motive.
    """
    
    if type(branch) is not str:
      raise TypeError("branch must be of type str.")
    #if branch is not "lhs" or "rhs":
      #raise ValueError("branch must either be 'lhs' or 'rhs'.")
    
    if motive < 0:
      return np.NaN

    #if branch is "lhs" or branch is "rhs":
    if branch is "lhs" and motive > 18.7:
      return -2.55389
    else:
      return self[branch]["position_v_motive"](motive)
  
  def get_motive(self, position):
    """
    Return motive given a value of position.
    """
    if position < -2.55389:
      return np.NaN
    elif position <= 0:
      return self["lhs"]["motive_v_position"](position)
    else:
      return self["rhs"]["motive_v_position"](position)
  
  def langmuir_poisson_eq(self, motive, position):
    """
    Langmuir's dimensionless Poisson's equation for the ODE solver.
    """
    
    # Note:
    # motive[0] = motive.
    # motive[1] = motive[0]'
    
    if position >= 0:
      return np.array([ motive[1],\
        0.5*np.exp(motive[0])*(1-special.erf( motive[0]**0.5 )) ])
        
    if position < 0:
      return np.array([ motive[1],\
        0.5*np.exp(motive[0])*(1+special.erf( motive[0]**0.5 )) ])


class Langmuir(TECBase):
  """
  Thermionic engine simulator. Considers space charge, ignores NEA.

  dict-like object that implements a model of electron transport including the negative space charge effect. This class explicitly ignores the fact that either electrode may have NEA and determines the vacuum level of an electrode at the barrier. The model is based on [1].

  Attributes
  ----------
  The attributes of the object are accessed like a dictionary. The object has three attributes; "Emitter" and "Collector" are both Electrode objects. "motive_data" is a dictionary containing (meta)data calculated during the motive calculation. "motive_data" should usually be accessed via the class's convenience methods. "motive_data" contains the following data:

    saturation_pt: Dict containing saturation point data described below. Only 
                   contains dimensionless quantities at the collector since the
                   emitter dimensionless quantities are all zero by definition. 
                   For brevity, "dimensionless" prefix omitted from "position" 
                   and "motive" variable names.
    
      output_voltage:         Voltage at which the saturation point occurs.
      
      output_current_density: Current at which the saturation point occurs.
    
    critical_pt:   Dict containing critical point data described below. Only 
                   contains dimensionless quantities at the emitter since the
                   collector dimensionless quantities are all zero by 
                   definition. For brevity, "dimensionless" prefix omitted from 
                   "position" and "motive" variable names.

    
      output_voltage:         Voltage at which the critical point occurs.
      
      output_current_density: Current at which the critical point occurs.
      
    dps:           Langmuir's dimensionless Poisson's equation solution object.
      
  Parameters
  ----------
  The TEC_Langmuir class is instantiated by a dict with two keys, "Emitter" and "Collector" (case insensitive). Both keys have data that is also of type dict which are configured to instantiate an Electrode object. Additional keys will be ignored and there are no default values for instantiation.

  Examples and interface testing
  ------------------------------
  >>> from tec_langmuir import TEC_Langmuir
  >>> em_dict = {"temp":1000,
  ...            "barrier":1,
  ...            "voltage":0,
  ...            "position":0,
  ...            "richardson":10,
  ...            "emissivity":0.5}
  >>> co_dict = {"temp":300,
  ...            "barrier":0.8,
  ...            "voltage":0,
  ...            "position":10,
  ...            "richardson":10,
  ...            "emissivity":0.5}
  >>> input_dict = {"Emitter":em_dict, "Collector":co_dict}
  >>> example_tec = TEC_Langmuir(input_dict)
  
  Make sure that the motive_data interface matches the above description.
  
  >>> isinstance(example_tec["motive_data"]["saturation_pt"]["output_voltage"],float)
  True
  >>> isinstance(example_tec["motive_data"]["saturation_pt"]["output_current_density"],float)
  True
  >>> isinstance(example_tec["motive_data"]["critical_pt"]["output_voltage"],float)
  True
  >>> isinstance(example_tec["motive_data"]["critical_pt"]["output_current_density"],float)
  True
  >>> type(example_tec["motive_data"]["dps"])
  <class 'tec.dimensionlesslangmuirpoissonsoln.DimensionlessLangmuirPoissonSoln'>

  Notes
  -----

  Bibliography
  ------------
  [1] Langmuir
  """
  
  def calc_back_current_density(self):
    """
    Return back current density in A m^{-2}.
    """
    return 0.0
    
  def calc_motive(self):
    """
    Calculate the motive parameters and populate "motive_data".
    """
    # Throw out any nea attributes if they exist.
    # I feel like this code needs some explanation. The model this class implements assumes that neither electrode has NEA. Therefore, it doesn't make sense to allow anyone to set an "nea" attribute for either electrode. However, it is possible to instantiate a TEC_Langmuir object without either electrode having an "nea" attribute, then later set an "nea" attribute for one of the electrodes. It would be easy to check for "nea" during instantiation, but I would have to write a lot of ugly, hacky code to prevent either of the electrodes from acquiring an "nea" attribute later on. Since the calc_motive() method is presumably called whenever the TEC_Langmuir attributes (or sub-attributes) are called, the following block of code will notice if "nea" has been added to the electrodes, and will remove it.
    for electrode in ["Emitter","Collector"]:
      if "nea" in self[electrode]:
        del self[electrode]["nea"]
    
    # For brevity, "dimensionless" prefix omitted from "position" and "motive" variable names.
    
    self["motive_data"] = {}
    self["motive_data"]["dps"] = DimensionlessLangmuirPoissonSoln()
    
    self["motive_data"]["saturation_pt"] = self.calc_saturation_pt()
    self["motive_data"]["critical_pt"] = self.calc_critical_pt()
    
    if self.calc_output_voltage() < self["motive_data"]["saturation_pt"]["output_voltage"]:
      # Accelerating mode.
      self["motive_data"]["max_motive_ht"] = self["Emitter"].calc_motive_bc()
    elif self.calc_output_voltage() > self["motive_data"]["critical_pt"]["output_voltage"]:
      # Retarding mode.
      self["motive_data"]["max_motive_ht"] = self["Collector"].calc_motive_bc()
    else:
      # Space charge limited mode.
      output_current_density = optimize.brentq(self.output_voltage_target_function,\
        self["motive_data"]["saturation_pt"]["output_current_density"],\
        self["motive_data"]["critical_pt"]["output_current_density"])
        
      barrier = physical_constants["boltzmann"] * self["Emitter"]["temp"] * \
        np.log(self["Emitter"].calc_saturation_current()/output_current_density)
      self["motive_data"]["max_motive_ht"] = barrier + self["Emitter"].calc_motive_bc()
    
  def get_motive(self,pos):
    """
    Value of motive relative to ground for given value(s) of position in J.
    
    Position must be of numerical type or numpy array. Returns NaN if position 
    falls outside of the interelectrode space.
    """
    # For brevity, "dimensionless" prefix omitted from "position" and "motive" variable names. The "position" and "motive" variables refer to the dimensionless quantities, while "pos" and "mot" refer to the dimensioned quantities.
    em_motive = (self.get_max_motive_ht() - self["Emitter"].calc_barrier_ht()) / \
      (physical_constants["boltzmann"] * self["Emitter"]["temp"])
    em_position = self["motive_data"]["dps"].get_position(em_motive)
    
    position = pos * ((2 * np.pi * physical_constants["electron_mass"] * \
      physical_constants["electron_charge"]**2) / \
      (physical_constants["permittivity0"]**2 * physical_constants["boltzmann"]**3))**(1.0/4) * \
      (self.calc_output_current_density()**(1.0/2))/(self["Emitter"]["temp"]**(3.0/4)) + \
      em_position
      
    # What follows is some hacky code
      
    motive = []
      
    for p in position:
      motive.append(self["motive_data"]["dps"].get_motive(p))
    
    # Turn the list into a numpy array
    motive = np.array(motive)
    
    mot = self.get_max_motive_ht() - \
      physical_constants["boltzmann"] * self["Emitter"]["temp"] * motive
      
    return mot
  
  def get_max_motive_ht(self, with_position=False):
    """
    Returns value of the maximum motive relative to ground in J.
    
    If with_position is True, return the position at which the maximum motive occurs.
    """
    if with_position:
      em_motive = (self.get_max_motive_ht() - self["Emitter"].calc_barrier_ht()) / \
        (physical_constants["boltzmann"] * self["Emitter"]["temp"])
      em_position = self["motive_data"]["dps"].get_position(em_motive)
      
      return -1 * em_position * \
        ((physical_constants["permittivity0"]**2 * physical_constants["boltzmann"]**3)/\
        (2*np.pi*physical_constants["electron_mass"]*\
        physical_constants["electron_charge"]**2))**(1.0/4) * \
        (self["Emitter"]["temp"]**(3.0/4))/(self.calc_output_current_density()**(1.0/2))
    else:
      return self["motive_data"]["max_motive_ht"]
  
  def calc_saturation_pt(self):
    """
    Calculate and return saturation point condition.
    
    Returns dict with keys output_voltage and output_current_density with values in [V] and [A m^-2], respectively.
    """    
    # For brevity, "dimensionless" prefix omitted from "position" and "motive" variable names.
    output_current_density = self["Emitter"].calc_saturation_current()
    
    position = self.calc_interelectrode_spacing() * \
      ((2 * np.pi * physical_constants["electron_mass"] * physical_constants["electron_charge"]**2) / \
      (physical_constants["permittivity0"]**2 * physical_constants["boltzmann"]**3))**(1.0/4) * \
      (output_current_density**(1.0/2))/(self["Emitter"]["temp"]**(3.0/4))
      
    motive = self["motive_data"]["dps"].get_motive(position)
    
    output_voltage = (self["Emitter"]["barrier"] - \
      self["Collector"]["barrier"] - \
      motive * physical_constants["boltzmann"] * self["Emitter"]["temp"]) / \
      physical_constants["electron_charge"]
    
    return {"output_voltage":output_voltage,
	    "output_current_density":output_current_density}
  
  def calc_critical_pt(self):
    """
    Calculate and return critical point condition.
    
    Returns dict with keys output_voltage and output_current_density with values in [V] and [A m^-2], respectively.
    """
    # For brevity, "dimensionless" prefix omitted from "position" and "motive" variable names.
    
    # Rootfinder to get critical point output current density.
    output_current_density = optimize.brentq(self.critical_point_target_function,\
      self["Emitter"].calc_saturation_current(),0)
    
    position = -self.calc_interelectrode_spacing() * \
      ((2 * np.pi * physical_constants["electron_mass"] * physical_constants["electron_charge"]**2) / \
      (physical_constants["permittivity0"]**2 * physical_constants["boltzmann"]**3))**(1.0/4) * \
      (output_current_density**(1.0/2))/(self["Emitter"]["temp"]**(3.0/4))
      
    motive = np.log(self["Emitter"].calc_saturation_current()/output_current_density)
    
    output_voltage = (self["Emitter"]["barrier"] - \
      self["Collector"]["barrier"] + \
      motive * physical_constants["boltzmann"] * self["Emitter"]["temp"]) / \
      physical_constants["electron_charge"]
    
    return {"output_voltage":output_voltage,
	    "output_current_density":output_current_density}
       
  
  def critical_point_target_function(self,output_current_density):
    """
    Target function for critical point rootfinder.
    """
    position = -self.calc_interelectrode_spacing() * \
      ((2 * np.pi * physical_constants["electron_mass"] * physical_constants["electron_charge"]**2) / \
      (physical_constants["permittivity0"]**2 * physical_constants["boltzmann"]**3))**(1.0/4) * \
      (output_current_density**(1.0/2))/(self["Emitter"]["temp"]**(3.0/4))
      
    if output_current_density == 0:
      motive = np.inf
    else:
      motive = np.log(self["Emitter"].calc_saturation_current()/output_current_density)
    
    return position - self["motive_data"]["dps"].get_position(motive)

  def output_voltage_target_function(self,output_current_density):
    """
    Target function for the output voltage rootfinder.
    """
    # For brevity, "dimensionless" prefix omitted from "position" and "motive" variable names.
    em_motive = np.log(self["Emitter"].calc_saturation_current()/output_current_density)
    em_position = self["motive_data"]["dps"].get_position(em_motive)
    
    x0 = ((physical_constants["permittivity0"]**2 * physical_constants["boltzmann"]**3) / \
      (2*np.pi*physical_constants["electron_mass"]*physical_constants["electron_charge"]**2))**(1./4) * \
      self["Emitter"]["temp"]**(3./4) / output_current_density**(1./2)
    
    co_position = self.calc_interelectrode_spacing()/x0 + em_position
    co_motive = self["motive_data"]["dps"].get_motive(co_position)
    
    return self.calc_output_voltage() - ((self["Emitter"]["barrier"] + \
      em_motive * physical_constants["boltzmann"] * self["Emitter"]["temp"]) - \
      (self["Collector"]["barrier"] + \
      co_motive * physical_constants["boltzmann"] * self["Emitter"]["temp"]))/ \
      physical_constants["electron_charge"]
      