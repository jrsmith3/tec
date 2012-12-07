# -*- coding: utf-8 -*-

import math
from constants import physical_constants

__author__ = "Joshua Ryan Smith (joshua.r.smith@gmail.com)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2012 Joshua Ryan Smith"
__license__ = ""

class Electrode(dict):
  
  """
  Thermionic electrode.
  
  An Electrode object is instantiated by a dict. The dict must have the keys 
  listed below which adhere to the noted constraints and units (what I'm calling 
  "TEC units"). Additional keys will be ignored, and there are no default values 
  for instantiation. 
  
  The user can set either temp or richardson equal to zero to "switch off" the 
  electrode -- the calc_saturation_current method will return a value of zero in 
  either case. See the docstring of that method for more info.
  
  It is assumed that all input parameters are to machine precision despite the 
  explicit number of significant figures defined by the user. For example, if 
  the machine has fifteen digits of precision, an explicit value of
  
    1.4
    
  for barrier_ht is understood to be
  
    1.40000000000000
  
  Keys for instantiating dict:
    Key        Constraint Unit             Description
    ---        ---------- ----             -----------
    temp       >  0       K
    
    barrier_ht >= 0       eV               Sometimes referred to as work 
                                           function. In the case of a metal and 
                                           a positive electron affinity 
                                           semiconductor, the barrier height is 
                                           the difference between the vacuum 
                                           energy and the Fermi level. In the 
                                           case of a negative electron affinity 
                                           semiconductor, the barrier_ht is the 
                                           difference between the conduction 
                                           band minimum and Fermi level.
                                           
    voltage               V                Explicitly sets the bias of the 
                                           electrode with respect to ground. 
                                           Disambiguates the potential between 
                                           the Emitter and Collector in a TEC 
                                           object.
                                           
    position              \mu m            Explicitly sets the position of the 
                                           electrode. Disambiguates the relative 
                                           positions of the Emitter and 
                                           Collector in a TEC object.
                                           
    richardson >= 0       A cm^{-2} K^{-2} 
    
    emissivity < 1 & > 0  
    
    nea        >= 0       eV               Optional. In some semiconductors, the 
                                           vacuum level falls below the 
                                           conduction band minimum. An increase 
                                           in this value implies the vacuum 
                                           level moves ever lower from the 
                                           conduction band minimum.
                                           
    Here's an example.
    >>> input_params = {"temp":1000,
    ...                 "barrier_ht":1,
    ...                 "voltage":0,
    ...                 "position":0,
    ...                 "richardson":10,
    ...                 "emissivity":0.5}
    >>> El = Electrode(input_params)
    >>> El
    {'barrier_ht': 1.6021764600000001e-19,
     'emissivity': 0.5,
     'position': 0.0,
     'richardson': 100000.0,
     'temp': 1000.0,
     'voltage': 0.0}
  """
  
  def __init__(self,input_params):
    # Ensure input_params is of type dict.
    if input_params.__class__ is not dict:
      raise TypeError("Inputs must be of type dict.")
    
    # Ensure that the minimum required fields are present in input_params.
    req_fields = ["temp","barrier_ht","voltage","position","richardson",\
      "emissivity"]
    input_param_keys = set(input_params.keys())
    
    if not set(req_fields).issubset(input_param_keys):
      raise KeyError("Input dict is missing one or more keys.")
    
    if "nea" in input_param_keys:
      req_fields.append("nea")

    # Try to set the object's attributes:
    for key in req_fields:
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
    if key == "temp" and item < 0:
      raise ValueError("temp must be greater than or equal to zero.")
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
      # Update to J
      item = 1.60217646e-19 * item
    if key is "nea":
      # Update to J
      item = 1.60217646e-19 * item
    if key is "position":
      # Update to m
      item = 1e-6 * item
    if key is "richardson":
      # Update to A m^{-2} K^{-2}
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
    if self["temp"] == 0:
      saturation_current = 0
    else:
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
      