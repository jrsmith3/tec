# -*- coding: utf-8 -*-

from scipy import interpolate,integrate,special
import numpy as np

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
    
    self["lhs"] = self.calc_branch(-2.5538)
    self["rhs"] = self.calc_branch(100)
      
  def calc_branch(self, endpoint, num_points = 1000):
    """
    Calculates data for either the left or right hand side of the ode solution.
    """
    ics = np.array([0,0])
    position_array = np.linspace(0, endpoint, num_points)
    motive_array = integrate.odeint(self.langmuir_poisson_eq,ics,position_array)
    
    # NOTE: the InterpolatedUnivariateSpline class requires that the abscissae are monotonically increasing. That is not necessarily the case here.
    # FWIW, here's an easy way to flip a numpy array around: ar[::-1]
    motive_v_position = \
      interpolate.InterpolatedUnivariateSpline(position_array,motive_array[:,0])
    position_v_motive = \
      interpolate.InterpolatedUnivariateSpline(motive_array[:,0],position_array)
      
    return {"motive_v_position": motive_v_position, \
            "position_v_motive": position_v_motive}
  
  def get_position(self, motive, branch = -1):
    """
    Return position, default negative, given a value of motive.
    """
    if branch == -1:
      return self["rhs"]["position_v_motive"](motive)
    elif branch == 1:
      return self["lhs"]["position_v_motive"](motive)
  
  def get_motive(self, position):
    """
    Return motive given a value of position.
    """
    if position >= 0:
      return self["rhs"]["motive_v_position"](position)
    else:
      return self["lhs"]["motive_v_position"](position)

  
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
        