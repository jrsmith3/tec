# -*- coding: utf-8 -*-

"""
Generates the standard data for the TEC calc_forward_current_density method.
"""

import numpy as np
import pickle
import copy

def calc_special_case(params):
    """
    Calculate nearest special case; adjust and return params and intermediates.

    The approach is similar to what was used for the Electrode output current density.
    """

    boltzmann = 8.6173324e-5
    
    # Ignore the negative space charge effect and determine the maximum motive.    
    if (params["Emitter"]["barrier_ht"] + params["Emitter"]["voltage"]) > \
      (params["Collector"]["barrier_ht"] + params["Collector"]["voltage"]):
        psi_m = params["Emitter"]["barrier_ht"]
    else:
        psi_m = params["Collector"]["barrier_ht"] + \
          (params["Collector"]["voltage"] - params["Emitter"]["voltage"])
    
    # Adjust the emitter temperature to yield an argument for the exponent which is a natural number.
    n = np.round(psi_m / (boltzmann * params["Emitter"]["temp"]))
    params["Emitter"]["temp"] = psi_m / (boltzmann * n)
    
    # Adjust the emitter Richardson's constant to yield a value of current which is a natrual number.
    forward_current_density = (params["Emitter"]["richardson"] * psi_m**2) / \
      (np.exp(n) * n**2 * boltzmann**2)
        
    # Break off the exponent, round the resulting mantissa, and put everything back together. If the forward current density is 0, the following calculation will yield a value of NaN for the Richardson's constant, so just leave Richardson alone.
    if forward_current_density > 0:
        exponent = np.floor(np.log10(forward_current_density))
        forward_current_density = np.round(forward_current_density / 10**exponent) * 10**exponent
        
        params["Emitter"]["richardson"] = (forward_current_density * np.exp(n) * n**2 * boltzmann**2) / \
          psi_m**2
    
    params["forward_current_density"] = forward_current_density
    params["Emitter"]["n"] = n
    params["psi_m"] = psi_m
    
    return params

def print_results(params):
    """
    Nicely prints the parameters and intermediate quantities.
    """
    
    boltzmann = 8.6173324e-5

    print "n = psi_m/(boltzmann * em_temp)"
    print str(params["Emitter"]["n"]) + " = " + str(params["psi_m"]) + "/(" + \
          str(boltzmann) + " * " + str(params["Emitter"]["temp"]) + ")"
    print "\r"
    print "forward_current_density = (em_richardson * psi_m**2)/" +\
          "\r  (exp(n) * n**2 * boltzmann**2)"
    print str(params["forward_current_density"]) + \
          " = (" + str(params["Emitter"]["richardson"]) + " * " +\
          str(params["psi_m"]) + "**2)/ \\" + \
          "\r  (np.exp(" + str(params["Emitter"]["n"]) + ") * " + str(params["Emitter"]["n"]) + \
          "**2 * " + str(boltzmann) + "**2)"
    print "\r"
        
    print "Emitter"
    print " richardson:", params["Emitter"]["richardson"]
    print " barrier_ht:", params["Emitter"]["barrier_ht"]
    print " temp:      ", params["Emitter"]["temp"]
    print " voltage:   ", params["Emitter"]["voltage"]
    print "Collector"
    print " barrier_ht:", params["Collector"]["barrier_ht"]
    print " voltage:   ", params["Collector"]["voltage"]
    print "\r"
    print "forward_current_density:", params["forward_current_density"]
    print "========================================"
    
richardsons = [0.01,100]
barrier_hts = [0.5,5.0]
temps = [200,2000]
voltages = [-10,10]

std = []

for em_richardson in richardsons:
    for em_barrier_ht in barrier_hts:
        for em_temp in temps:
            for em_voltage in voltages:
                for co_barrier_ht in barrier_hts:
                    for co_voltage in voltages:
                      em = {"richardson": em_richardson,\
                            "temp": em_temp,\
                            "barrier_ht": em_barrier_ht,\
                            "voltage": em_voltage}
                      co = {"barrier_ht": co_barrier_ht,\
                            "voltage": co_voltage}
                      params = {"Emitter": copy.deepcopy(em), "Collector": copy.deepcopy(co)}
                      calc_special_case(params)
                      std.append(copy.deepcopy(params))

pickle.dump(std,open("TEC.calc_forward_current_density_STANDARD.dat","w"))

#srt = sorted(std, key=lambda itm: itm["forward_current_density"])
#for itm in srt:
   #print_results(itm)
