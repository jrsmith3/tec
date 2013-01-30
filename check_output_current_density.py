#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tec_langmuir import TEC_Langmuir
import pickle
import copy

std = pickle.load(open("test/TEC_Langmuir_temporary_STANDARD.dat","r"))

output_current_array = []
motives = []

for data in std:
  TECL = TEC_Langmuir(data)
  
  output_current_array.append([1e4*data["output_current_density"],TECL.calc_output_current_density()])
  motives.append(TECL["motive_data"]["max_motive"])


#input_params = copy.deepcopy(std[0])
#input_params["Collector"]["voltage"] = 0.5

#TECL = TEC_Langmuir(input_params)
#print TECL["motive_data"].keys()
