# -*- coding: utf-8 -*-

import math
import Constants

class Electrode(dict):
  
  """
  Thermionic electrode.
  
  An Electrode object is instantiated by a dict which defines the Electrode's 
  data. The dict which instantiates an Electrode must have the keys listed 
  below which adhere to the noted constraints. Additional keys will be 
  ignored, and there are no default values for instantiation. When setting 
  Electrode data, values are assumed to be TEC units.
  
  Data with constraints and units:
    temp       >  0 [K]
    barrier_ht >= 0 [eV]
    voltage         [V]
    position        [\mu m]
    richardson >= 0 [A cm^{-2} K^{-2}]
    emissivity < 1 & > 0
    nea        >= 0 [eV] (optional)
    
  Internally, the class deals with the data in SI units.
  """
  
  def __init__(self,input_params):
    """
    Instantiation of Electrode object.
    """
    
    # Is input_params a dict?
    if input_params.__class__ is not dict:
      raise TypeError("Inputs must be of type dict.")
    
    # Does input_params have the correct fields?
    correct_fields = ["temp","barrier_ht","voltage","position",\
      "richardson","emissivity"]
    input_param_keys = set(input_params.keys())
    
    if not set(correct_fields).issubset(input_param_keys):
      raise KeyError("Input dictionary missing a key.")
    
    if "nea" in input_param_keys:
      correct_fields.append("nea")

    # Try to set the object's attributes:
    for key in correct_fields:
      self[key] = input_params[key]

  
  def __setitem__(self,key,item):
    """
    Sets attribute values according to constraints.
    """

    # Check to see if the argument is numeric.
    try:
      item = float(item)
    except ValueError:
      raise TypeError("Argument must be of real numeric type.")
    
    # Check to see if constraints are met.
    if key == "temp" and item <= 0:
      raise ValueError("temp must be positive.")
    if key == "barrier_ht" and item < 0:
      raise ValueError("barrier_ht must be non-negative.")
    if key == "richardson" and item < 0:
      raise ValueError("richardson must be non-negative.")
    if key == "emissivity" and not (0 < item < 1):
      raise ValueError("emissivity must be between 0 and 1.")
    if key == "nea" and item < 0:
      raise ValueError("nea must be non-negative.")
    
    # Convert the pertinant values to SI:
    if key is "barrier_ht":
      item = 1.60217646e-19 * item
    if key is "nea":
      item = 1.60217646e-19 * item
    if key is "position":
      item = 1e-6 * item
    if key is "richardson":
      item = 1e4 * item
      
    # Set value.
    dict.__setitem__(self,key,item)
  
  # Methods
  def calc_saturation_current(self):
    """
    Return value of the saturation current in A m^{-2}.
  
    Calculates the output current density according to the Richardson-Dushman
    equation using the values of the Electrode object.
    """
    saturation_current = self["richardson"] * math.pow(self["temp"],2) * \
    math.exp(-self["barrier_ht"]/(physical_constants["boltzmann"] * self["temp"]))
    
    return saturation_current

  def calc_vacuum_energy(self):
    """
    Position of the vacuum energy relative to the arbitrary voltage ground.
    
    Note that this method is used to determine the electrostatic boundary 
    condition in order to calculate the solution to Poisson's equation. 
    The quantities are scaled appropriately for proper dimensionality.
    """
    
    if "nea" in self.keys():
      vacuum_energy = physical_constants["electron_charge"] * self["voltage"] + \
        self["barrier_ht"] + self["nea"]
    else:
      vacuum_energy = physical_constants["electron_charge"] * self["voltage"] + \
        self["barrier_ht"]
      
    return vacuum_energy
      