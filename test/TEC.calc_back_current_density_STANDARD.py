# -*- coding: utf-8 -*-

"""
Generates the standard data for the TEC calc_back_current_density method.

This script simply renames the fields of the forward current density standard data.
"""

import pickle
import copy

def transpose(fcdparams):
  """
  Transposes data from a set of forward current params to back current params.
  """
  em = copy.deepcopy(fcdparams["Emitter"])
  co = copy.deepcopy(fcdparams["Collector"])
  
  bcdparams = {"Emitter": co, "Collector": em}
  bcdparams["back_current_density"] = fcdparams["forward_current_density"]
  bcdparams["psi_m"] = fcdparams["psi_m"]
  
  return bcdparams

fcd = pickle.load(open("TEC.calc_forward_current_density_STANDARD.dat","r"))
bcd = []

for fcdparams in fcd:
  bcdparams = transpose(fcdparams)
  bcd.append(copy.deepcopy(bcdparams))
  
pickle.dump(bcd,open("TEC.calc_back_current_density_STANDARD.dat","w"))
