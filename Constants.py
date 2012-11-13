# -*- coding: utf-8 -*-

"""
Dict of physical constants used in TEC calculations.
  
TEC calculations are performed using SI units. The TEC API uses a different set
of units. Both are given below.

SI
--
boltzmann = 1.380657e-23          [J K^{-1}]
permittivity0 = 8.85418781762e-12 [F m^{-1}]
electron_charge = 1.60217738e-19  [C]
electron_mass = 9.1093897e-31     [kg]
sigma0 = 5.67050e-8               [W m^{-2} K^{-4}]

TEC units
---------
boltzmann = 8.6173423e-5          [eV K^{-1}]
electron_charge = 1
electron_mass = 1
permittivity0 = 8.85418781762e-12 [F/m] - I'm almost sure these units are wrong.
"""

__author__ = "Joshua Ryan Smith (joshua.r.smith@gmail.com)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2012 Joshua Ryan Smith"
__license__ = 

physical_constants = {boltzmann = 1.380657e-23, \
                      permittivity0 = 8.85418781762e-12
                      electron_charge = 1.60217738e-19  
                      electron_mass = 9.1093897e-31     
                      sigma0 = 5.67050e-8}