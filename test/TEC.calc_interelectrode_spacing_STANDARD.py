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

pickle.dump(std, open("TEC.calc_interelectrode_spacing_STANDARD.dat","w"))
