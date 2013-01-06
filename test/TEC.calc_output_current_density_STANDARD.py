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

# Sort nonsymhfcomp into trivial and not obviously trivial.
nonsymhfcomptrivial = []
nonsymhfcompnontrivial = []
for tecparams in nonsymhfcomp:
	if tecparams["Emitter"]["voltage"] != tecparams["Collector"]["voltage"]:
		nonsymhfcomptrivial.append(copy.deepcopy(tecparams))
	else:
		nonsymhfcompnontrivial.append(copy.deepcopy(tecparams))

# Deal with nonsymhfcomptrivial
eqparams = ["barrier_ht", "voltage"]
for el in tecparams.keys():
    print "==", el, "=="
    for eqparam in eqparams:
        print eqparam, ":", tecparams[el][eqparam] == fcdparams[el][eqparam]

# Deal with nonsymhfcompnontrivial
