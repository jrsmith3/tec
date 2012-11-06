from tec import Electrode
from tec import Constants
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
  
  def __init__(self,inputParams):
    """
    Instantiation of TEC object.
    """
    
    # is inputParams a dict?
    if inputParams.__class__ is dict:
      # Does inputParams have the correct fields? Compare the keys of 
      # inputParams to a list of the correct field names.
      correctFields = ["Emitter","Collector"]
      inputParamKeys = inputParams.keys()
      if correctFields.sort() != inputParamKeys.sort():
        raise KeyError("Input dictionary missing a key.")
    else:
      raise TypeError("Inputs must be of type dict or TEC.")
    
    # does it have superflous entries? (warning)
    # ADD CODE

    # Try to set the object's attributes:
    self["Emitter"] = inputParams["Emitter"]
    self["Collector"] = inputParams["Collector"]
  
  def __setitem__(self,key,item):
    """
    Sets attribute values according to Electrode constraints.
    """
    # Try to turn the argument into an Electrode. The Electrode class has a lot
    # of error checking and if the argument can't make it through that checking,
    # its not worth proceeding.
    ElecItem = Electrode(item)
    
    # Check constraints on arguments.
    self.__checkconstraints(key,ElecItem)
    
    # Set value.
    dict.__setitem__(self,key,ElecItem)
    
  #def __getitem__(self,key):
    #"""
    #Gets item.
    
    #I'm pretty sure I can put a hook in here to catch when the user is trying
    #to directly violate the constraints on the parameters; i.e. when the user
    #is trying to directly set, e.g., the temperature of the emitter less than
    #that of the collector: TEC["Emitter"]["temperature"]
    #"""
    
    #return dict.__getitem__(self,key)
    
  def __checkconstraints(self,key,ElecItem):
    """
    Check to see if the constraints are met. This method doesn't return any
    value, it just raises an exception if the constraints aren't met.
    """
      
    # This next if statement is here for the following reason: This set method
    # is called when the object is instantiated AND for general attribute 
    # setting. When this method is called during instantiation, it may be that
    # one or both of the attributes (Emitter or Collector) are not set. Thus, 
    # during the bound-checking, comparing the values of the variable 'item' 
    # against a non-existant attribute will fail. I'm trying to avoid this 
    # failure. There are four cases that need to be considered: 1. Emitter not 
    # set, Collector not set 2. Emitter set, Collector not set. 3. Emitter not 
    # set, Collector set 4. Emitter set, Collector set. It turns out that it
    # only matters if we encounter the case where neither the Emitter nor the 
    # Collector is set. If we encounter the case where neither attribute is set,
    # we can just set the attribute. Otherwise, we'll do the boundchecking.
    
    if self.has_key("Emitter") or self.has_key("Collector"):
    # Was previously more confusing:   
    #if not(not self.has_key("Emitter") and not self.has_key("Collector")):
      # Check to see if constraints are met.
      if key == "Emitter":
        if ElecItem["temperature"] < self["Collector"]["temperature"]:
          raise ValueError("Emitter temp must be greater than Collector temp")
        if ElecItem["position"] > self["Collector"]["position"]:
          raise ValueError("Emitter pos must be less than Collector pos.")
      if key == "Collector":
        if ElecItem["temperature"] > self["Emitter"]["temperature"]:
          raise ValueError("Emitter temp must be greater than Collector temp")
        if ElecItem["position"] < self["Emitter"]["position"]:
          raise ValueError("Emitter pos must be less than Collector pos.")
      

  # Methods ==================================================================
  def calcinterelectrodespacing(self):
    """
    Return distance between Collector and Emitter [um].
    """
    return self["Collector"]["position"] - self["Emitter"]["position"]
  
  def calcoutputvoltage(self):
    """
    Return potential difference between Emitter and Collector [V].
    """
    return self["Collector"]["voltage"] - self["Emitter"]["voltage"]
  
  def calccontactpotential(self):
    """
    Return contact potential [V].
    
    The contact potential is defined as the difference in barrier height between
    the emitter and collector. This value should not be confused with the output
    voltage which is the voltage difference between the collector and emitter.
    """
    return (self["Emitter"]["barrierHeight"] - \
      self["Collector"]["barrierHeight"])/Constants.electronCharge
    
  def calcforwardcurrentdensity(self):
    """
    Return forward current density [A cm^{-2}].
    """
    
    if self["Emitter"]["barrierHeight"] < self.calcmaxmotiveheight():
      return self["Emitter"].calcsaturationcurrent() * \
        math.exp(-(self.calcmaxmotiveheight()-self["Emitter"]["barrierHeight"])/\
          (Constants.boltzmann * self["Emitter"]["temperature"]))
    else:
      return self["Emitter"].calcsaturationcurrent()
  
  def calcbackcurrentdensity(self):
    """
    Return back current density [A cm^{-2}].
    """
    
    if self["Collector"]["barrierHeight"] < self.calcmaxmotiveheight():
      return self["Collector"].calcsaturationcurrent() * \
        math.exp(-(self.calcmaxmotiveheight()-self["Collector"]["barrierHeight"]-self.calcoutputvoltage())/ \
          (Constants.boltzmann * self["Collector"]["temperature"]))
    else:
      return self["Collector"].calcsaturationcurrent()
  
  def calcoutputcurrentdensity(self):
    """
    Return output current density: diff. between forward and back current [A cm^{-2}].
    """
    return self.calcforwardcurrentdensity() - self.calcbackcurrentdensity()
  
  def calcoutputpowerdensity(self):
    """
    Return output power density [W cm^{-2}].
    """
    return self.calcoutputcurrentdensity() * self.calcoutputvoltage()
  
  # This method needs work: voltage/current density is not resistance
  def calcloadresistance(self):
    """
    Return load resistance [Ohms].
    """
    # There is something fishy about the units in this calculation.
    if self.calcoutputcurrentdensity() != 0:
      return self.calcoutputvoltage() / self.calcoutputcurrentdensity()
    else:
      return np.nan
  
  # Methods regarding interesting maximum values ------------------------------
  #def calcmaxoutputpowerdensity(self):
    #"""
    #Return maximum output power density [W cm^{-2}].
    #
    #Optionally, return the voltage at which the maximum power density occurs.
    #"""
    #
    # This method is model-independent because there will always be a 
    # model-dependent way to determine the voltage at which the maximum output
    # power density occurs.
    # First, I'll cache the Collector voltage because the strategy I'm using
    # requires that I change the object's Collector voltage. I'll then calculate
    # the voltage at which the maximum output power occurs, put the Collector 
    # voltage back, and finally return the value of maximum output power.
    #cachedVoltage = self["Collector"]["voltage"]
    #self["Collector"]["voltage"] = self.calcvoltageatmaxoutputpowerdensity()
    #maxOutputPowerDensity = self.calcoutputpowerdensity()
    #self["Collector"]["voltage"] = cachedVoltage
    #return maxOutputPowerDensity
  
  #def calcvoltageatmaxoutputpowerdensity(self):
    #"""
    #Voltage corresponding to maximum output power density [V]
    #"""
    
    ## This method is model-dependent, so I'm just going to pass.
    #pass
  
  #def __maxoutputpowertf(self,targetVoltage):
    #"""
    #The target function for finding the maximum output power density and the
    #corresponding voltage.
    #"""
    #self["Collector"]["voltage"] = targetVoltage
    #return -self.calcoutputpowerdensity()
  
  #def calcmaxefficiency(self):
    #"""
    #Return maximum total efficiency in the range 0 to 1.
    #
    #Optionally, return the voltage at which the maximum efficiency occurs.
    #"""
    #  
    # This method is model-independent because there will always be a 
    # model-dependent way to determine the voltage at which the maximum 
    # efficiency occurs.
    # First, I'll cache the Collector voltage because the strategy I'm using
    # requires that I change the object's Collector voltage. I'll then calculate
    # the voltage at which the maximum efficiency occurs, put the Collector 
    # voltage back, and finally return the value of maximum efficiency.
    #cachedVoltage = self["Collector"]["voltage"]
    #self["Collector"]["voltage"] = self.calcvoltageatmaxefficiency()
    #maxEfficiency = self.calctotalefficiency()
    #self["Collector"]["voltage"] = cachedVoltage
    #return maxEfficiency
  
  #def calcvoltageatmaxefficiency(self):
    #"""
    #Voltage corresponding to maximum total efficiency
    #"""
    
    ## This method is model-dependent, so I'm just going to pass.
    #pass
  
  #def __maxefficiencytf(self,targetVoltage):
    #"""
    #The target function for finding the maximum efficiency and the corresponding
    #voltage.
    #"""
    #self["Collector"]["voltage"] = targetVoltage
    #return -self.calctotalefficiency()
  
  
  # Methods regarding motive --------------------------------------------------
  def calcmotive(self, arrayLength = 100):
    """
    WARNING: THIS METHOD OUTPUTS DUMMY DATA AND MUST BE OVERLOADED FOR SUBCLASSING.
    
    Return the motive vs. position as a dict.
    
    The returned dict has two fields, "motive" and "position". Each field
    contains a 1D numpy array of length defined by the int input argument
    arrayLength. The default value for arrayLength is 100.
    """
    return {"position": np.ones(arrayLength) ,\
            "motive": np.ones(arrayLength)}
  
  def calcmaxmotiveheight(self):
    """
    Returns the value of the maximum motive height in [eV]. 
    
    This value should not be confused with the maximum motive given in 
    "Thermionic Energy Conversion Vol. 1" by Hatsopoulos and Gyftopoulos as 
    \psi_{m}. The value returned by this method is equivalent to 
    \psi_{m} - \mu_{E}.
    """
    motive = self.calcmotive()
    return float(motive["motive"].max())
  
  #def calcpositionatmaxmotive(self):
    #"""
    #Position at which the max. motive occurs [um]
    #"""
    #motive = self.calcmotive()
    #indx = motive[:,1].argmax()
    #return float(motive[indx,0])
  
  
  # Methods regarding efficiency ----------------------------------------------
  def calccarnotefficiency(self):
    """
    Return value of carnot efficiency in the range 0 to 1.
    
    This method will return a negative value if the emitter temperature is less
    than the collector temperature.
    """
    return 1 - (self["Collector"]["temperature"]/self["Emitter"]["temperature"])
  
  def calcradiationefficiency(self):
    """
    Return efficiency of device considering only blackbody heat transport.
    
    The output will be between 0 and 1. If the output power is less than zero,
    return nan.
    """
    if self.calcoutputpowerdensity() > 0:
      return self.calcoutputpowerdensity() / self.__calcblackbodyheattransport()
    else:
      return np.nan
  
  def calcelectronicefficiency(self):
    """
    Return efficiency of device considering only electronic heat transport.
    
    The output will be between 0 and 1. If the output power is less than zero,
    return nan.

    See "Thermionic Energy Conversion Vol. I" by Hatsopoulous and Gyftopoulous
    pp 73 for a description of the electronic efficiency.
    """
    if self.calcoutputpowerdensity() > 0:
      return self.calcoutputpowerdensity() / self.__calcelectronicheattransport()
    else:
      return np.nan
  
  def calctotalefficiency(self):
    """
    Return total efficiency considering all heat transport mechanisms.
    
    The output will be between 0 and 1. If the output power is less than zero,
    return nan.
    """
    if self.calcoutputpowerdensity() > 0:
      return self.calcoutputpowerdensity() / \
        (self.__calcblackbodyheattransport() + self.__calcelectronicheattransport())
    else:
      return np.nan

  def __calcelectronicheattransport(self):
    """
    Returns the electronic heat transport of a TEC object.
    
    A description of electronic losses can be found on page 69 (eq. 2.57a) of
    "Thermionic Energy Conversion Vol. 1" by Hatsopoulous and Gyftopoulous.
    """
    elecHeatTransportForward = self.calcforwardcurrentdensity()*(self.calcmaxmotiveheight()+\
      2 * Constants.boltzmann * self["Emitter"]["temperature"]) / \
      Constants.electronCharge
    elecHeatTransportBackward = self.calcbackcurrentdensity()*(self.calcmaxmotiveheight()+\
      2 * Constants.boltzmann * self["Collector"]["temperature"]) / \
      Constants.electronCharge
    return elecHeatTransportForward - elecHeatTransportBackward
  
  def __calcblackbodyheattransport(self):
    """
    Returns the radiation transport of a TEC object.
    """
    return Constants.sigma0 * \
      (self["Emitter"]["emissivity"] * pow(self["Emitter"]["temperature"],4) - \
      self["Collector"]["emissivity"] * pow(self["Collector"]["temperature"],4))
    
