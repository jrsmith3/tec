# -*- coding: utf-8 -*-
# IPython log file

"""
Generates the standard data for the TEC calc_interelectrode_spacing method.
"""

import pickle
import copy

std = []

em = {"position": 0}
co = {"position": 1}

params = {"Emitter": copy.deepcopy(em), "Collector": copy.deepcopy(co)}

params["interelectrode_spacing"] = params["Collector"]["position"] - params["Emitter"]["position"]
params["interelectrode_spacing"]
#[Out]# 1
std.append(copy.deepcopy(params))

params["Collector"]["position"] = 100

params["interelectrode_spacing"] = params["Collector"]["position"] - params["Emitter"]["position"]
params["interelectrode_spacing"]
#[Out]# 100
std.append(copy.deepcopy(params))

params["Emitter"]["position"] = 10

params["interelectrode_spacing"] = params["Collector"]["position"] - params["Emitter"]["position"]
params["interelectrode_spacing"]
#[Out]# 90
std.append(copy.deepcopy(params))

params["Emitter"]["position"] = 99

params["interelectrode_spacing"] = params["Collector"]["position"] - params["Emitter"]["position"]
params["interelectrode_spacing"]
#[Out]# 1
std.append(copy.deepcopy(params))

std
#[Out]# [{'interelectrode_spacing': 1, 'Collector': {'position': 1}, 'Emitter': {'position': 0}}, {'interelectrode_spacing': 100, 'Collector': {'position': 100}, 'Emitter': {'position': 0}}, {'interelectrode_spacing': 90, 'Collector': {'position': 100}, 'Emitter': {'position': 10}}, {'interelectrode_spacing': 1, 'Collector': {'position': 100}, 'Emitter': {'position': 99}}]

# Add some dummy data to fill out the rest of the parameters so this data can instantiate a TEC object without modification.
# Here's some code that should be generalized because otherwise I'm copying it between files.
for params in std:
  for el in ["Emitter", "Collector"]:
    params[el]["richardson"] = 0.01
    params[el]["temp"] = 200
    params[el]["barrier_ht"] = 0.5
    params[el]["voltage"] = 0
    params[el]["emissivity"] = 0.5

pickle.dump(std, open("TEC.calc_interelectrode_spacing_STANDARD.dat","w"))
