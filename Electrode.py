import math
from tec import Constants

class Electrode(dict):
  
  """
  Implementation of thermionic electrode.
  
  An Electrode object is instantiated by a dict which defines the Electrode's 
  data. The values of this dict must obey certain constraints and are given in 
  TEC units (see below). There are no default values for instantiation. 
  
  Data with constraints and units:
    temperature   >  0 [K]
    barrierHeight >= 0 [eV]
    voltage            [V]
    position           [\mu m]
    richardson    >= 0 [A cm^{-2} K^{-2}]
    emissivity    < 1 & > 0
    
  Internally, the class deals with the data in SI units.
  """
  
  def __init__(self,inputParams):
    """
    Instantiation of Electrode object.
    """
    
    # is inputParams a dict?
    if inputParams.__class__ is not dict:
      raise TypeError("Inputs must be of type dict.")
    
    # Does inputParams have the correct fields? Compare the keys of 
    # inputParams to a list of the correct field names.
    correctFields = ["temperature","barrierHeight","voltage","position",\
      "richardson","emissivity"]
    
    inputParamKeys = inputParams.keys()
    if correctFields.sort() != inputParamKeys.sort():
      raise KeyError("Input dictionary missing a key.")
    
    # Does inputParams have superflous keys? (warning)
    # ADD CODE
    
    # Try to set the object's attributes:
    self["temperature"] = inputParams["temperature"]
    self["barrierHeight"] = inputParams["barrierHeight"]
    self["voltage"] = inputParams["voltage"]
    self["position"] = inputParams["position"]
    self["richardson"] = inputParams["richardson"]
    self["emissivity"] = inputParams["emissivity"]

  
  def __setitem__(self,key,item):
    """
    Sets attribute values according to constraints.
    """

    # Check to see if the argument is numeric.
    try:
      item = float(item)
    except ValueError:
      raise TypeError("Argument must be of real numeric type.")
    
    ## Check to see if the name of the key is valid: (error)
    #if key is not ("temperature" or "barrierHeight" or "voltage" or \
      #"position" or "richardson" or "emissivity"):
      #raise KeyError("Superflous key.")
    
    # Check to see if constraints are met.
    if key == "temperature" and item <= 0:
      raise ValueError("temperature must be positive.")
    if key == "barrierHeight" and item < 0:
      raise ValueError("barrierHeight must be non-negative.")
    if key == "richardson" and item < 0:
      raise ValueError("richardson must be non-negative.")
    if key == "emissivity" and not (0 < item < 1):
      raise ValueError("emissivity must be between 0 and 1.")
    
    # Convert the pertinant values to SI:
    if key is "barrierHeight":
      item = 1.60217646e-19 * item
    if key is "position":
      item = 1e-6 * item
    if key is "richardson":
      item = 1e4 * item
      
    # Set value.
    dict.__setitem__(self,key,item)
  
  # Methods
  def calcsaturationcurrent(self):
    """
    Return value of the saturation current in A m^{-2}.
  
    Calculates the output current density according to the Richardson-Dushman
    equation using the values of the Electrode object. This method requires no
    arguments.
    """
    saturationCurrent = self["richardson"] * math.pow(self["temperature"],2) * \
    math.exp(-self["barrierHeight"]/(Constants.boltzmann * self["temperature"]))
    
    return saturationCurrent
    