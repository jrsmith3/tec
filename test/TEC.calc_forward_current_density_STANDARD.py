# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

"""
Generates the standard data for the TEC calc_forward_current_density method.

This script was generated from an ipython notebook session.
"""

# <codecell>

import numpy as np
import pickle

# <codecell>

def calc_special_case(params):
    """
    Calculate nearest special case; adjust and return params and intermediates.

    The approach is similar to what was used for the Electrode output current density.
    """

    boltzmann = 8.6173324e-5
    
    # Ignore the negative space charge effect and determine the maximum motive.    
    if (params["em_barrier_ht"] + params["em_voltage"]) > \
      (params["co_barrier_ht"] + params["co_voltage"]):
        psi_m = params["em_barrier_ht"]
    else:
        psi_m = params["co_barrier_ht"] + \
          (params["co_voltage"] - params["em_voltage"])
    
    # Adjust the emitter temperature to yield an argument for the exponent which is a natural number.
    n = np.round(psi_m / (boltzmann * params["em_temp"]))
    params["em_temp"] = psi_m / (boltzmann * n)
    
    # Adjust the emitter Richardson's constant to yield a value of current which is a natrual number.
    forward_current_density = (params["em_richardson"] * psi_m**2) / \
      (np.exp(n) * n**2 * boltzmann**2)
        
    # Break off the exponent, round the resulting mantissa, and put everything back together. If the forward current density is 0, the following calculation will yield a value of NaN for the Richardson's constant, so just leave Richardson alone.
    if forward_current_density > 0:
        exponent = np.floor(np.log10(forward_current_density))
        forward_current_density = np.round(forward_current_density / 10**exponent) * 10**exponent
        
        params["em_richardson"] = (forward_current_density * np.exp(n) * n**2 * boltzmann**2) / \
          psi_m**2
    
    params["forward_current_density"] = forward_current_density
    params["n"] = n
    params["psi_m"] = psi_m
    
    return params

# <codecell>

def print_results(params):
    """
    Nicely prints the parameters and intermediate quantities.
    """
    
    boltzmann = 8.6173324e-5

    print "n = psi_m/(boltzmann * em_temp)"
    print str(params["n"]) + " = " + str(params["psi_m"]) + "/(" + \
          str(boltzmann) + " * " + str(params["em_temp"]) + ")"
    print "\r"
    print "forward_current_density = (em_richardson * psi_m**2)/" +\
          "\r  (exp(n) * n**2 * boltzmann**2)"
    print str(params["forward_current_density"]) + \
          " = (" + str(params["em_richardson"]) + " * " +\
          str(params["psi_m"]) + "**2)/ \\" + \
          "\r  (np.exp(" + str(params["n"]) + ") * " + str(params["n"]) + \
          "**2 * " + str(boltzmann) + "**2)"
    print "\r"
        
    print "Emitter"
    print " richardson:", params["em_richardson"]
    print " barrier_ht:", params["em_barrier_ht"]
    print " temp:      ", params["em_temp"]
    print " voltage:   ", params["em_voltage"]
    print "Collector"
    print " barrier_ht:", params["co_barrier_ht"]
    print " voltage:   ", params["co_voltage"]
    print "\r"
    print "forward_current_density:", params["forward_current_density"]
    print "========================================"
    
# <codecell>

em_richardsons = [0.01,100]
em_barrier_hts = [0.5,5.0]
em_temps = [200,2000]
em_voltages = [-10,10]

co_barrier_hts = [0.5,5.0]
co_voltages = [-10,10]

std = []

# <codecell>

for em_richardson in em_richardsons:
    for em_barrier_ht in em_barrier_hts:
        for em_temp in em_temps:
            for em_voltage in em_voltages:
                for co_barrier_ht in co_barrier_hts:
                    for co_voltage in co_voltages:
                        params = {"em_richardson":em_richardson,
                                  "em_barrier_ht":em_barrier_ht,
                                  "em_temp":em_temp,
                                  "em_voltage":em_voltage,
                                  "co_barrier_ht":co_barrier_ht,
                                  "co_voltage":co_voltage}
                        params = calc_special_case(params)
                        std.append(params)                        

# <codecell>

pickle.dump(std,open("TEC.calc_forward_current_density_STANDARD.dat","w"))

# <codecell>

#srt = sorted(std, key=lambda itm: itm["forward_current_density"])
#for itm in srt:
   #print_results(itm)
