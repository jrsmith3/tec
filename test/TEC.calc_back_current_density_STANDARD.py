# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

"""
Generates the standard data for the TEC calc_back_current_density method.

This script was generated from an ipython notebook session.
"""


# <codecell>

import numpy as np
import pickle

# <codecell>

co_richardsons = [0.01,100]
co_barrier_hts = [0.5,5.0]
co_temps = [200,2000]
co_voltages = [-10,10]

em_barrier_hts = [0.5,5.0]
em_voltages = [-10,10]

std = []

# <codecell>

for co_richardson in co_richardsons:
    for co_barrier_ht in co_barrier_hts:
        for co_temp in co_temps:
            for co_voltage in co_voltages:
                for em_barrier_ht in em_barrier_hts:
                    for em_voltage in em_voltages:
                        params = {"co_richardson":co_richardson,
                                  "co_barrier_ht":co_barrier_ht,
                                  "co_temp":co_temp,
                                  "co_voltage":co_voltage,
                                  "em_barrier_ht":em_barrier_ht,
                                  "em_voltage":em_voltage}
                        params = calc_special_case(params)
                        std.append(params)                        

# <codecell>

#pickle.dump(std,open("TEC.calc_back_current_density_STANDARD.dat","w"))

# <codecell>

srt = sorted(std, key=lambda itm: itm["back_current_density"])
for itm in srt:
   print_results(itm)

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
        psi_m = params["em_barrier_ht"] + \
          (params["em_voltage"] - params["co_voltage"])
    else:
        psi_m = params["co_barrier_ht"]
    
    # Adjust the collector temperature to yield an argument for the exponent which is a natural number.
    n = np.round(psi_m / (boltzmann * params["co_temp"]))
    params["co_temp"] = psi_m / (boltzmann * n)
    
    # Adjust the collector Richardson's constant to yield a value of current which is a natrual number.
    back_current_density = (params["co_richardson"] * psi_m**2) / \
      (np.exp(n) * n**2 * boltzmann**2)
        
    # Break off the exponent, round the resulting mantissa, and put everything back together. If the forward current density is 0, the following calculation will yield a value of NaN for the Richardson's constant, so just leave Richardson alone.
    if back_current_density > 0:
        exponent = np.floor(np.log10(back_current_density))
        back_current_density = np.round(back_current_density / 10**exponent) * 10**exponent
        
        params["co_richardson"] = (back_current_density * np.exp(n) * n**2 * boltzmann**2) / \
          psi_m**2
    
    params["back_current_density"] = back_current_density
    params["n"] = n
    params["psi_m"] = psi_m
    
    return params

# <codecell>

def print_results(params):
    """
    Nicely prints the parameters and intermediate quantities.
    """
    
    boltzmann = 8.6173324e-5

    print "n = psi_m/(boltzmann * co_temp)"
    print str(params["n"]) + " = " + str(params["psi_m"]) + "/(" + \
          str(boltzmann) + " * " + str(params["co_temp"]) + ")"
    print "\r"
    print "back_current_density = (co_richardson * psi_m**2)/" +\
          "\r  (exp(n) * n**2 * boltzmann**2)"
    print str(params["back_current_density"]) + \
          " = (" + str(params["co_richardson"]) + " * " +\
          str(params["psi_m"]) + "**2)/ \\" + \
          "\r  (np.exp(" + str(params["n"]) + ") * " + str(params["n"]) + \
          "**2 * " + str(boltzmann) + "**2)"
    print "\r"
        
    print "Collector"
    print " richardson:", params["co_richardson"]
    print " barrier_ht:", params["co_barrier_ht"]
    print " temp:      ", params["co_temp"]
    print " voltage:   ", params["co_voltage"]
    print "Emitter"
    print " barrier_ht:", params["em_barrier_ht"]
    print " voltage:   ", params["em_voltage"]
    print "\r"
    print "back_current_density:", params["back_current_density"]
    print "========================================"
    


