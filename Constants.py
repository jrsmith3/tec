#!/usr/bin/python

class Constants:
  """
  Defines the various physical constants relevant to the TEC calculations.
  
  This class defines boltzmann's constant, the electron charge, the
  electron mass, and the Stefan-Boltzmann constant in SI units.
  """
  
  # Here are the constants in SI units:
  boltzmann = 1.380657e-23          # [J K^{-1}]
  permittivity0 = 8.85418781762e-12 # [F m^{-1}]
  electronCharge = 1.60217738e-19   # [C]
  electronMass = 9.1093897e-31      # [kg]
  sigma0 = 5.67050e-8               # [W m^{-2} K^{-4}]
  
  # Here are the constants in TEC units
  #boltzmann = 8.6173423e-5
  #electronCharge = 1
  #electronMass = 1
  #permittivity0 = 8.85418781762e-12 #[F/m] - I'm almost sure these units are wrong.
