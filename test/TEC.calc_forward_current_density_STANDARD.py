# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <codecell>

import numpy as np
import pickle

# <codecell>

def calc_special_case(params):
    """
    Calculate nearest special case given a set of params.

    I use an approach similar to what I was using for the 
    Electrode output current density.
    """

    boltzmann = 8.6173324e-5

    if (params["em_barrier_ht"] + params["em_voltage"]) > \
      (params["co_barrier_ht"] + params["co_voltage"]):
        psi_m = params["em_barrier_ht"]
    else:
        psi_m = params["co_barrier_ht"] + \
          (params["co_voltage"] - params["em_voltage"])
    
    n = np.round(psi_m / (boltzmann * params["em_temp"]))
    params["em_temp"] = psi_m / (boltzmann * n)
    
    J = (params["em_richardson"] * psi_m**2) / \
      (np.exp(n) * n**2 * boltzmann**2)
        
    # Break off the exponent, round the resulting mantissa, 
    # and put everything back together
    if J > 0:
        exponent = np.floor(np.log10(J))
        J = np.round(J / 10**exponent) * 10**exponent
        
        params["em_richardson"] = (J * np.exp(n) * n**2 * boltzmann**2) / \
          psi_m**2
    
    params["forward_current_density"] = J
    
    
    return params

# <codecell>

def print_results(params):
    """
    Nicely prints the parameters and intermediate quantities.
    """

    boltzmann = 8.6173324e-5

    if (params["em_barrier_ht"] + params["em_voltage"]) > \
      (params["co_barrier_ht"] + params["co_voltage"]):
        psi_m = params["em_barrier_ht"]
    else:
        psi_m = params["co_barrier_ht"] + \
          (params["co_voltage"] - params["em_voltage"])
    
    n = np.round(psi_m / (boltzmann * params["em_temp"]))
    
    print "n = psi_m/(boltzmann * em_temp)"
    print str(n) + " = " + str(psi_m) + "/(" + \
          str(boltzmann) + " * " + str(params["em_temp"]) + ")"
    print "\r"
    print "forward_current_density = (em_richardson * psi_m**2)/" +\
          "\r  (exp(n) * n**2 * boltzmann**2)"
    print str(params["forward_current_density"]) + \
          " = (" + str(params["em_richardson"]) + " * " +\
          str(psi_m) + "**2)/ \\" + \
          "\r  (np.exp(" + str(n) + ") * " + str(n) + "**2 * " + \
          str(boltzmann) + "**2)"
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

#print std
#pickle.dump(std,open("TEC.calc_forward_current_density_STANDARD.dat","w"))

# <codecell>

#srt = sorted(std, key=lambda itm: itm["forward_current_density"])
#for itm in srt:
#    print_results(itm)

