# -*- coding: utf-8 -*-
# IPython log file

"""
Generates the standard data for the TEC calc_interelectrode_spacing method.
"""

import pickle
std = []

Emitter_position = 0
Collector_position = 1

interelectrode_spacing = Collector_position - Emitter_position
interelectrode_spacing
#[Out]# 1
result = {"Emitter_position":Emitter_position, "Collector_position":Collector_position, "interelectrode_spacing":interelectrode_spacing}
std.append(result)

Collector_position = 100

interelectrode_spacing = Collector_position - Emitter_position
interelectrode_spacing
#[Out]# 100
result = {"Emitter_position":Emitter_position, "Collector_position":Collector_position, "interelectrode_spacing":interelectrode_spacing}
std.append(result)

Emitter_position = 10

interelectrode_spacing = Collector_position - Emitter_position
interelectrode_spacing
#[Out]# 90
result = {"Emitter_position":Emitter_position, "Collector_position":Collector_position, "interelectrode_spacing":interelectrode_spacing}
std.append(result)

Emitter_position = 99

interelectrode_spacing = Collector_position - Emitter_position
interelectrode_spacing
#[Out]# 1
result = {"Emitter_position":Emitter_position, "Collector_position":Collector_position, "interelectrode_spacing":interelectrode_spacing}
std.append(result)

std
#[Out]# [{'Collector_position': 1, 'Emitter_position': 0, 'interelectrode_spacing': 1},
#[Out]#  {'Collector_position': 100,
#[Out]#   'Emitter_position': 0,
#[Out]#   'interelectrode_spacing': 100},
#[Out]#  {'Collector_position': 100,
#[Out]#   'Emitter_position': 10,
#[Out]#   'interelectrode_spacing': 90},
#[Out]#  {'Collector_position': 100,
#[Out]#   'Emitter_position': 99,
#[Out]#   'interelectrode_spacing': 1}]

pickle.dump(std, open("TEC.calc_interelectrode_spacing_STANDARD.dat","w"))
