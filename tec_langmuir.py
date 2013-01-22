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
    output_current_density = 0.0
    
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
       
  def calc_motive(self):
    """
    Calculate the motive parameters.
    
    I'm not really sure where this method is going to go or if it will keep this name, but I know I will need all this code somewhere.
    """
    # For brevity, "dimensionless" prefix omitted from "position" and "motive" variable names.
    
    # Rootfinder to get output current density corresponding to output voltage.
    output_current_density = 0.0
    
    em_motive = np.log(self["Emitter"].calc_output_current()/output_current_density)
    
    # NOTE: At this point I pretty much have what I need. I can get the other dimensionless parameters simply by knowing the value of output current. I can get the emitter and collector dimensionless motives and positions.
  
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