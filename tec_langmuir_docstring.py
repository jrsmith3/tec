# -*- coding: utf-8 -*-

"""
Thermionic engine simulator. Considers space charge, ignores NEA.

dict-like object that implements a model of electron transport including the negative space charge effect. This class explicitly ignores the fact that either electrode may have NEA and determines the vacuum level of an electrode at the barrier. The model is based on [1].

Attributes
----------
The attributes of the object are accessed like a dictionary. The object has three attributes, "Emitter" and "Collector" are both Electrode objects. "motive_data" is a dictionary containing (meta)data calculated during the motive calculation. "motive_data" should usually be accessed via the class's convenience methods. "motive_data" contains the following data:

  motive_array:   A two-element array containing the electrostatic boundary 
                  conditions, i.e. the vacuum level of the emitter and 
                  collector, respectively.
  
  position_array: A two-element array containing the values of position 
                  corresponding to the values in motive_array.
                  
  motive_interp:  A scipy.interpolate.interp1d object that interpolates the 
                  two arrays described above used in the class's convenience 
                  methods.

Parameters
----------
The TEC_Langmuir class is instantiated by a dict with two keys, "Emitter" and "Collector" (case insensitive). Both keys have data that is also of type dict which are configured to instantiate an Electrode object. Additional keys will be ignored and there are no default values for instantiation.

Examples
--------
>>> em_dict = {"temp":1000,
...            "barrier_ht":1,
...            "voltage":0,
...            "position":0,
...            "richardson":10,
...            "emissivity":0.5}
>>> co_dict = {"temp":300,
...            "barrier_ht":0.8,
...            "voltage":0,
...            "position":10,
...            "richardson":10,
...            "emissivity":0.5}
>>> input_dict = {"Emitter":em_dict, "Collector":co_dict}
>>> example_tec = TEC(input_dict)

Notes
-----

Bibliography
------------
[1] 
"""