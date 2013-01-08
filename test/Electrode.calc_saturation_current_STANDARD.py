# -*- coding: utf-8 -*-
# IPython log file (modified from original)

"""
Generates the standard data for the Electrode calc_saturation_current method.
"""

import numpy as np
import pickle
boltzmann = 8.6173324e-5
std = []

barrier_ht = 0.5
temp = 200
richardson = 0.01

barrier_ht/(boltzmann*temp)
#[Out]# 29.011298206391572
n = 29
temp = barrier_ht/(boltzmann*n)
temp
#[Out]# 200.0779186647695
(richardson * barrier_ht**2)/(np.exp(n) * n**2 * boltzmann**2)
#[Out]# 1.0182592095082621e-10
saturation_current = 1e-10
richardson = (1e-10 * np.exp(n) * n**2 * boltzmann**2)/(barrier_ht**2)
richardson
#[Out]# 0.0098206821078782106
# Don't forget to scale the current to A m^{-2}
result = {"barrier_ht": barrier_ht, "temp": temp, "richardson": richardson, \
  "saturation_current": saturation_current * 1e-4, "n": n}
std.append(result)

richardson = 100

(richardson * barrier_ht**2)/(np.exp(n) * n**2 * boltzmann**2)
#[Out]# 1.0182592095082621e-06
saturation_current = 1e-6
richardson = (saturation_current * np.exp(n) * n**2 * boltzmann**2)/(barrier_ht**2)
richardson
#[Out]# 98.206821078782085
# Don't forget to scale the current to A m^{-2}
result = {"barrier_ht": barrier_ht, "temp": temp, "richardson": richardson, \
  "saturation_current": saturation_current * 1e-4, "n": n}
std.append(result)

temp = 2000
richardson = 0.01

barrier_ht/(boltzmann*temp)
#[Out]# 2.9011298206391576
n = 3
temp = barrier_ht/(boltzmann*n)
temp
#[Out]# 1934.0865470927718
(richardson * barrier_ht**2)/(np.exp(n) * n**2 * boltzmann**2)
#[Out]# 1862.3802719093931
saturation_current = 2e3
richardson = (saturation_current * np.exp(n) * n**2 * boltzmann**2)/(barrier_ht**2)
richardson
#[Out]# 0.01073894537096612
# Don't forget to scale the current to A m^{-2}
result = {"barrier_ht": barrier_ht, "temp": temp, "richardson": richardson, \
  "saturation_current": saturation_current * 1e-4, "n": n}
std.append(result)

richardson = 100
(richardson * barrier_ht**2)/(np.exp(n) * n**2 * boltzmann**2)
#[Out]# 18623802.71909393
saturation_current = 2e7
richardson = (saturation_current * np.exp(n) * n**2 * boltzmann**2)/(barrier_ht**2)
richardson
#[Out]# 107.38945370966118
# Don't forget to scale the current to A m^{-2}
result = {"barrier_ht": barrier_ht, "temp": temp, "richardson": richardson, \
  "saturation_current": saturation_current * 1e-4, "n": n}
std.append(result)

barrier_ht = 5.0
temp = 200
richardson = 0.01

barrier_ht/(boltzmann*temp)
#[Out]# 290.11298206391575
n = 290
temp = barrier_ht/(boltzmann*n)
temp
#[Out]# 200.0779186647695
(richardson * barrier_ht**2)/(np.exp(n) * n**2 * boltzmann**2)
#[Out]# 4.5394012190313501e-124
saturation_current = 5e-124
richardson = (saturation_current * np.exp(n) * n**2 * boltzmann**2)/(barrier_ht**2)
richardson
#[Out]# 0.011014668584564848
# Don't forget to scale the current to A m^{-2}
result = {"barrier_ht": barrier_ht, "temp": temp, "richardson": richardson, \
  "saturation_current": saturation_current * 1e-4, "n": n}
std.append(result)

