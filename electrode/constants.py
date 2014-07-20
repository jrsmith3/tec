# -*- coding: utf-8 -*-

"""
Physics constants in SI units. Created similar to astropy's Constants module.
"""
from scipy import constants
from astropy.constants import Constant


def generate_constant(const_symbol, const_name):
    """
    Returns astropy Constant.
    """
    return Constant(const_symbol,
                    const_name,
                    constants.physical_constants[const_name][0],
                    constants.physical_constants[const_name][1],
                    constants.physical_constants[const_name][2],
                    "CODATA 2010",
                    system="si")

m_u = generate_constant("m_u", "atomic mass constant")
N_A = generate_constant("N_A", "Avogadro constant")
k = generate_constant("k", "Boltzmann constant")
G_0 = generate_constant("G_0", "conductance quantum")
epsilon_0 = generate_constant("epsilon_0", "electric constant")
m_e = generate_constant("m_e", "electron mass")
# eV = generate_constant("eV","electron volt")
e = generate_constant("e", "elementary charge")
F = generate_constant("F", "Faraday constant")
alpha = generate_constant("alpha", "fine-structure constant")
# mu_0 = generate_constant("mu_0","magnetic constant")
# Phi_0 = generate_constant("Phi_0","magnetic flux quantum")
# R = generate_constant("R","molar gas constant")
# G = generate_constant("G","Newtonian constant of gravitation")
h = generate_constant("h","Planck constant")
hbar = generate_constant("hbar","Planck constant over 2 pi")
# m_p = generate_constant("m_p","proton mass")
# R_infty = generate_constant("R_infty","Rydberg constant")
# c = generate_constant("c","speed of light in vacuum")
# sigma = generate_constant("sigma","Stefan-Boltzmann constant")
