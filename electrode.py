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
    
  for barrier is understood to be
  
    1.40000000000000
  
  Keys for instantiating dict:
    Key        Constraint Unit             Description
    ---        ---------- ----             -----------
    temp       >  0       K
    
    barrier >= 0          eV               Sometimes referred to as work 
                                           function. In the case of a metal and 
                                           a positive electron affinity 
                                           semiconductor, the barrier height is 
                                           the difference between the vacuum 
                                           energy and the Fermi level. In the 
                                           case of a negative electron affinity 
                                           semiconductor, the barrier is the 
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
  ...                 "barrier":1,
  ...                 "voltage":0,
  ...                 "position":0,
  ...                 "richardson":10,
  ...                 "emissivity":0.5}
  >>> El = Electrode(input_params)
  >>> El
  {'barrier': 1.6021764600000001e-19,
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
    req_fields = ["temp","barrier","voltage","position","richardson",\
      "emissivity"]
    input_param_keys = set(input_params.keys())
    
    if not set(req_fields).issubset(input_param_keys):
      missing_keys = set(req_fields) - input_param_keys
      raise KeyError("Input dict is missing the following keys:" + \
      str(list(missing_keys)))
    
    if "nea" in input_param_keys:
      req_fields.append("nea")

    # Try to set the object's attributes:
    for key in req_fields:
      self[key] = input_params[key]
      
    self.__param_changed = False

  
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
    if key == "barrier" and item < 0:
      raise ValueError("barrier must be non-negative.")
    if key == "richardson" and item < 0:
      raise ValueError("richardson must be non-negative.")
    if key == "emissivity" and not (0 < item < 1):
      raise ValueError("emissivity must be between 0 and 1.")
    if key == "nea" and item < 0:
      raise ValueError("nea must be non-negative.")
    
    # Convert the pertinant values to SI:
    if key is "barrier":
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
      
    # Check to see if the Electrode already has the attribute set. If so, add the flag.
    if key in ["temp","richardson","barrier","voltage","position","nea"]:
      if key in self.keys():
        self.__param_changed = True
      
    # Set value.
    dict.__setitem__(self,key,item)
    
  def param_changed_and_reset(self):
    """
    Return True, reset to False if a parameter affecting motive has just been changed.

    Parameters which affect motive are temp, barrier, voltage, position, richardson, and nea.
    """
    if self.__param_changed:
      self.__param_changed = False
      return True
    else:
      return False
  
  # Methods
  def calc_saturation_current(self):
    """
    Return value of the saturation current in A m^{-2}.
  
    Calculates the output current density according to the Richardson-Dushman
    equation. If either temp or barrier are equal to 0, this  method returns
    a value of 0.
    """
    if self["temp"] == 0:
      saturation_current = 0
    else:
      saturation_current = self["richardson"] * math.pow(self["temp"],2) * \
      math.exp(-self["barrier"]/(physical_constants["boltzmann"] * self["temp"]))
    
    return saturation_current

  def calc_vacuum_energy(self):
    """
    Position of the vacuum energy relative to fermi energy in J.
    
    If the Electrode does not have NEA, the vacuum energy occurs at the top of 
    the barrier and is therefore equal to the barrier. If the Electrode does 
    have NEA, the vacuum level is the barrier reduced by the value of the NEA.
    """
    
    if "nea" in self.keys():
      return self["barrier"] - self["nea"]
    else:
      return self["barrier"]
      
  def calc_barrier_ht(self):
    """
    Returns value of barrier height relative to ground in J.
    """
    return self["barrier"] + physical_constants["electron_charge"] * self["voltage"]
      
  def calc_motive_bc(self):
    """
    Returns the motive boundary condition in J. 
    
    It is worth remembering the boundary condition is relative to ground.
    """
    return self.calc_vacuum_energy() + \
      physical_constants["electron_charge"] * self["voltage"]
    