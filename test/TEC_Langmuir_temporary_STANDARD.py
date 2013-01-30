# -*- coding: utf-8 -*-
import pickle
import copy
import csv

"""
Convert data in jrsssl000059.dat to STANDARD format for testing.

This script takes the data I used in paper \cite{}, Fig. \ref{} and converts it to a format that matches what I'm using to numerically test the methods for the classes in the rest of this package. Part of the conversion is by hand, and the other is programmatically.

This data tests a very narrow range of values and therefore isn't comprehensive. I am mainly using it for TDD on the methods of the TEC_Langmuir class.
"""

def get_data():
  f = open("jrsssl000059.dat","r")
  data = []
  for line in f.readlines():
      if not line.startswith("#"):
	line = line.strip()
	data.append(line.split("\t"))
  f.close()
  
  data = data[1:]
  return data

em_params = {"temp": 950,\
	     "barrier_ht": 1.4,\
	     "voltage": 0,\
	     "position": 0,\
	     "richardson": 10,\
	     "emissivity": 0.5}

co_params = {"temp": 300,\
	     "barrier_ht": 0.6,\
	     "position": 10,\
	     "richardson": 10,\
	     "emissivity": 0.5}
	     
input_params = {"Emitter":em_params, "Collector":co_params}

data = get_data()

# The following block was copied directly from jrsssl000059.dat as a guide to what data is contained in each column.
#                 col 1: voltage (abscissa) [V]
#                 col 2: current density (ordinate) [A/cm^2]
#                 col 3: power density (ordinate) [W/cm^2]
#                 col 4: emitter dimensionless motive (ordinate)
#                 col 5: emitter dimensionless distance (ordinate)
#                 col 6: collector dimensionless motive (ordinate)
#                 col 7: collector dimensionless distance (ordinate)
#                 col 8: efficiency (electrons + photons)

reformatted_data_list = []
for dat in data:
  params = copy.deepcopy(input_params)
  
  # I am following the description of the data found above.
  params["Collector"]["voltage"] = float(dat[0])
  params["output_current_density"] = float(dat[1])
  # I ignore item 2 because its just the product of items 0 and 1.
  params["Emitter"]["dimensionless_motive"] = float(dat[3])
  params["Emitter"]["dimensionless_distance"] = float(dat[4])
  params["Collector"]["dimensionless_motive"] = float(dat[5])
  params["Collector"]["dimensionless_distance"] = float(dat[6])
  # I ignore item 7 because I don't care about efficiency at this point.
  
  reformatted_data_list.append(copy.deepcopy(params))
  
pickle.dump(reformatted_data_list, open("TEC_Langmuir_temporary_STANDARD.dat","w"))

  