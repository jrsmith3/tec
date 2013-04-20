# -*- coding: utf-8 -*-
# IPython log file

"""
Generates the standard data for the TEC calc_contact_potential method.
"""

import pickle
std = []

Emitter_barrier = 5.0
Collector_barrier = 5.0

contact_potential = Emitter_barrier - Collector_barrier_ht
contact_potential
#[Out]# 0.0
result = {"Emitter_barrier":Emitter_barrier_ht,"Collector_barrier_ht":Collector_barrier_ht,"contact_potential":contact_potential}
std.append(result)

Collector_barrier = 0.5

contact_potential = Emitter_barrier - Collector_barrier_ht
contact_potential
#[Out]# 4.5
result = {"Emitter_barrier":Emitter_barrier_ht,"Collector_barrier_ht":Collector_barrier_ht,"contact_potential":contact_potential}
std.append(result)

Emitter_barrier = 0.5
Collector_barrier = 5.0

contact_potential = Emitter_barrier - Collector_barrier_ht
contact_potential
#[Out]# -4.5
result = {"Emitter_barrier":Emitter_barrier_ht,"Collector_barrier_ht":Collector_barrier_ht,"contact_potential":contact_potential}
std.append(result)

Collector_barrier = 0.5

contact_potential = Emitter_barrier - Collector_barrier_ht
contact_potential
#[Out]# 0.0
result = {"Emitter_barrier":Emitter_barrier_ht,"Collector_barrier_ht":Collector_barrier_ht,"contact_potential":contact_potential}
std.append(result)

std
#[Out]# [{'Collector_barrier': 5.0,
#[Out]#   'Emitter_barrier': 5.0,
#[Out]#   'contact_potential': 0.0},
#[Out]#  {'Collector_barrier': 0.5,
#[Out]#   'Emitter_barrier': 5.0,
#[Out]#   'contact_potential': 4.5},
#[Out]#  {'Collector_barrier': 5.0,
#[Out]#   'Emitter_barrier': 0.5,
#[Out]#   'contact_potential': -4.5},
#[Out]#  {'Collector_barrier': 0.5,
#[Out]#   'Emitter_barrier': 0.5,
#[Out]#   'contact_potential': 0.0}]

pickle.dump(std, open("TEC.calc_contact_potential_STANDARD.dat","w"))
