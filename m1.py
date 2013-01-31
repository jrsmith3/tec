#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tec import TEC
import pickle
import copy

std = pickle.load(open("test/TEC_temporary_STANDARD.dat","r"))

output_current_array = []
motives = []

for data in std:
  tec = TEC(data)
  
  output_current_array.append([1e4*data["output_current_density"],tec.calc_forward_current_density()])

#input_params = copy.deepcopy(std[0])
#input_params["Collector"]["voltage"] = 0.5

#tec = TEC_Langmuir(input_params)
#print tec["motive_data"].keys()
