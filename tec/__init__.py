# -*- coding: utf-8 -*-
"""
=========================
Base Library (:mod:`tec`)
=========================

.. currentmodule:: tec

Base library

.. autoclass:: Electrode
  :members:
.. autoclass:: TECBase
  :members:
"""

import numpy as np
from scipy import interpolate,optimize
import matplotlib.pyplot as plt
import matplotlib

physical_constants = {"boltzmann" : 1.3806488e-23, \
                      "permittivity0" : 8.85418781762e-12, \
                      "electron_charge" : 1.602176565e-19, \
                      "electron_mass" : 9.1093897e-31, \
                      "sigma0" : 5.67050e-8}

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
      saturation_current = self["richardson"] * self["temp"]**2 * \
      np.exp(-self["barrier"]/(physical_constants["boltzmann"] * self["temp"]))
    
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
    

def max_value(calculator):
  """
  Decorator method to calculate the maximum value of the requested method.
  """
  def wrapper(self, with_output = False, set_voltage = False):
    """
    Arguments (* denotes default argument):
      with_output == "max": Returns the maximum value of the method relative to the output voltage.
                     "voltage": Returns the voltage at which the maximum output occurs.
                     "full": Returns all of the data that the minimization method returns.
                     else*: Do no minimization and just return the current value of the method.
      set_voltage == True: After the optimization, leave the object with an output voltage that maximizes the method in question.
                     False*: Return the output voltage to whatever it was originally.
                     
      The set_voltage argument has no effect unless the with_output argument is "max", "voltage", or "full". 
    """
    if with_output in ["max","voltage","full"]:
      # Save the collector voltage because we are going to be moving it around.
      saved_voltage = self["Collector"]["voltage"]
      
      # Set up the bounds for the minimization.
      lo = self["Emitter"]["voltage"]
      hi = (self["Emitter"]["barrier"] + self["Collector"]["barrier"]) / \
        physical_constants["electron_charge"] + self["Emitter"]["voltage"]
        
      # God, this is fugly and probably wrong.
      output = optimize.fminbound(target_function,lo,hi,[self],full_output = True)
      
      # I don't know if this code is the best way to set the voltage.
      if set_voltage is True:
        # Just leave everything alone.
        pass
      else:
        # Put everything back like it was.
        self["Collector"]["voltage"] = saved_voltage
    else:    
      return calculator(self)
    
    # Figure out what to return.
    if with_output == "max":
      return -1 * output[1]
    elif with_output == "voltage":
      return output[0]
    elif with_output == "full":
      return output
  
  def target_function(voltage,obj):
    """
    Target function of the max_value decorator.
    """
    obj["Collector"]["voltage"] = voltage
    return -1 * calculator(obj)

  return wrapper

