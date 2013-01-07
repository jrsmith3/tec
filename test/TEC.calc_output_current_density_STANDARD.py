# -*- coding: utf-8 -*-
import copy

def issymmetric(tecparams):
	"""
	Determines if the set of tecparams is symmetric.
	"""

	# Iterate over the keys of both sub-dicts to see if they match. 
	# If they don't, the multiplication will eventually up False.
	sym = True
	for key in tecparams["Emitter"].keys():
		sym = sym * (tecparams["Emitter"][key] == tecparams["Collector"][key])

	return sym

def complement(tecparams):
	"""
	Returns the complement of a set of tecparams.
	"""

	em = copy.deepcopy(tecparams["Emitter"])
	co = copy.deepcopy(tecparams["Collector"])

	outparams = {"Emitter": co, "Collector": em}

	if "output_current_density" in tecparams.keys():
		outparams["output_current_density"] = -1 * tecparams["output_current_density"]

	return outparams
	
def compare_params(tecparams, fcdparams):
  """
  Compare a set of tecparams against forward current density standard data.
  
  This method returns a value of True or False. It first method checks the voltage and barrier_ht attributes and ensures they are equal for both electrodes across the two sets of params. Only one of the electrodes in fcdparams will have richardson and temp attributes; this method finds which electrode has them, and compares them against the attributes of the corresponding electrode in tecparams. This comparison is fuzzy; the values have to match within a factor of two to be considered equal.
  """
  iseq = True
  eqparams = ["barrier_ht", "voltage"]
  for el in tecparams.keys():
    for eqparam in eqparams:
      iseq = iseq * (tecparams[el][eqparam] == fcdparams[el][eqparam])
      
  # Figure out which electrode in fcdparams has temp and richardson.
  full_el = find_full_params(fcdparams)
      
  almost_eqparams = ["temp", "richardson"]
  for almost_eqparam in almost_eqparams:
    if (tecparams[full_el][almost_eqparam]/fcdparams[full_el][almost_eqparam] < 2) && \
       (tecparams[full_el][almost_eqparam]/fcdparams[full_el][almost_eqparam] > 0.5):
	 iseq = iseq * True
    else:
      iseq = iseq * False
      
  return iseq
  
def find_full_params(fcdparams):
  """
  Returns the name of the electrode with the full set of parameters.
  
  The forward and back current density standard data consists of a dictionary with two fields, "Emitter" and "Collector", corresponding to the emitter and collector electrode. One of these electrodes does not have the full set of parameters that a typical Electrode object would have. This method returns the name of the electrode that has the full set of parameters an Electrode object should have.
  """
  for el in fcdparams.keys():
    if "temp" in fcdparams[el]:
      return el
	

def merge_params(tecparams, fcdparams):
  """
  Merge a set of forward/back current standard data into a set of tecparams.
  
  This method determines which electrode of forward/back current density standard data is completely filled out; i.e. has attributes for richardson, temp, and current_density. It then overwrites the corresponding electrode in tecparams with this data.
  
  Please note that this method does no comparisons between tecparams and fcdparams, it just clobbers whatever data is in tecparams.
  """
  full_el = find_full_params(fcdparams)
  
  tecparams[full_el] = copy.deepcopy(fcdparams[full_el])

#fcdstd = pickle.load("TEC.calc_forward_current_density_STANDARD.dat")

richardsons = [0.01, 100]
temps = [200, 2000]
barrier_hts = [0.5, 5.0]
voltages = [-10, 10]

electrodes = []
std = []

for richardson in richardsons:
	for temp in temps:
		for barrier_ht in barrier_hts:
			for voltage in voltages:
				electrode = {"richardson": richardson, \
							 "temp": temp, \
							 "barrier_ht": barrier_ht, \
							 "voltage": voltage}
				electrodes.append(electrode)

for emitter in electrodes:
	for collector in electrodes:
		std.append({"Emitter": copy.deepcopy(emitter), \
					"Collector": copy.deepcopy(collector)})

# Buckets for the symmetric entries and non-symmetric, half-complementary entries.
sym = []
nonsymhfcomp = []

for tecparams in std:
	if issymmetric(tecparams):
		sym.append(copy.deepcopy(tecparams))
	elif complement(tecparams) not in nonsymhfcomp:
		nonsymhfcomp.append(copy.deepcopy(tecparams))

# Deal with the symmetric trivial cases
symtrivial = []
for tecparams in sym:
	trivparams = copy.deepcopy(tecparams)
	trivparams["output_current_density"] = 0.
	symtrivial.append(trivparams)
	
# Perturb symmetric cases

# Fill out data for each set of params in nonsymhfcomp using data from the forward current density standard data.
for tecparams in nonsymhfcomp:
  for fcdparams in fcdstd:
    if compare_params(tecparams, fcdparams):
      merge_params(tecparams, fcdparams)
    elif compare_params(tecparams, complement(fcdparams)):
      merge_params(tecparams, complement(fcdparams))

# Sort nonsymhfcomp into trivial and not obviously trivial.
nonsymhfcomptrivial = []
nonsymhfcompnontrivial = []
for tecparams in nonsymhfcomp:
	if tecparams["Emitter"]["voltage"] != tecparams["Collector"]["voltage"]:
		nonsymhfcomptrivial.append(copy.deepcopy(tecparams))
	else:
		nonsymhfcompnontrivial.append(copy.deepcopy(tecparams))

# Deal with nonsymhfcomptrivial

# Deal with nonsymhfcompnontrivial
