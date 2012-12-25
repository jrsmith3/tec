# -*- coding: utf-8 -*-
# IPython log file

"""
Generates the standard data for the TEC calc_output_voltage method.
"""


import pickle
std = []

Emitter_voltage = 0
Collector_voltage = 0

output_voltage = Collector_voltage - Emitter_voltage
output_voltage
#[Out]# 0
result = {"Emitter_voltage":Emitter_voltage, "Collector_voltage":Collector_voltage, "output_voltage":output_voltage}
std.append(result)

Collector_voltage = 5

output_voltage = Collector_voltage - Emitter_voltage
output_voltage
#[Out]# 5
result = {"Emitter_voltage":Emitter_voltage, "Collector_voltage":Collector_voltage, "output_voltage":output_voltage}
std.append(result)

Emitter_voltage = 5
Collector_voltage = 0

output_voltage = Collector_voltage - Emitter_voltage
output_voltage
#[Out]# -5
result = {"Emitter_voltage":Emitter_voltage, "Collector_voltage":Collector_voltage, "output_voltage":output_voltage}
std.append(result)

Collector_voltage = 5

output_voltage = Collector_voltage - Emitter_voltage
output_voltage
#[Out]# 0
result = {"Emitter_voltage":Emitter_voltage, "Collector_voltage":Collector_voltage, "output_voltage":output_voltage}
std.append(result)

std
#[Out]# [{'Collector_voltage': 0, 'Emitter_voltage': 0, 'output_voltage': 0},
#[Out]#  {'Collector_voltage': 5, 'Emitter_voltage': 0, 'output_voltage': 5},
#[Out]#  {'Collector_voltage': 0, 'Emitter_voltage': 5, 'output_voltage': -5},
#[Out]#  {'Collector_voltage': 5, 'Emitter_voltage': 5, 'output_voltage': 0}]

pickle.dump(std, open("TEC.calc_output_voltage_STANDARD.dat","w"))
