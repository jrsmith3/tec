import numpy as np
from scipy import interpolate, optimize
import matplotlib.pyplot as plt
import matplotlib
from astropy import units, constants


def max_value(calculator):
  """
  Decorator method to calculate the max value, etc. of the requested method.
  """
  def wrapper(self, action = None, set_voltage = False):
    """
    :param action: Key indicating the method's desired action. 
    :param action==None: Simply returns the current value of the method. 
    :param action=="max": Returns the maximum value of the method relative to the output voltage.
    :param action=="voltage": Returns the voltage at which the maximum output occurs.
    :param action=="full": Returns all of the data that the minimization method returns.
    :param set_voltage: If True, leave the voltage set such that the desired output is maximized. Parameter has no effect unless the action argument is "max", "voltage", or "full".
    :type set_voltage: bool
    """
    if action in ["max","voltage","full"]:
      # Save the collector voltage because we are going to be moving it around.
      saved_voltage = self["Collector"]["voltage"]
      
      # Set up the bounds for the minimization.
      lo = self["Emitter"]["voltage"]
      hi = (self["Emitter"]["barrier"] + self["Collector"]["barrier"]) / \
        constants.e + self["Emitter"]["voltage"]
        
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
    if action == "max":
      return -1 * output[1]
    elif action == "voltage":
      return output[0]
    elif action == "full":
      return output
  
  def target_function(voltage,obj):
    """
    Target function of the max_value decorator.
    """
    obj["Collector"]["voltage"] = voltage
    return -1 * calculator(obj)

  return wrapper

