#!/usr/bin/python

from Electrode import Electrode

class NEAElectrode(Electrode):
  
  """
  NEAElectrode class, child of Electrode.
  
  The data is passed to this method in TEC units which are given in the 
  following block. Internally, the class deals with the data in SI units. The 
  methods which return values return the values in SI units.
  
  Data with constraints and units:
    temperature   >  0 [K]
    barrierHeight >= 0 [eV]
    negativeElectronAffinity >= 0 [eV]
    voltage            [V]
    position           [\mu m]
    richardson    >= 0 [A cm^{-2} K^{-2}]
    emissivity    < 1 & > 0
  """
  
  def __init__(self,inputParams):
    """
    Instantiation of NEAElectrode object.
    """
    
    # is inputParams a dict?
    if inputParams.__class__ is not dict:
      raise TypeError("Inputs must be of type dict.")
    
    # Does inputParams have the correct fields? 
    if not inputParams.has_key("negativeElectronAffinity"):
      raise KeyError("Input dictionary missing a key.")
      
    # Does inputParams have superflous keys? (warning)
    # ADD CODE
      
    # Try to set the object's attributes:
    self["negativeElectronAffinity"] = inputParams["negativeElectronAffinity"]
    Electrode.__init__(self,inputParams)
  
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
    if key == "negativeElectronAffinity" and item < 0:
      raise ValueError("NEA must be positive.")
    
    # Convert to SI units:
    if key is "negativeElectronAffinity":
      item = 1.60217646e-19 * item

    # Set value.
    Electrode.__setitem__(self,key,item)
