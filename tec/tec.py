# -*- coding: utf-8 -*-

from tec import Electrode
from tec import physical_constants
import math
import numpy as np
from scipy import optimize

class TEC(dict):
  
  """
  Parent class for TEC objects: template for TEC functionality.
  
  This class is meant to be a template for particular implementations of TEC
  models and as such it should only be subclassed, not instantiated directly. 
  The TEC class has two attributes, both of type Electrode: Emitter and 
  Collector. A TEC object is instantiated with a dict with two fields: "Emitter"
  and "Collector". Each must contain a dict suitable for instantiating an 
  Electrode object. The TEC class has no default values for instantiation.
  
  See the individual methods for details. Methods returning values show the
  units of the returned quantity in brackets: [].
  """
  
  def __init__(self,input_params):
    # is input_params a dict?
    if input_params.__class__ is dict:
      raise TypeError("Inputs must be of type dict.")

    # Ensure that the required fields are present in input_params.
    req_fields = ["Emitter","Collector"]
    input_param_keys = set(input_params.keys())
    
    if not set(req_fields).issubset(input_param_keys):
      raise KeyError("Input dict is missing one or more keys.")
    
    # Try to set the object's attributes:
    for key in req_fields:
      self[key] = input_params[key]
  
  def __setitem__(self,key,item):
    """
    Sets attribute values according to Electrode constraints.
    """
    # Try to turn the argument into an Electrode. The Electrode class has a lot
    # of error checking and if the argument can't make it through that checking,
    # its not worth proceeding.
    ElecItem = Electrode(item)
    
    # Set value.
    dict.__setitem__(self,key,ElecItem)
    
  # Methods ==================================================================
  def calc_interelectrode_spacing(self):
    """
    Return distance between Collector and Emitter [um].
    """
    return self["Collector"]["position"] - self["Emitter"]["position"]
  
  def calc_output_voltage(self):
    """
    Return potential difference between Emitter and Collector [V].
    """
    return self["Collector"]["voltage"] - self["Emitter"]["voltage"]
  
  def calc_contact_potential(self):
    """
    Return contact potential [V].
    
    The contact potential is defined as the difference in barrier height between
    the emitter and collector. This value should not be confused with the output
    voltage which is the voltage difference between the collector and emitter.
    """
    return (self["Emitter"]["barrier_ht"] - \
      self["Collector"]["barrier_ht"])/physical_constants["electron_charge"]
    
  def calc_forward_current_density(self):
    """
    Return forward current density [A cm^{-2}].
    """
    
    if self["Emitter"]["barrier_ht"] < self.calc_max_motive_height():
      return self["Emitter"].calc_saturation_current() * \
        math.exp(-(self.calc_max_motive_height()-self["Emitter"]["barrier_ht"])/\
          (physical_constants["boltzmann"] * self["Emitter"]["temp"]))
    else:
      return self["Emitter"].calc_saturation_current()
  
  def calc_back_current_density(self):
    """
    Return back current density [A cm^{-2}].
    """
    
    if self["Collector"]["barrier_ht"] < self.calc_max_motive_height():
      return self["Collector"].calc_saturation_current() * \
        math.exp(-(self.calc_max_motive_height()-self["Collector"]["barrier_ht"]-self.calc_output_voltage())/ \
          (physical_constants["boltzmann"] * self["Collector"]["temp"]))
    else:
      return self["Collector"].calc_saturation_current()
  
  def calc_output_current_density(self):
    """
    Return output current density: diff. between forward and back current [A cm^{-2}].
    """
    return self.calc_forward_current_density() - self.calc_back_current_density()
  
  def calc_output_power_density(self):
    """
    Return output power density [W cm^{-2}].
    """
    return self.calc_output_current_density() * self.calc_output_voltage()
  
  # This method needs work: voltage/current density is not resistance
  def calc_load_resistance(self):
    """
    Return load resistance [Ohms].
    """
    # There is something fishy about the units in this calculation.
    if self.calc_output_current_density() != 0:
      return self.calc_output_voltage() / self.calc_output_current_density()
    else:
      return np.nan
  
  # Methods regarding motive --------------------------------------------------
  def calc_motive(self, arrayLength = 100):
    """
    Return the motive vs. position as a dict.
    
    The returned dict has two fields, "motive" and "position". Each field
    contains a 1D numpy array of length defined by the int input argument
    arrayLength. The default value for arrayLength is 100.
    """
    return {"position": np.ones(arrayLength) ,\
            "motive": np.ones(arrayLength)}
  
  def calc_max_motive_height(self):
    """
    Returns the value of the maximum motive height in [eV]. 
    
    This value should not be confused with the maximum motive given in 
    "Thermionic Energy Conversion Vol. 1" by Hatsopoulos and Gyftopoulos as 
    \psi_{m}. The value returned by this method is equivalent to 
    \psi_{m} - \mu_{E}.
    """
    motive = self.calc_motive()
    return float(motive["motive"].max())
  
  #def calc_position_at_max_motive(self):
    #"""
    #Position at which the max. motive occurs [um]
    #"""
    #motive = self.calc_motive()
    #indx = motive[:,1].argmax()
    #return float(motive[indx,0])
  
  
  # Methods regarding efficiency ----------------------------------------------
  def calc_carnot_efficiency(self):
    """
    Return value of carnot efficiency in the range 0 to 1.
    
    This method will return a negative value if the emitter temperature is less
    than the collector temperature.
    """
    return 1 - (self["Collector"]["temp"]/self["Emitter"]["temp"])
  
  def calc_radiation_efficiency(self):
    """
    Return efficiency of device considering only blackbody heat transport.
    
    The output will be between 0 and 1. If the output power is less than zero,
    return nan.
    """
    if self.calc_output_power_density() > 0:
      return self.calc_output_power_density() / self.__calc_black_body_heat_transport()
    else:
      return np.nan
  
  def calc_electronic_efficiency(self):
    """
    Return efficiency of device considering only electronic heat transport.
    
    The output will be between 0 and 1. If the output power is less than zero,
    return nan.

    See "Thermionic Energy Conversion Vol. I" by Hatsopoulous and Gyftopoulous
    pp 73 for a description of the electronic efficiency.
    """
    if self.calc_output_power_density() > 0:
      return self.calc_output_power_density() / self.__calc_electronic_heat_transport()
    else:
      return np.nan
  
  def calc_total_efficiency(self):
    """
    Return total efficiency considering all heat transport mechanisms.
    
    The output will be between 0 and 1. If the output power is less than zero,
    return nan.
    """
    if self.calc_output_power_density() > 0:
      return self.calc_output_power_density() / \
        (self.__calc_black_body_heat_transport() + self.__calc_electronic_heat_transport())
    else:
      return np.nan

  def __calc_electronic_heat_transport(self):
    """
    Returns the electronic heat transport of a TEC object.
    
    A description of electronic losses can be found on page 69 (eq. 2.57a) of
    "Thermionic Energy Conversion Vol. 1" by Hatsopoulous and Gyftopoulous.
    """
    elecHeatTransportForward = self.calc_forward_current_density()*(self.calc_max_motive_height()+\
      2 * physical_constants["boltzmann"] * self["Emitter"]["temp"]) / \
      Constants.electronCharge
    elecHeatTransportBackward = self.calc_back_current_density()*(self.calc_max_motive_height()+\
      2 * physical_constants["boltzmann"] * self["Collector"]["temp"]) / \
      Constants.electronCharge
    return elecHeatTransportForward - elecHeatTransportBackward
  
  def __calc_black_body_heat_transport(self):
    """
    Returns the radiation transport of a TEC object.
    """
    return Constants.sigma0 * \
      (self["Emitter"]["emissivity"] * pow(self["Emitter"]["temp"],4) - \
      self["Collector"]["emissivity"] * pow(self["Collector"]["temp"],4))
    