class TECBase(dict):
  
  """
  Thermionic engine simulator. Ignores space charge, considers NEA.

  dict-like object that implements a model of electron transport; ignores the negative space charge effect. This class calculates a motive between the vacuum levels of the two elecrodes which may or may not feature NEA. The model is based on [1]. 

  Attributes
  ----------
  The attributes of the object are accessed like a dictionary. The object has three attributes, "Emitter" and "Collector" are both Electrode objects. "motive_data" is a dictionary containing (meta)data calculated during the motive calculation. "motive_data" should usually be accessed via the class's convenience methods. "motive_data" contains the following data:

    motive_array:   A two-element array containing the electrostatic boundary 
                    conditions, i.e. the vacuum level of the emitter and 
                    collector, respectively.
    
    position_array: A two-element array containing the values of position 
                    corresponding to the values in motive_array.
                    
    motive_interp:  A scipy.interpolate.interp1d object that interpolates the 
                    two arrays described above used in the class's convenience 
                    methods.

  Parameters
  ----------
  The TECBase class is instantiated by a dict with two keys, "Emitter" and "Collector" (case insensitive). Both keys have data that is also of type dict which are configured to instantiate an Electrode object. Additional keys will be ignored and there are no default values for instantiation.

  Examples
  --------
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
  ...            "emissivity":0.5}
  >>> input_dict = {"Emitter":em_dict, "Collector":co_dict}
  >>> example_tec = TECBase(input_dict)
  
  Notes
  -----
  "motive_data" contains the interp1d object because there's no sense in re-instantiating it every time I call the associated methods.

  Bibliography
  ------------
  [1] "Thermionic Energy Conversion, Vol. I." Hatsopoulous and Gyftopoulous. p. 48.
  """
  
  def __init__(self,input_params):
    # is input_params a dict?
    if not isinstance(input_params,dict):
      raise TypeError("Inputs must be of type dict.")

    # Ensure that the required fields are present in input_params.
    req_fields = ["Emitter","Collector"]
    input_param_keys = set(input_params.keys())
    
    if not set(req_fields).issubset(input_param_keys):
      raise KeyError("Input dict is missing one or more keys.")
    
    # Try to set the object's attributes:
    for key in req_fields:
      self[key] = input_params[key]
      
    self.calc_motive()
  
  def __setitem__(self,key,item):
    """
    Sets attribute values according to Electrode constraints.
    """
    # Try to turn the argument into an Electrode. The Electrode class has a lot
    # of error checking and if the argument can't make it through that checking,
    # its not worth proceeding.
    if key in ["Emitter","Collector"]:
      item = Electrode(item)
    
    # Set value.
    dict.__setitem__(self,key,item)
    
  def __getitem__(self,key):
    """
    Return attribute, recalculating motive_data if necessary.
    """
    
    # By the time we are calling this method, the object has been instantiated. Therefore it has all of the necessary attributes (Emitter, Collector, motive_data). It is possible that one of the Electrodes' data has changed in such a way that it is no longer consistant with motive_data. The Electrode already knows it has changed because it now has an item called, "param_changed". At this point all I have to do is look for that attribute in both Electrodes, delete it, delete "motive_data" and then call calc_motive().
    
    for el in ["Emitter","Collector"]:
      El = dict.__getitem__(self,el)
      if El.param_changed_and_reset():
        del self["motive_data"]
        self.calc_motive()
      
    return dict.__getitem__(self,key)
  
  # Methods regarding motive --------------------------------------------------
  def calc_motive(self):
    """
    Calculates the motive (meta)data and populates the 'motive_data' attribute.
    """
    motive_array = np.array([self["Emitter"].calc_motive_bc(), \
      self["Collector"].calc_motive_bc()])
    position_array = np.array([self["Emitter"]["position"], \
      self["Collector"]["position"]])
    motive_interp = interpolate.InterpolatedUnivariateSpline(position_array, motive_array, k = 1)
    
    self["motive_data"] = {"motive_array":motive_array, \
                           "position_array":position_array, \
                           "motive_interp":motive_interp}

  def get_motive(self, position):
    """
    Value of motive relative to ground for given value(s) of position in J.
    
    Position must be of numerical type or numpy array. Returns NaN if position 
    falls outside of the interelectrode space.
    """
    return self["motive_data"]["motive_interp"](position)
  
  def get_max_motive_ht(self, with_position=False):
    """
    Returns value of the maximum motive relative to ground in J.
    
    If with_position is True, return the position at max motive.
    """
    
    max_motive = self["motive_data"]["motive_array"].max()
    max_motive_indx = self["motive_data"]["motive_array"].argmax()
    position_at_max_motive = self["motive_data"]["position_array"][max_motive_indx]
    
    if with_position:
      return position_at_max_motive
    else:
      return max_motive
      
  
  # Methods returning basic data about the TEC --------------------------------
  def calc_interelectrode_spacing(self):
    """
    Return distance between Collector and Emitter in m.
    """
    return self["Collector"]["position"] - self["Emitter"]["position"]
  
  def calc_output_voltage(self):
    """
    Return potential difference between Emitter and Collector in V.
    """
    return self["Collector"]["voltage"] - self["Emitter"]["voltage"]
  
  def calc_contact_potential(self):
    """
    Return contact potential in V.
    
    The contact potential is defined as the difference in barrier height between
    the emitter and collector. This value should not be confused with the output
    voltage which is the voltage difference between the collector and emitter.
    """
    return (self["Emitter"]["barrier"] - \
      self["Collector"]["barrier"])/physical_constants["electron_charge"]
    
    
  # Methods regarding current and power ---------------------------------------
  def calc_forward_current_density(self):
    """
    Return forward current density in A m^{-2}.
    """
    
    if self["Emitter"].calc_barrier_ht() >= self.get_max_motive_ht():
      return self["Emitter"].calc_saturation_current()
    else:
      barrier = self.get_max_motive_ht() - self["Emitter"].calc_barrier_ht()
      return self["Emitter"].calc_saturation_current() * \
	np.exp(-barrier/(physical_constants["boltzmann"]*self["Emitter"]["temp"]))
  
  def calc_back_current_density(self):
    """
    Return back current density in A m^{-2}.
    """
    
    if self["Collector"].calc_barrier_ht() >= self.get_max_motive_ht():
      return self["Collector"].calc_saturation_current()
    else:
      barrier = self.get_max_motive_ht() - self["Collector"].calc_barrier_ht()
      return self["Collector"].calc_saturation_current() * \
	np.exp(-barrier/(physical_constants["boltzmann"]*self["Collector"]["temp"]))
  
  
  def calc_output_current_density(self):
    """
    Return difference between forward and back current density in A m^{-2}.
    """
    return self.calc_forward_current_density() - \
      self.calc_back_current_density()
  
  @max_value
  def calc_output_power_density(self):
    """
    Return output power density in W m^{-2}.
    """
    return self.calc_output_current_density() * self.calc_output_voltage()
  
  # This method needs work: voltage/current density is not resistance
  def calc_load_resistance(self):
    """
    Return load resistance in ohms.
    """
    # There is something fishy about the units in this calculation.
    if self.calc_output_current_density() != 0:
      return self.calc_output_voltage() / self.calc_output_current_density()
    else:
      return np.nan
  

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
  
  @max_value
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
    Returns the electronic heat transport of a TECBase object.
    
    A description of electronic losses can be found on page 69 (eq. 2.57a) of
    "Thermionic Energy Conversion Vol. 1" by Hatsopoulous and Gyftopoulous.
    """
    elecHeatTransportForward = self.calc_forward_current_density()*(self.get_max_motive_ht()+\
      2 * physical_constants["boltzmann"] * self["Emitter"]["temp"]) / \
      physical_constants["electron_charge"]
    elecHeatTransportBackward = self.calc_back_current_density()*(self.get_max_motive_ht()+\
      2 * physical_constants["boltzmann"] * self["Collector"]["temp"]) / \
      physical_constants["electron_charge"]
    return elecHeatTransportForward - elecHeatTransportBackward
  
  def __calc_black_body_heat_transport(self):
    """
    Returns the radiation transport of a TECBase object.

    Equation for radiative heat transfer taken from Incropera et.al. p. 793, Eq. 13.19. ISBN:978-0-471-45727-5.
    """
    return physical_constants["sigma0"] * \
      (self["Emitter"]["temp"]**4 - self["Collector"]["temp"]**4) / \
      ((1./self["Emitter"]["emissivity"]) + (1./self["Collector"]["emissivity"]) - 1)

  def plot_motive(self, axl = None, show = False, fontsize = False):
    """
    Plot an annotated motive diagram relative to ground.

    If this method is called without an argument, it will create a figure with a subplot(111) and plot the motive diagram with the barriers, neas, voltages, etc. If a matplotplib Axes object is passed to this method, this method will draw the motive diagram on that Axes. If show == True, the method will pyplot.show() the result.
    """

    if axl == None:
      fig = plt.figure()
      axl = fig.add_subplot(111)
    else:
      fig = plt.gcf()

    # Create the axes object for the collector barrier visualization.
    axr = fig.add_axes(axl.get_position())

    # Generate the position and corresponding motive values.
    pos = np.linspace(self["Emitter"]["position"],self["Collector"]["position"],100)
    mot = self.get_motive(pos) / physical_constants["electron_charge"]

    # Plot all the items on the emitter-side axes.
    axl.plot(pos,mot,"k")

    # Work out the x-interval.
    x_interval = self["Collector"]["position"] - self["Emitter"]["position"]

    # maximum motive
    plt.plot(self.get_max_motive_ht(with_position=True), self.get_max_motive_ht() / physical_constants["electron_charge"], 'k+')
    plt.annotate("$\psi_{m}$", 
      xytext = (1.1 * self.get_max_motive_ht(with_position=True), 1.05 * self.get_max_motive_ht() / physical_constants["electron_charge"]),
      xy = (self.get_max_motive_ht(with_position=True), self.get_max_motive_ht() / physical_constants["electron_charge"]))
    
    # labels and dimension lines
    for el, factr in zip(["Emitter", "Collector"],[-1,1]):
      if "nea" in self[el]:
        nea = "$\chi_{" + el[0] + "}$"
        self.dimension_line(nea, self[el]["position"] + (factr * 0.25 * x_interval), 
          self[el].calc_motive_bc() / physical_constants["electron_charge"], 
          self[el].calc_barrier_ht() / physical_constants["electron_charge"])
        barrier = "$\zeta_{" + el[0] + "}$"
        barrier_pos = 0.6
      else:
        barrier = "$\phi_{" + el[0] + "}$"
        barrier_pos = 0.25
      self.dimension_line(barrier,self[el]["position"] + \
        (factr * barrier_pos * x_interval), 
        self[el]["voltage"], 
        self[el].calc_barrier_ht() / physical_constants["electron_charge"])

    self.barrier_artist(axl, "Emitter")
    self.barrier_artist(axr, "Collector")

    # x-scaling
    xl_buffer = 0.25
    xr_buffer = 0.6
    xmin = self["Emitter"]["position"] - (xl_buffer * x_interval)
    xmax = self["Collector"]["position"] + (xr_buffer * x_interval)
    xlim = (xmin, xmax)

    axl.set_xlim(xlim)
    axr.set_xlim(xlim)

    # y-scaling
    y_lo = min([0, self["Emitter"]["voltage"], self["Collector"]["voltage"]])
    y_hi = max([self["Emitter"].calc_barrier_ht() / \
      physical_constants["electron_charge"], 
      self["Collector"].calc_barrier_ht() / physical_constants["electron_charge"], 
      self.get_max_motive_ht()])

    axl.set_ylim([y_lo, 1.1 * y_hi])
    axr.set_ylim([y_lo, 1.1 * y_hi])

    # Set the fontsize of all the elements.
    if fontsize:
      axs = [axl, axr]

      for ax in axs:
        # Set fontsize of annotations
        for child in ax.get_children():
          if isinstance(child, matplotlib.text.Annotation):
            child.set_fontsize(fontsize)
          if isinstance(child, matplotlib.axis.YAxis):
            for tick_label in child.get_majorticklabels():
              tick_label.set_fontsize(fontsize)

    if show:
      plt.show()

  def barrier_artist(self, ax, el):
    """
    Helper method to properly draw barrier using spines.
    """
    if el == "Emitter":
      loc = "left"
    else:
      loc = "right"

    # Initialize the axes borders, etc.
    ax.xaxis.set(visible = False)
    ax.spines["top"].set_color("none")
    ax.spines["bottom"].set_color("none")
    ax.spines["right"].set_color("none")
    ax.spines["left"].set_color("none")
    ax.patch.set_visible(False)

    # Switch back on the appropriate spine.
    ax.spines[loc].set_color("k")
    ax.spines[loc].set_linewidth(0.25)

    # Only have ticks on the proper side of the plot
    ax.yaxis.set_ticks_position(loc)
    ax.tick_params(direction = "outward")

    # Draw the barrier of the electrode using the axes object's spines. Constrain it to the proper side of the motive curve.
    # Fix the unit offset on the right
    if el == "Collector":
      x_loc = self[el]["position"] - 1
    else:
      x_loc = self[el]["position"]

    ax.spines[loc].set_position(("data", x_loc))
    ax.spines[loc].set_bounds(self[el]["voltage"], 
      self[el].calc_barrier_ht() / physical_constants["electron_charge"])

    # Set up ticks and labels for emitter.
    ticks_labels = ["$\mu_{" + el[0] + "}$",
              "$\psi_{" + el[0] + "}$",
              "$\psi_{" + el[0] + ",CBM}$"]
    if "nea" in self[el]:
      ticks_loc = matplotlib.ticker.FixedLocator([self[el]["voltage"],
        self[el].calc_motive_bc() / physical_constants["electron_charge"],
        self[el].calc_barrier_ht() / physical_constants["electron_charge"]])
    else:
      del ticks_labels[-1]
      ticks_loc = matplotlib.ticker.FixedLocator([self[el]["voltage"],
        self[el].calc_barrier_ht() / physical_constants["electron_charge"]])

    ticks_format = matplotlib.ticker.FixedFormatter(ticks_labels)

    # Apply ticks to axes object
    ax.yaxis.set_major_locator(ticks_loc)
    ax.yaxis.set_major_formatter(ticks_format)

  def dimension_line(self, label, x, y_lo, y_hi, label_loc = "mi", label_pos = "left"):
    """
    Plots a vertical dimension line on the gca().

    label: string labeling the dimension line.  
    x: horizontal placement of dimension line.
    y_lo: dimension line will extend down to this position.
    y_hi: dimension line will extend up to this position.
    label_loc: vertical placement of the label. Can be "lo" "mi" or "hi".
    label_pos: which side of the dimension line the label is placed.
    """
    ax = plt.gca()

    # Figure out where the text should go.
    if label_pos == "right":
      ha = "right"
    else:
      ha = "left"

    if label_loc == "hi":
      label_y = np.mean([y_lo, y_hi, y_hi, y_hi])
    elif label_loc == "lo":
      label_y = np.mean([y_lo, y_lo, y_lo, y_hi])
    else:
      label_y = np.mean([y_lo, y_hi])

    # Write the text.
    ax.annotate(label, xy = [x, y_lo], xytext = [x, label_y], ha = "center",
      arrowprops = {"arrowstyle":"->", "linewidth":0.25})
    ax.annotate(label, xy = [x, y_hi], xytext = [x, label_y], ha = "center",
      arrowprops = {"arrowstyle":"->", "linewidth":0.25})
