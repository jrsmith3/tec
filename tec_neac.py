# -*- coding: utf-8 -*-

from electrode import Electrode
from constants import physical_constants
from dimensionlesslangmuirpoissonsoln import DimensionlessLangmuirPoissonSoln
from tec_langmuir import TEC_Langmuir
import numpy as np
from scipy import interpolate,optimize

class TEC_NEAC(TEC_Langmuir):
  """
  Thermionic engine simulator. Considers space charge and collector NEA.

  dict-like object that implements a model of electron transport including the negative space charge effect. This class considers the possibility the collector features NEA, but assumes the emitter has PEA. The model is based on [1].

  Attributes
  ----------
  The attributes of the object are accessed like a dictionary. The object has three attributes; "Emitter" and "Collector" are both Electrode objects. "motive_data" is a dictionary containing (meta)data calculated during the motive calculation. "motive_data" should usually be accessed via the class's convenience methods. "motive_data" contains the following data:

    saturation_pt: Dict containing saturation point data described below.
    
      output_voltage:         Voltage at which the saturation point occurs.
      
      output_current_density: Current at which the saturation point occurs.
    
    virt_critical_pt:   Dict containing virtual critical point data described below.

    
      output_voltage:         Voltage at which the critical point occurs.
      
      output_current_density: Current at which the critical point occurs.
      
    dps:           Langmuir's dimensionless Poisson's equation solution object.

    spclmbs_max_dist: Space charge limited mode boundary surface maximum distance: distance below which the TEC experiences no space charge limited mode. [m]
      
  Parameters
  ----------
  The TEC_Langmuir class is instantiated by a dict with two keys, "Emitter" and "Collector" (case insensitive). Both keys have data that is also of type dict which are configured to instantiate an Electrode object. Additional keys will be ignored and there are no default values for instantiation.

  Examples and interface testing
  ------------------------------
  >>> from tec_neac import TEC_NEAC
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
  ...            "emissivity":0.5,
  ...            "nea":0.2,}
  >>> input_dict = {"Emitter":em_dict, "Collector":co_dict}
  >>> example_tec = TEC_NEAC(input_dict)
  
  Make sure that the motive_data interface matches the above description.
  
  >>> isinstance(example_tec["motive_data"]["saturation_pt"]["output_voltage"],float)
  True
  >>> isinstance(example_tec["motive_data"]["saturation_pt"]["output_current_density"],float)
  True
  >>> isinstance(example_tec["motive_data"]["virt_critical_pt"]["output_voltage"],float)
  True
  >>> isinstance(example_tec["motive_data"]["virt_critical_pt"]["output_current_density"],float)
  True
  >>> isinstance(example_tec["motive_data"]["spclmbs_max_dist"],float)
  True
  >>> type(example_tec["motive_data"]["dps"])
  <class 'tec.dimensionlesslangmuirpoissonsoln.DimensionlessLangmuirPoissonSoln'>

  Notes
  -----

  Bibliography
  ------------
  [1] JRS, work in progress.
  """
  
  def calc_motive(self):
    """
    Calculate the motive parameters and populate "motive_data".
    """
    # For brevity, "dimensionless" prefix omitted from "position" and "motive" variable names.
    
    self["motive_data"] = {}
    self["motive_data"]["dps"] = DimensionlessLangmuirPoissonSoln()

    self["motive_data"]["spclmbs_max_dist"] = self.calc_spclmbs_max_dist()
    self["motive_data"]["saturation_pt"] = self.calc_saturation_pt()
    self["motive_data"]["virt_critical_pt"] = self.calc_virt_critical_pt()

    if self.calc_output_voltage() < self["motive_data"]["saturation_pt"]["output_voltage"]:
      # Accelerating mode.
      self["motive_data"]["max_motive_ht"] = self["Emitter"].calc_barrier_ht()
    elif self.calc_output_voltage() > self["motive_data"]["virt_critical_pt"]["output_voltage"]:
      # Retarding mode.
      self["motive_data"]["max_motive_ht"] = self["Collector"].calc_barrier_ht()
    else:
      # Space charge limited mode.
      output_current_density = optimize.brentq(self.output_voltage_target_function,\
        self["motive_data"]["saturation_pt"]["output_current_density"],\
        self["motive_data"]["virt_critical_pt"]["output_current_density"])
        
      barrier = physical_constants["boltzmann"] * self["Emitter"]["temp"] * \
        np.log(self["Emitter"].calc_saturation_current()/output_current_density)
      self["motive_data"]["max_motive_ht"] = barrier + self["Emitter"].calc_barrier_ht()
      
  def calc_spclmbs_max_dist(self):
    """
    Calculate space charge limited mode boundary surface maximum interelectrode distance.
    """
    # For brevity, "dimensionless" prefix omitted from "position" and "motive" variable names.
    # I am using the suffix "vr" to denote "Virtual cRitical point."
    co_motive_vr = self["Collector"]["nea"]/ \
      (physical_constants["boltzmann"] * self["Emitter"]["temp"])
    co_position_vr = self["motive_data"]["dps"].get_position(co_motive_vr,branch="rhs")
    
    spclbs_max_dist = (co_position_vr * self["Emitter"]["temp"]**(3./4)) / \
      (self["Emitter"].calc_saturation_current()**(1./2)) * \
      ((physical_constants["permittivity0"]**2 * physical_constants["boltzmann"]**3)/ \
      (2*np.pi*physical_constants["electron_mass"]*physical_constants["electron_charge"]**2))**(1./4)
      
    return spclbs_max_dist
    
    
  def calc_saturation_pt(self):
    """
    Calculate and return saturation point condition.
    
    Returns dict with keys output_voltage and output_current_density with values in [V] and [A m^-2], respectively.
    """    
    # For brevity, "dimensionless" prefix omitted from "position" and "motive" variable names.
    # If the device is operating within the space charge limited mode boundary surface, we can immediately set the values and exit.
    if self.calc_interelectrode_spacing() <= self["motive_data"]["spclmbs_max_dist"]:
      return {"output_voltage":self.calc_contact_potential(),
              "output_current_density":self["Emitter"].calc_saturation_current()}
    
    output_current_density = self["Emitter"].calc_saturation_current()
    
    position = self.calc_interelectrode_spacing() * \
      ((2 * np.pi * physical_constants["electron_mass"] * physical_constants["electron_charge"]**2) / \
      (physical_constants["permittivity0"]**2 * physical_constants["boltzmann"]**3))**(1.0/4) * \
      (output_current_density**(1.0/2))/(self["Emitter"]["temp"]**(3.0/4))
      
    motive = self["motive_data"]["dps"].get_motive(position)
    
    output_voltage = (self["Emitter"]["barrier"] + self["Collector"]["nea"] - \
      self["Collector"]["barrier"] - \
      motive * physical_constants["boltzmann"] * self["Emitter"]["temp"]) / \
      physical_constants["electron_charge"]
    
    return {"output_voltage":output_voltage,
            "output_current_density":output_current_density}
  
  def calc_virt_critical_pt(self):
    """
    Calculate and return virtual critical point condition.
    
    Returns dict with keys output_voltage and output_current_density with values in [V] and [A m^-2], respectively.
    """
    # For brevity, "dimensionless" prefix omitted from "position" and "motive" variable names.
    # If the device is operating within the space charge limited mode boundary surface, we can immediately set the values and exit.
    if self.calc_interelectrode_spacing() <= self["motive_data"]["spclmbs_max_dist"]:
      return {"output_voltage":self.calc_contact_potential(),
              "output_current_density":self["Emitter"].calc_saturation_current()}
    
    output_current_density = optimize.brentq(self.virt_critical_point_target_function,\
      self["Emitter"].calc_saturation_current(),0)
    
    motive = np.log(self["Emitter"].calc_saturation_current()/output_current_density)
    output_voltage = self["Emitter"]["barrier"] - self["Collector"]["barrier"] + \
      physical_constants["boltzmann"] * self["Emitter"]["temp"] * motive
    
    return {"output_voltage":output_voltage,
            "output_current_density":output_current_density}

  def virt_critical_point_target_function(self,output_current_density):
    """
    Target function for virtual critical point rootfinder.
    """
    # For brevity, "dimensionless" prefix omitted from "position" and "motive" variable names. Since this method is only about the virtual critical point, I don't use any suffix.
    co_motive = self["Collector"]["nea"]/ \
      (physical_constants["boltzmann"] * self["Emitter"]["temp"])
    co_position = self["motive_data"]["dps"].get_position(co_motive,branch="rhs")
    
    if output_current_density == 0:
      em_motive = np.inf
    else:
      em_motive = np.log(self["Emitter"].calc_saturation_current()/output_current_density)
    
    em_position = self["motive_data"]["dps"].get_position(em_motive)
    
    # offset is the dimensionless distance term which, along with the emitter and collector dimensionless distance, sums to zero.
    offset = self.calc_interelectrode_spacing() * \
      ((2 * np.pi * physical_constants["electron_mass"] * physical_constants["electron_charge"]**2) / \
      (physical_constants["permittivity0"]**2 * physical_constants["boltzmann"]**3))**(1.0/4) * \
      (output_current_density**(1.0/2))/(self["Emitter"]["temp"]**(3.0/4))
      
    return co_position - (em_position + offset)

  def output_voltage_target_function(self,output_current_density):
    """
    Target function for the output voltage rootfinder.
    """
    # For brevity, "dimensionless" prefix omitted from "position" and "motive" variable names.
    em_motive = np.log(self["Emitter"].calc_saturation_current()/output_current_density)
    em_position = self["motive_data"]["dps"].get_position(em_motive)
    
    offset = self.calc_interelectrode_spacing() * \
      ((2 * np.pi * physical_constants["electron_mass"] * physical_constants["electron_charge"]**2) / \
      (physical_constants["permittivity0"]**2 * physical_constants["boltzmann"]**3))**(1.0/4) * \
      (output_current_density**(1.0/2))/(self["Emitter"]["temp"]**(3.0/4))

    co_position = em_position + offset
    co_motive = self["motive_data"]["dps"].get_motive(co_position)
    
    return self.calc_output_voltage() - ((self["Emitter"]["barrier"] + \
      em_motive * physical_constants["boltzmann"] * self["Emitter"]["temp"]) - \
      (self["Collector"]["barrier"] - self["Collector"]["nea"] + \
      co_motive * physical_constants["boltzmann"] * self["Emitter"]["temp"]))/ \
      physical_constants["electron_charge"]
