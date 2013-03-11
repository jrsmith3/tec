# -*- coding: utf-8 -*-

from scipy import interpolate,integrate,special
import numpy as np
import pdb

class DimensionlessLangmuirPoissonSoln(dict):
  """
  Approximation of solution of Langmuir's dimensionless Poisson's equation.
  """
  
  def __init__(self):
    
    # Here is the algorithm:
    # 1. Set up the default ode solver parameters.
    # 2. Check to see if either the rhs or lhs params were passed as arguments. If not, use the default params.
    # 3. Cat the additional default ode solver parameters to the lhs and rhs set of params.
    # 4. Solve both the lhs and rhs odes.
    # 5. Create the lhs and rhs interpolation objects.
    
    self["lhs"] = self.calc_branch(-2.5538,"lhs")
    # self["rhs"] = self.calc_branch(100,"lhs")
    
    data = np.loadtxt("kleynen_langmuir.dat")
    rhs = data[565:-1,:]
    self["rhs"] = {}

    self["rhs"]["motive_v_position"] = \
      interpolate.interp1d(rhs[:,0],rhs[:,1])
    self["rhs"]["position_v_motive"] = \
        interpolate.interp1d(rhs[:,1],rhs[:,0])
      
  def calc_branch(self, endpoint, side, num_points = 1000):
    """
    Calculates data for either the left or right hand side of the ode solution.
    """
    ics = np.array([0,0])
    position_array = np.linspace(0, endpoint, num_points)
    motive_array = integrate.odeint(self.langmuir_poisson_eq,ics,position_array)
    
    # Create the motive_v_position interpolation, but first check the abscissae (position_array) are monotonically increasing.
    if position_array[0] < position_array[-1]:
      motive_v_position = \
        interpolate.InterpolatedUnivariateSpline(position_array,motive_array[:,0])
    else:
      motive_v_position = \
        interpolate.InterpolatedUnivariateSpline(position_array[::-1],motive_array[::-1,0])
      
    # Now create the position_v_motive interpolation but first check the abscissae (motive_array in this case) are monotonically increasing. Use linear interpolation to avoid weirdness near the origin.
    
    # I think I don't need the following block.
    if motive_array[0,0] < motive_array[-1,0]:
      position_v_motive = \
        interpolate.InterpolatedUnivariateSpline(motive_array[:,0],position_array,k=1)
    else:
      position_v_motive = \
        interpolate.InterpolatedUnivariateSpline(motive_array[::-1,0],position_array[::-1],k=1)
      
    return {"motive_v_position": motive_v_position, 
            "position_v_motive": position_v_motive}
  
  def get_position(self, motive, branch = "lhs"):
    """
    Return position, default negative, given a value of motive.
    """
    
    if type(branch) is not str:
      raise TypeError("branch must be of type str.")
    #if branch is not "lhs" or "rhs":
      #raise ValueError("branch must either be 'lhs' or 'rhs'.")
    
    if motive < 0:
      return np.NaN

    #if branch is "lhs" or branch is "rhs":
    if branch is "lhs" and motive > 18.7:
      return -2.55389
    else:
      return self[branch]["position_v_motive"](motive)
  
  def get_motive(self, position):
    """
    Return motive given a value of position.
    """
    if position < -2.55389:
      return np.NaN
    elif position <= 0:
      return self["lhs"]["motive_v_position"](position)
    else:
      return self["rhs"]["motive_v_position"](position)
  
  def langmuir_poisson_eq(self, motive, position):
    """
    Langmuir's dimensionless Poisson's equation for the ODE solver.
    """
    
    # Note:
    # motive[0] = motive.
    # motive[1] = motive[0]'
    
    if position >= 0:
      return np.array([ motive[1],\
        0.5*np.exp(motive[0])*(1-special.erf( motive[0]**0.5 )) ])
        
    if position < 0:
      return np.array([ motive[1],\
        0.5*np.exp(motive[0])*(1+special.erf( motive[0]**0.5 )) ])
        