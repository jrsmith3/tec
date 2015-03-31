# -*- coding: utf-8 -*-

"""
Geometric calculations and quantities
"""

import numpy as np
from astropy import units, constants

def sphere_surface_area(radius):
    """
    Surface area of sphere
    """
    area = 4 * np.pi * radius**2
    return area

def sphere_volume(radius):
    """
    Volume of sphere
    """
    vol = (4./3) * np.pi * radius**3
    return vol