class TECBase(object):
  """
  Base thermoelectron engine class

  This class provides the base API for subclasses which implement particular models of TEC electron transport. Even though this class isn't intended to be a model, it implements a model of electron transport which completely ignores the negative space charge effect, similar to the model described on p. 51 of :cite:`978-0-26-208059-0`.

  :param emitter: Object from `tec.electrode` which initializes emitter.
  :param collector: Object from `tec.electrode` which initializes collector.

  Attributes
  ==========
  `TECBase` objects have two attributes: `emitter` and `collector`, both of which are objects from `tec.electrode`.

  Examples
  ========
  >>> from tec.electrode import Metal
  >>> from tec import TECBase
  >>> em = Metal({"temp":1000,
  ...             "barrier":1,
  ...             "voltage":0,
  ...             "position":0,
  ...             "richardson":10,
  ...             "emissivity":0.5})
  >>> co = Metal({"temp":300,
  ...             "barrier":0.8,
  ...             "voltage":0,
  ...             "position":10,
  ...             "richardson":10,
  ...             "emissivity":0.5})
  >>> example_tec = TECBase(emitter = em, collector = co)
  """
  
  def __init__(self,emitter, collector):
    self.emitter = emitter
    self.collector = collector
      
    self.calc_motive()
  

  # Methods regarding motive ----------------------------------------
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
    
    :param position: float or numpy array at which motive is to be evaluated. Returns NaN if position falls outside of the interelectrode space.
    """
    return self["motive_data"]["motive_interp"](position)
  
  def get_max_motive_ht(self, with_position=False):
    """
    Value of the maximum motive relative to ground in J.
    
    :param bool with_position: True returns the position at max motive instead.
    """
    
    max_motive = self["motive_data"]["motive_array"].max()
    max_motive_indx = self["motive_data"]["motive_array"].argmax()
    position_at_max_motive = self["motive_data"]["position_array"][max_motive_indx]
    
    if with_position:
      return position_at_max_motive
    else:
      return max_motive
      
  
  # Methods returning basic data about the TEC ----------------------
  def calc_interelectrode_spacing(self):
    """
    Distance between collector and emitter

    :returns: `astropy.units.Quantity` in units of :math:`um`.
    :symbol: :math:`d`
    """
    return self.collector.position - self.emitter.position

  
  def calc_output_voltage(self):
    """
    Voltage difference between collector and emitter

    :returns: `astropy.units.Quantity` in units of :math:`V`.
    :symbol: :math:`V`
    """
    return self.collector.voltage - self.emitter.voltage

  
  def calc_contact_potential(self):
    """
    Contact potential between collector and emitter
    
    The contact potential is defined as the difference in barrier height between the emitter and collector. This value should not be confused with the quantity returned by :meth:`calc_output_voltage` which is the voltage difference between the collector and emitter.
    """
    return (self.emitter.barrier - self.collector.barrier) / constants.e
    
    
  # Methods regarding current and power -----------------------------
  def calc_forward_current_density(self):
    """
    Net current moving from emitter to collector

    :returns: `astropy.units.Quantity` in units of :math:`A cm^{-2}`.
    :symbol: :math:`J_{f}`
    """
    sat_current_density = self.emitter.calc_saturation_current_density()

    if self.emitter.calc_barrier_ht() >= self.get_max_motive_ht():
      current_density = sat_current_density
    else:
      barrier = self.get_max_motive_ht() - self.emitter.calc_barrier_ht()
      kT = constants.k_B * self.emitter.temp
      exponent = (barrier / kT).decompose()

      current_density = sat_current_density * np.exp(-exponent)

    return current_density


  def calc_back_current_density(self):
    """
    Net current moving from collector to emitter

    :returns: `astropy.units.Quantity` in units of :math:`A cm^{-2}`.
    :symbol: :math:`J_{b}`
    """
    sat_current_density = self.collector.calc_saturation_current_density()

    if self.collector.calc_barrier_ht() >= self.get_max_motive_ht():
      current_density = sat_current_density
    else:
      barrier = self.get_max_motive_ht() - self.collector.calc_barrier_ht()
      kT = constants.k_B * self.emitter.temp
      exponent = (barrier  kT).decompose()

      current_density = sat_current_density * np.exp(-exponent)

    return current_density

  
  def calc_output_current_density(self):
    """
    Net current density flowing across device

    :returns: `astropy.units.Quantity` in units of :math:`A cm^{-2}`.
    :symbol: :math:`J`
    """
    return self.calc_forward_current_density() - self.calc_back_current_density()
  

  # @max_value
  def calc_output_power_density(self):
    """
    Output power density of device

    :returns: `astropy.units.Quantity` in units of :math:`W cm^{-2}`.
    :symbol: :math:`w`
    """
    power_dens = self.calc_output_current_density() * self.calc_output_voltage()

    return power_dens.to("W/cm2")


  # Methods regarding efficiency ------------------------------------
  def calc_carnot_efficiency(self):
    """
    Carnot efficiency
    
    :returns: float between 0 and 1 where unity is 100% efficiency. Returns NaN if collector temperature is greater than emitter temperature.
    :symbol: :math:`J`
    """
    if self.emitter.temp >= self.collector.temp:
      efficiency = 1 - (self.collector.temp / self.emitter.temp)
    else:
      efficiency = np.NaN

    return efficiency
  

  def calc_radiation_efficiency(self):
    """
    Efficiency considering only blackbody heat transport in range 0 to 1.

    This method will return nan if the output power is less than zero. See :cite:`978-0-26-208059-0` p. 73 for a description of how the radiation efficiency is calculated.
    """
    if self.calc_output_power_density() > 0:
      return self.calc_output_power_density() / self.__calc_black_body_heat_transport()
    else:
      return np.nan
  

  def calc_electronic_efficiency(self):
    """
    Efficiency considering only electronic heat transport in range 0 to 1.

    This method will return nan if the output power is less than zero. See :cite:`978-0-26-208059-0` p. 73 for a description of how the electronic efficiency is calculated.
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
    
    A description of electronic losses can be found in :cite:`978-0-26-208059-0`, page 69 (eq. 2.57a).
    """
    elecHeatTransportForward = self.calc_forward_current_density()*(self.get_max_motive_ht()+\
      2 * constants.k_B * self["Emitter"]["temp"]) / \
      constants.e
    elecHeatTransportBackward = self.calc_back_current_density()*(self.get_max_motive_ht()+\
      2 * constants.k_B * self["Collector"]["temp"]) / \
      constants.e
    return elecHeatTransportForward - elecHeatTransportBackward
  

  def __calc_black_body_heat_transport(self):
    """
    Returns the radiation transport of a TECBase object.

    Equation for radiative heat transfer taken from :cite:`978-0-471-45727-5` p. 793, Eq. 13.19.
    """
    return constants.sigma_sb * \
      (self["Emitter"]["temp"]**4 - self["Collector"]["temp"]**4) / \
      ((1./self["Emitter"]["emissivity"]) + (1./self["Collector"]["emissivity"]) - 1)


  # Methods for plotting --------------------------------------------
  def plot_motive(self, axl = None, show = False, fontsize = False, output_voltage = False):
    """
    Plot an annotated motive diagram relative to ground.

    :param axl: :class:`matplotlib.Axes` object on which to draw motive diagram. None results in a new figure with a subplot(111) as the location to draw the motive diagram.
    :param bool show: If True, :meth:`pyplot.show()` the result.
    :param int fontsize: Annotation font size.
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
    mot = self.get_motive(pos) / constants.e

    # Plot all the items on the emitter-side axes.
    axl.plot(pos,mot,"k")

    # Work out the x-interval.
    x_interval = self["Collector"]["position"] - self["Emitter"]["position"]

    # maximum motive
    plt.plot(self.get_max_motive_ht(with_position=True), self.get_max_motive_ht() / constants.e, 'k+')
    plt.annotate("$\psi_{m}$", 
      xytext = (1.1 * self.get_max_motive_ht(with_position=True), 1.05 * self.get_max_motive_ht() / constants.e),
      xy = (self.get_max_motive_ht(with_position=True), self.get_max_motive_ht() / constants.e))
    
    # labels and dimension lines
    for el, factr in zip(["Emitter", "Collector"],[-1,1]):
      if "nea" in self[el]:
        nea = "$\chi_{" + el[0] + "}$"
        self.dimension_line(nea, self[el]["position"] + (factr * 0.25 * x_interval), 
          self[el].calc_motive_bc() / constants.e, 
          self[el].calc_barrier_ht() / constants.e)
        barrier = "$\zeta_{" + el[0] + "}$"
        barrier_pos = 0.6
      else:
        barrier = "$\phi_{" + el[0] + "}$"
        barrier_pos = 0.25
      self.dimension_line(barrier,self[el]["position"] + \
        (factr * barrier_pos * x_interval), 
        self[el]["voltage"], 
        self[el].calc_barrier_ht() / constants.e)

      # Code for output voltage
      if output_voltage:
        if el == "Collector":
          self.dimension_line("eV",self[el]["position"] + \
            (factr * barrier_pos * x_interval), 
            self["Emitter"]["voltage"], 
            self[el]["voltage"])

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
      constants.e, 
      self["Collector"].calc_barrier_ht() / constants.e, 
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
    Helper method to properly draw barrier on the motive diagram using spines.
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
      self[el].calc_barrier_ht() / constants.e)

    # Set up ticks and labels for emitter.
    ticks_labels = ["$\mu_{" + el[0] + "}$",
              "$\psi_{" + el[0] + "}$",
              "$\psi_{" + el[0] + ",CBM}$"]
    if "nea" in self[el]:
      ticks_loc = matplotlib.ticker.FixedLocator([self[el]["voltage"],
        self[el].calc_motive_bc() / constants.e,
        self[el].calc_barrier_ht() / constants.e])
    else:
      del ticks_labels[-1]
      ticks_loc = matplotlib.ticker.FixedLocator([self[el]["voltage"],
        self[el].calc_barrier_ht() / constants.e])

    ticks_format = matplotlib.ticker.FixedFormatter(ticks_labels)

    # Apply ticks to axes object
    ax.yaxis.set_major_locator(ticks_loc)
    ax.yaxis.set_major_formatter(ticks_format)

  def dimension_line(self, label, x, y_lo, y_hi, label_loc = "mi", label_pos = "left"):
    """
    Helper method to plot vertical dimension line on the motive diagram.

    :param dict label: Dict containing sub-dicts which can instantiate 

    :param string label: Label for dimension line.
    :param float x: Horizontal placement of dimension line.
    :param float y_lo: Lower extent of dimension line.
    :param float y_hi: Upper extent of dimension line.
    :param str label_loc: Vertical placement of the label. Can be "lo" "mi" or "hi".
    :param str label_pos: Which side of the dimension line the label is placed ("left" or "right").
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
