# -*- coding: utf-8 -*-
# IPython log file (modified from original)

"""
Generates the standard data for the Electrode calc_saturation_current method.

This script was modified from an ipython session to calculate some special case sets of parameters with outputs. By "special case" I mean the following: a set of parameters which yield a value of output current density that is a single digit (within precision of the calc_saturation_current method) times some power of 10. For example, 2e7. I chose to use the recorded output of an ipython session because I am only testing 8 sets of parameters and it is not that much code to visually parse and check the values by hand if one is so inclined.

The parameters and corresponding output value is collected together in a dict, and appended to a list. At the end of the script, the list is pickled and written to a file for use in the numerical testing strategy described in the README.

The input parameters were chosen to span the range of interesting parameters, given below.

  barrier_ht: [0.5, 5.0]
  temp:       [200, 2000]
  richardson: [0.01, 100]
"""

import numpy as np
import pickle
k = 8.6173324e-5
std = []

phi = 0.5
T = 200
A = 0.01

phi/(k*T)
#[Out]# 29.011298206391572
n = 29
T = phi/(k*n)
T
#[Out]# 200.0779186647695
(A * phi**2)/(np.exp(n) * n**2 * k**2)
#[Out]# 1.0182592095082621e-10
J = 1e-10
A = (1e-10 * np.exp(n) * n**2 * k**2)/(phi**2)
A
#[Out]# 0.0098206821078782106
# Don't forget to scale the current to A m^{-2}
result = {"barrier_ht": phi, "temp": T, "richardson": A, "current": J * 1e-4}
std.append(result)

A = 100

(A * phi**2)/(np.exp(n) * n**2 * k**2)
#[Out]# 1.0182592095082621e-06
J = 1e-6
A = (J * np.exp(n) * n**2 * k**2)/(phi**2)
A
#[Out]# 98.206821078782085
# Don't forget to scale the current to A m^{-2}
result = {"barrier_ht": phi, "temp": T, "richardson": A, "current": J * 1e-4}
std.append(result)

T = 2000
A = 0.01

phi/(k*T)
#[Out]# 2.9011298206391576
n = 3
T = phi/(k*n)
T
#[Out]# 1934.0865470927718
(A * phi**2)/(np.exp(n) * n**2 * k**2)
#[Out]# 1862.3802719093931
J = 2e3
A = (J * np.exp(n) * n**2 * k**2)/(phi**2)
A
#[Out]# 0.01073894537096612
# Don't forget to scale the current to A m^{-2}
result = {"barrier_ht": phi, "temp": T, "richardson": A, "current": J * 1e-4}
std.append(result)

A = 100
(A * phi**2)/(np.exp(n) * n**2 * k**2)
#[Out]# 18623802.71909393
J = 2e7
A = (J * np.exp(n) * n**2 * k**2)/(phi**2)
A
#[Out]# 107.38945370966118
# Don't forget to scale the current to A m^{-2}
result = {"barrier_ht": phi, "temp": T, "richardson": A, "current": J * 1e-4}
std.append(result)

phi = 5.0
T = 200
A = 0.01

phi/(k*T)
#[Out]# 290.11298206391575
n = 290
T = phi/(k*n)
T
#[Out]# 200.0779186647695
(A * phi**2)/(np.exp(n) * n**2 * k**2)
#[Out]# 4.5394012190313501e-124
J = 5e-124
A = (J * np.exp(n) * n**2 * k**2)/(phi**2)
A
#[Out]# 0.011014668584564848
# Don't forget to scale the current to A m^{-2}
result = {"barrier_ht": phi, "temp": T, "richardson": A, "current": J * 1e-4}
std.append(result)

A = 100
(A * phi**2)/(np.exp(n) * n**2 * k**2)
#[Out]# 4.5394012190313504e-120
J = 5e-120
A = (J * np.exp(n) * n**2 * k**2)/(phi**2)
A
#[Out]# 110.14668584564851
# Don't forget to scale the current to A m^{-2}
result = {"barrier_ht": phi, "temp": T, "richardson": A, "current": J * 1e-4}
std.append(result)

T = 2000
A = 0.01

phi/(k*T)
#[Out]# 29.011298206391576
n = 29
T = phi/(k*n)
T
#[Out]# 2000.7791866476948
(A * phi**2)/(np.exp(n) * n**2 * k**2)
#[Out]# 1.0182592095082621e-08
J = 1e-8
A = (J * np.exp(n) * n**2 * k**2)/(phi**2)
A
#[Out]# 0.0098206821078782088
# Don't forget to scale the current to A m^{-2}
result = {"barrier_ht": phi, "temp": T, "richardson": A, "current": J * 1e-4}
std.append(result)

A = 100
(A * phi**2)/(np.exp(n) * n**2 * k**2)
#[Out]# 0.0001018259209508262
J = 1e-4
A = (J * np.exp(n) * n**2 * k**2)/(phi**2)
A
#[Out]# 98.206821078782099
result = {"barrier_ht": phi, "temp": T, "richardson": A, "current": J * 1e-4}
std.append(result)

std
#[Out]# [{'current': 1.0000000000000002e-14, 'richardson': 0.0098206821078782106, 'barrier_ht': 0.5, 'temp': 200.0779186647695}, {'current': 1e-10, 'richardson': 98.206821078782085, 'barrier_ht': 0.5, 'temp': 200.0779186647695}, {'current': 0.20000000000000001, 'richardson': 0.01073894537096612, 'barrier_ht': 0.5, 'temp': 1934.0865470927718}, {'current': 2000.0, 'richardson': 107.38945370966118, 'barrier_ht': 0.5, 'temp': 1934.0865470927718}, {'current': 5.0000000000000001e-128, 'richardson': 0.011014668584564848, 'barrier_ht': 5.0, 'temp': 200.0779186647695}, {'current': 5.0000000000000003e-124, 'richardson': 110.14668584564851, 'barrier_ht': 5.0, 'temp': 200.0779186647695}, {'current': 9.9999999999999998e-13, 'richardson': 0.0098206821078782088, 'barrier_ht': 5.0, 'temp': 2000.7791866476948}, {'current': 1e-08, 'richardson': 98.206821078782099, 'barrier_ht': 5.0, 'temp': 2000.7791866476948}]
pickle.dump(std, open("Electrode.calc_saturation_current_STANDARD.dat","w"))