richardson = 100
(richardson * barrier_ht**2)/(np.exp(n) * n**2 * boltzmann**2)
#[Out]# 4.5394012190313504e-120
saturation_current = 5e-120
richardson = (saturation_current * np.exp(n) * n**2 * boltzmann**2)/(barrier_ht**2)
richardson
#[Out]# 110.14668584564851
# Don't forget to scale the current to A m^{-2}
result = {"barrier_ht": barrier_ht, "temp": temp, "richardson": richardson, \
  "saturation_current": saturation_current * 1e-4, "n": n}
std.append(result)

temp = 2000
richardson = 0.01

barrier_ht/(boltzmann*temp)
#[Out]# 29.011298206391576
n = 29
temp = barrier_ht/(boltzmann*n)
temp
#[Out]# 2000.7791866476948
(richardson * barrier_ht**2)/(np.exp(n) * n**2 * boltzmann**2)
#[Out]# 1.0182592095082621e-08
saturation_current = 1e-8
richardson = (saturation_current * np.exp(n) * n**2 * boltzmann**2)/(barrier_ht**2)
richardson
#[Out]# 0.0098206821078782088
# Don't forget to scale the current to A m^{-2}
result = {"barrier_ht": barrier_ht, "temp": temp, "richardson": richardson, \
  "saturation_current": saturation_current * 1e-4, "n": n}
std.append(result)

richardson = 100
(richardson * barrier_ht**2)/(np.exp(n) * n**2 * boltzmann**2)
#[Out]# 0.0001018259209508262
saturation_current = 1e-4
richardson = (saturation_current * np.exp(n) * n**2 * boltzmann**2)/(barrier_ht**2)
richardson
#[Out]# 98.206821078782099
result = {"barrier_ht": barrier_ht, "temp": temp, "richardson": richardson, \
  "saturation_current": saturation_current * 1e-4, "n": n}
std.append(result)

std
#[Out]# [{'barrier_ht': 0.5,
#[Out]#   'n': 29,
#[Out]#   'richardson': 0.0098206821078782106,
#[Out]#   'saturation_current': 1.0000000000000002e-14,
#[Out]#   'temp': 200.0779186647695},
#[Out]#  {'barrier_ht': 0.5,
#[Out]#   'n': 29,
#[Out]#   'richardson': 98.206821078782085,
#[Out]#   'saturation_current': 1e-10,
#[Out]#   'temp': 200.0779186647695},
#[Out]#  {'barrier_ht': 0.5,
#[Out]#   'n': 3,
#[Out]#   'richardson': 0.01073894537096612,
#[Out]#   'saturation_current': 0.20000000000000001,
#[Out]#   'temp': 1934.0865470927718},
#[Out]#  {'barrier_ht': 0.5,
#[Out]#   'n': 3,
#[Out]#   'richardson': 107.38945370966118,
#[Out]#   'saturation_current': 2000.0,
#[Out]#   'temp': 1934.0865470927718},
#[Out]#  {'barrier_ht': 5.0,
#[Out]#   'n': 290,
#[Out]#   'richardson': 0.011014668584564848,
#[Out]#   'saturation_current': 5.0000000000000001e-128,
#[Out]#   'temp': 200.0779186647695},
#[Out]#  {'barrier_ht': 5.0,
#[Out]#   'n': 290,
#[Out]#   'richardson': 110.14668584564851,
#[Out]#   'saturation_current': 5.0000000000000003e-124,
#[Out]#   'temp': 200.0779186647695},
#[Out]#  {'barrier_ht': 5.0,
#[Out]#   'n': 29,
#[Out]#   'richardson': 0.0098206821078782088,
#[Out]#   'saturation_current': 9.9999999999999998e-13,
#[Out]#   'temp': 2000.7791866476948},
#[Out]#  {'barrier_ht': 5.0,
#[Out]#   'n': 29,
#[Out]#   'richardson': 98.206821078782099,
#[Out]#   'saturation_current': 1e-08,
#[Out]#   'temp': 2000.7791866476948}]

# Add some dummy data to fill out the rest of the parameters so this data can instantiate an Electrode object without modification.
# Here's some code that should be generalized because otherwise I'm copying it between files.
for params in std:
  params["position"] = 0
  params["emissivity"] = 0.5
  params["voltage"] = 0

pickle.dump(std, open("Electrode.calc_saturation_current_STANDARD.dat","w"))
