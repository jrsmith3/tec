#!/usr/bin/env python

"""
Generates a list of standard data to verify the Electrode 
calc_saturation_current method is returning numerically accurate values.

As of 2012.11.22 20:47 EST, the sha256 checksum of the resulting data is:
153886103db759defb34adb25d9b55da783257fd3929400c31bb17badbd4926e  electrode_output_current_std.dat
0ab781b6431f1f82f0ca890a263964c043bca33b3d94e9c40fe5c8adb808a603  electrode_vac_energy_no_nea_std.dat
33d8ca7783cc90675f011e22ea2662e9bf66bf89eea87cb6a2498d6ffa02fa10  electrode_vac_energy_with_nea_std.dat
"""

__author__ = "Joshua Ryan Smith (joshua.r.smith@gmail.com)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2012 Joshua Ryan Smith"
__license__ = ""

import pickle
import math
import numpy

boltzmann = 8.6173423e-5
electron_charge = 1.60217738e-19
	  
# Generate data for the calc_saturation_current method.
params = {"temp": 1,
	  "barrier_ht": 1,
	  "richardson": 1,
	  "emissivity": 0.5,
	  "position": 0,
	  "voltage": 0}
	  
temps = range(300,2050,50)
barrier_hts = numpy.arange(0.5,5,0.1)
richardsons = [0.01,0.1,1,10,100]
test_values = []

for temp in temps:
  params["temp"] = temp
  for barrier_ht in barrier_hts:
    params["barrier_ht"] = barrier_ht
    for richardson in richardsons:
      params["richardson"] = richardson
      outpt_cur = params["richardson"] * math.pow(params["temp"],2) * \
	math.exp(-params["barrier_ht"]/(boltzmann * params["temp"]))
      params["outpt_cur"] = outpt_cur
      # You have to use the copy() method otherwise you end up with an array 
      # where every item points to the same object. When you pickle it, you
      # end up with a bunch of the exact same dict.
      test_values.append(params.copy())
      
#pickle the results and write it to a file electrode_output_current_std.dat.
f = open("electrode_output_current_std.dat","w")
pickle.dump(test_values,f)
f.close()


# Generate data for the calc_vacuum_energy method without NEA.
params = {"temp": 1,
	  "barrier_ht": 1,
	  "richardson": 1,
	  "emissivity": 0.5,
	  "position": 0,
	  "voltage": 0}

barrier_hts = numpy.arange(0.5,5,0.1)
test_values = []

for barrier_ht in barrier_hts:
  params["barrier_ht"] = barrier_ht
  vac_energy = params["voltage"] * electron_charge + params["barrier_ht"]
  params["vac_energy"] = vac_energy
  test_values.append(params.copy())

#pickle the results and write it to a file electrode_output_current_std.dat.
f = open("electrode_vac_energy_no_nea_std.dat","w")
pickle.dump(test_values,f)
f.close()


# Generate data for the calc_vacuum_energy method with NEA.
params = {"temp": 1,
	  "barrier_ht": 1,
	  "richardson": 1,
	  "emissivity": 0.5,
	  "position": 0,
	  "voltage": 0,\
	  "nea": 0}

barrier_hts = numpy.arange(0.5,5,0.1)
neas = numpy.arange(0,1.5,0.1)
test_values = []

for barrier_ht in barrier_hts:
  params["barrier_ht"] = barrier_ht
  for nea in neas:
    params["nea"] = nea
    vac_energy = params["voltage"] * electron_charge + \
      params["barrier_ht"] - params["nea"]
    params["vac_energy"] = vac_energy
    test_values.append(params.copy())

#pickle the results and write it to a file electrode_output_current_std.dat.
f = open("electrode_vac_energy_with_nea_std.dat","w")
pickle.dump(test_values,f)
f.close()
