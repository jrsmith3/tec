# -*- coding: utf-8 -*-
# IPython log file

"""
Generates the standard data for the Electrode calc_vacuum_energy method.
"""

import numpy as np
import pickle
e_chrg = 1.602176565e-19
std = []

barrier_ht = 0
nea = 0
voltage = 0

e_vac = e_chrg * (voltage + barrier_ht - nea)
e_vac
#[Out]# 0.0
result = {"voltage":voltage, "barrier_ht":barrier_ht, "nea":nea, "e_vac":e_vac}
std.append(result)

voltage = 6.2415093432601795e1

e_vac = e_chrg * (voltage + barrier_ht - nea)
e_vac
#[Out]# 1.0000000000000001e-17
result = {"voltage":voltage, "barrier_ht":barrier_ht, "nea":nea, "e_vac":e_vac}
std.append(result)

nea = 6.2415093432601795e1
voltage = 0

e_vac = e_chrg * (voltage + barrier_ht - nea)
e_vac
#[Out]# -1.0000000000000001e-17
result = {"voltage":voltage, "barrier_ht":barrier_ht, "nea":nea, "e_vac":e_vac}
std.append(result)

voltage = 6.2415093432601795e1

e_vac = e_chrg * (voltage + barrier_ht - nea)
e_vac
#[Out]# 0.0
result = {"voltage":voltage, "barrier_ht":barrier_ht, "nea":nea, "e_vac":e_vac}
std.append(result)

barrier_ht = 6.2415093432601795e1
nea = 0
voltage = 0

e_vac = e_chrg * (voltage + barrier_ht - nea)
e_vac
#[Out]# 1.0000000000000001e-17
result = {"voltage":voltage, "barrier_ht":barrier_ht, "nea":nea, "e_vac":e_vac}
std.append(result)

voltage = 6.2415093432601795e1

e_vac = e_chrg * (voltage + barrier_ht - nea)
e_vac
#[Out]# 2.0000000000000001e-17
result = {"voltage":voltage, "barrier_ht":barrier_ht, "nea":nea, "e_vac":e_vac}
std.append(result)

nea = 6.2415093432601795e1
voltage = 0

e_vac = e_chrg * (voltage + barrier_ht - nea)
e_vac
#[Out]# 0.0
result = {"voltage":voltage, "barrier_ht":barrier_ht, "nea":nea, "e_vac":e_vac}
std.append(result)

voltage = 6.2415093432601795e1

e_vac = e_chrg * (voltage + barrier_ht - nea)
e_vac
#[Out]# 1.0000000000000001e-17
result = {"voltage":voltage, "barrier_ht":barrier_ht, "nea":nea, "e_vac":e_vac}
std.append(result)

std
#[Out]# [{'barrier_ht': 0, 'e_vac': 0.0, 'voltage': 0, 'nea': 0}, {'barrier_ht': 0, 'e_vac': 1.0000000000000001e-17, 'voltage': 62.415093432601793, 'nea': 0}, {'barrier_ht': 0, 'e_vac': -1.0000000000000001e-17, 'voltage': 0, 'nea': 62.415093432601793}, {'barrier_ht': 0, 'e_vac': 0.0, 'voltage': 62.415093432601793, 'nea': 62.415093432601793}, {'barrier_ht': 62.415093432601793, 'e_vac': 1.0000000000000001e-17, 'voltage': 0, 'nea': 0}, {'barrier_ht': 62.415093432601793, 'e_vac': 2.0000000000000001e-17, 'voltage': 62.415093432601793, 'nea': 0}, {'barrier_ht': 62.415093432601793, 'e_vac': 0.0, 'voltage': 0, 'nea': 62.415093432601793}, {'barrier_ht': 62.415093432601793, 'e_vac': 1.0000000000000001e-17, 'voltage': 62.415093432601793, 'nea': 62.415093432601793}]

pickle.dump(std, open("Electrode.calc_vacuum_energy_STANDARD.dat","w"))
