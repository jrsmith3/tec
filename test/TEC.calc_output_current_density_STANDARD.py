# -*- coding: utf-8 -*-

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

	em = tecparams["Emitter"].copy()
	co = tecparams["Collector"].copy()

	outparams = {"Emitter": co.copy(), "Collector": em.copy()}

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
				electrodes.append(electrode.copy())

for emitter in electrodes:
	for collector in electrodes:
		std.append({"Emitter": emitter.copy(), "Collector": collector.copy()})

# Buckets for the symmetric entries and non-symmetric, half-complementary entries.
sym = []
nonsymhfcomp = []

for tecparams in std:
	if issymmetric(tecparams):
		sym.append(tecparams.copy())
	elif complement(tecparams) not in nonsymhfcomp:
		nonsymhfcomp.append(tecparams.copy())
