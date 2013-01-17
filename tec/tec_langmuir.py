# -*- coding: utf-8 -*-

from electrode import Electrode
from constants import physical_constants
import math
import numpy as np
from scipy import interpolate
from tec import TEC

class TEC_Langmuir(TEC):
  """
  Implementation of Langmuir's TEC model.
  """
  
  def calc_back_current_density(self):
    """
    Return back current density in A m^{-2}.
    """
    return 0.0
    
  def calc_saturation_point(self):
    """
    Calculate saturation point condition and populate motive_data.
    """    
    # For brevity, "dimensionless" prefix omitted from "position" and "motive" variable names.
    output_current_density = self["Emitter"].calc_output_current()
    
    position = self.calc_interelectrode_spacing() * \
      ((2 * np.pi * physical_constants["electron_mass"] * physical_constants["electron_charge"]**2) / \
      (physical_constants["epsilon_0"]**2 * physical_constants["boltzmann"]**3))**(1.0/4) * \
      (output_current_density**(1.0/2))/(self["Emitter"]["temp"]**(3.0/4))
      
    motive = self["motive_data"]["dps"].get_motive(position)
    
    output_voltage = (self["Emitter"]["barrier_ht"] - \
      self["Collector"]["barrier_ht"] - \
      motive * physical_constants["boltzmann"] * self["Emitter"]["temp"]) / \
      physical_constants["electron_charge"]
    
    # Populate motive_data.
    self["motive_data"]["saturation_point"] = \
      {"dimenisonless_position":position,
       "dimensionless_motive":motive,
       "output_voltage":output_voltage,
       "output_current_density":output_current_density}
  
  def calc_critical_point(self):
    """
    Calculate critical point condition and populate motive_data.
    """
    # For brevity, "dimensionless" prefix omitted from "position" and "motive" variable names.
    
    # Rootfinder to get critical point output current density.
    output_current_density = 0
    
    position = -self.calc_interelectrode_spacing() * \
      ((2 * np.pi * physical_constants["electron_mass"] * physical_constants["electron_charge"]**2) / \
      (physical_constants["epsilon_0"]**2 * physical_constants["boltzmann"]**3))**(1.0/4) * \
      (output_current_density**(1.0/2))/(self["Emitter"]["temp"]**(3.0/4))
      
    motive = np.log(self["Emitter"].calc_output_current()/output_current_density)
    
    output_voltage = (self["Emitter"]["barrier_ht"] - \
      self["Collector"]["barrier_ht"] + \
      motive * physical_constants["boltzmann"] * self["Emitter"]["temp"]) / \
      physical_constants["electron_charge"]
    
    # Populate motive_data.
    self["motive_data"]["saturation_point"] = \
      {"dimenisonless_position":position,
       "dimensionless_motive":motive,
       "output_voltage":output_voltage,
       "output_current_density":output_current_density}
  
  def critical_point_target_function(self,output_current_density):
    """
    Target function for critical point rootfinder.
    """
    position = -self.calc_interelectrode_spacing() * \
      ((2 * np.pi * physical_constants["electron_mass"] * physical_constants["electron_charge"]**2) / \
      (physical_constants["epsilon_0"]**2 * physical_constants["boltzmann"]**3))**(1.0/4) * \
      (output_current_density**(1.0/2))/(self["Emitter"]["temp"]**(3.0/4))
      
    if output_current_density == 0:
      motive = np.inf
    else:
      motive = np.log(self["Emitter"].calc_output_current()/output_current_density)
    
    return position - self["dps"].get_position(motive)

