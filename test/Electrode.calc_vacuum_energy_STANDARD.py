# -*- coding: utf-8 -*-
# IPython log file

"""
Generates the standard data for the Electrode calc_vacuum_energy method.
"""

import numpy as np
import pickle
electron_charge = 1.602176565e-19
std = []

barrier = 0
nea = 0
voltage = 0

vacuum_energy = electron_charge * (voltage + barrier - nea)
vacuum_energy
#[Out]# 0.0
params = {"voltage":voltage, "barrier":barrier_ht, "nea":nea, "vacuum_energy":vacuum_energy}
std.append(params)

voltage = 6.2415093432601795e1

vacuum_energy = electron_charge * (voltage + barrier - nea)
vacuum_energy
#[Out]# 1.0000000000000001e-17
params = {"voltage":voltage, "barrier":barrier_ht, "nea":nea, "vacuum_energy":vacuum_energy}
std.append(params)

nea = 6.2415093432601795e1
voltage = 0

vacuum_energy = electron_charge * (voltage + barrier - nea)
vacuum_energy
#[Out]# -1.0000000000000001e-17
params = {"voltage":voltage, "barrier":barrier_ht, "nea":nea, "vacuum_energy":vacuum_energy}
std.append(params)

voltage = 6.2415093432601795e1

vacuum_energy = electron_charge * (voltage + barrier - nea)
vacuum_energy
#[Out]# 0.0
params = {"voltage":voltage, "barrier":barrier_ht, "nea":nea, "vacuum_energy":vacuum_energy}
std.append(params)

barrier = 6.2415093432601795e1
nea = 0
voltage = 0

vacuum_energy = electron_charge * (voltage + barrier - nea)
vacuum_energy
#[Out]# 1.0000000000000001e-17
params = {"voltage":voltage, "barrier":barrier_ht, "nea":nea, "vacuum_energy":vacuum_energy}
std.append(params)

voltage = 6.2415093432601795e1

vacuum_energy = electron_charge * (voltage + barrier - nea)
vacuum_energy
#[Out]# 2.0000000000000001e-17
params = {"voltage":voltage, "barrier":barrier_ht, "nea":nea, "vacuum_energy":vacuum_energy}
std.append(params)

nea = 6.2415093432601795e1
voltage = 0

vacuum_energy = electron_charge * (voltage + barrier - nea)
vacuum_energy
#[Out]# 0.0
params = {"voltage":voltage, "barrier":barrier_ht, "nea":nea, "vacuum_energy":vacuum_energy}
std.append(params)

voltage = 6.2415093432601795e1

vacuum_energy = electron_charge * (voltage + barrier - nea)
vacuum_energy
#[Out]# 1.0000000000000001e-17
params = {"voltage":voltage, "barrier":barrier_ht, "nea":nea, "vacuum_energy":vacuum_energy}
std.append(params)

std
#[Out]# [{'barrier': 0, 'voltage': 0, 'vacuum_energy': 0.0, 'nea': 0}, {'barrier_ht': 0, 'voltage': 62.415093432601793, 'vacuum_energy': 1.0000000000000001e-17, 'nea': 0}, {'barrier_ht': 0, 'voltage': 0, 'vacuum_energy': -1.0000000000000001e-17, 'nea': 62.415093432601793}, {'barrier_ht': 0, 'voltage': 62.415093432601793, 'vacuum_energy': 0.0, 'nea': 62.415093432601793}, {'barrier_ht': 62.415093432601793, 'voltage': 0, 'vacuum_energy': 1.0000000000000001e-17, 'nea': 0}, {'barrier_ht': 62.415093432601793, 'voltage': 62.415093432601793, 'vacuum_energy': 2.0000000000000001e-17, 'nea': 0}, {'barrier_ht': 62.415093432601793, 'voltage': 0, 'vacuum_energy': 0.0, 'nea': 62.415093432601793}, {'barrier_ht': 62.415093432601793, 'voltage': 62.415093432601793, 'vacuum_energy': 1.0000000000000001e-17, 'nea': 62.415093432601793}]

# Add some dummy data to fill out the rest of the parameters so this data can instantiate an Electrode object without modification.
# Here's some code that should be generalized because otherwise I'm copying it between files.
for params in std:
  params["richardson"] = 0.01
  params["temp"] = 200
  params["position"] = 0
  params["emissivity"] = 0.5

pickle.dump(std, open("Electrode.calc_vacuum_energy_STANDARD.dat","w"))
