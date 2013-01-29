# -*- coding: utf-8 -*-

from electrode import Electrode
from constants import physical_constants
from dimensionlesslangmuirpoissonsoln import DimensionlessLangmuirPoissonSoln
from tec import TEC
import numpy as np
from scipy import interpolate

class TEC_Langmuir(TEC):
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
  ...            "barrier_ht":1,
  ...            "voltage":0,
  ...            "position":0,
  ...            "richardson":10,
  ...            "emissivity":0.5}
  >>> co_dict = {"temp":300,
  ...            "barrier_ht":0.8,
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
    # For brevity, "dimensionless" prefix omitted from "position" and "motive" variable names.
    
    self["motive_data"] = {}
    self["motive_data"]["dps"] = DimensionlessLangmuirPoissonSoln()
    
    self.calc_saturation_pt()
    self.calc_critical_pt()
    
  def get_motive(self):
    """
    Returns value of motive for given value(s) of position.
    
    Position must be of numerical type or numpy array. Returns NaN if position 
    falls outside of the interelectrode space.
    """
    pass
  
  def get_max_motive(self, with_position=False):
    """
    Returns value of the maximum motive relative to emitter Fermi energy in eV.
    
    If with_position is True, return a tuple where the first element is the 
    maximum motive value and the second element is the corresponding position.
    """
    pass
  
  def calc_saturation_pt(self):
    """
    Calculate saturation point condition and populate motive_data.
    """    
    # For brevity, "dimensionless" prefix omitted from "position" and "motive" variable names.
    output_current_density = self["Emitter"].calc_saturation_current()
    
    position = self.calc_interelectrode_spacing() * \
      ((2 * np.pi * physical_constants["electron_mass"] * physical_constants["electron_charge"]**2) / \
      (physical_constants["permittivity0"]**2 * physical_constants["boltzmann"]**3))**(1.0/4) * \
      (output_current_density**(1.0/2))/(self["Emitter"]["temp"]**(3.0/4))
      
    motive = self["motive_data"]["dps"].get_motive(position)
    
    output_voltage = (self["Emitter"]["barrier_ht"] - \
      self["Collector"]["barrier_ht"] - \
      motive * physical_constants["boltzmann"] * self["Emitter"]["temp"]) / \
      physical_constants["electron_charge"]
    
    # Populate motive_data.
    self["motive_data"]["saturation_pt"] = \
      {"output_voltage":output_voltage,
       "output_current_density":output_current_density}
  
  def calc_critical_pt(self):
    """
    Calculate critical point condition and populate motive_data.
    """
    # For brevity, "dimensionless" prefix omitted from "position" and "motive" variable names.
    
    # Rootfinder to get critical point output current density.
    output_current_density = 1.0
    
    position = -self.calc_interelectrode_spacing() * \
      ((2 * np.pi * physical_constants["electron_mass"] * physical_constants["electron_charge"]**2) / \
      (physical_constants["permittivity0"]**2 * physical_constants["boltzmann"]**3))**(1.0/4) * \
      (output_current_density**(1.0/2))/(self["Emitter"]["temp"]**(3.0/4))
      
    motive = np.log(self["Emitter"].calc_saturation_current()/output_current_density)
    
    output_voltage = (self["Emitter"]["barrier_ht"] - \
      self["Collector"]["barrier_ht"] + \
      motive * physical_constants["boltzmann"] * self["Emitter"]["temp"]) / \
      physical_constants["electron_charge"]
    
    # Populate motive_data.
    self["motive_data"]["critical_pt"] = \
      {"output_voltage":output_voltage,
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
    
    return position - self["dps"].get_position(motive)

  def output_voltage_target_function(self,output_current_density):
    """
    Target function for the output voltage rootfinder.
    """
    # For brevity, "dimensionless" prefix omitted from "position" and "motive" variable names.
    em_motive = np.log(self["Emitter"].calc_saturation_current/output_current_density)
    em_position = self["motive_data"]["dps"].get_position(em_motive)
    
    # NOTE: I haven't yet defined x0. Probably it will end up as a helper method.
    co_position = self.calc_interelectrode_spacing()/x0 + em_position
    co_motive = self["motive_data"]["dps"].get_motive(co_position)
    
    return ((self["Emitter"]["barrier_ht"] + \
      em_motive * physical_constants["boltzmann"] * self["Emitter"]["temperature"]) - \
      (self["Collector"]["barrier_ht"] + \
      co_motive * physical_constants["boltzmann"] * self["Emitter"]["temperature"]))/ \
      physical_constants["electron_charge"]