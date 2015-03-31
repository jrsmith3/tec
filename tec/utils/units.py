# -*- coding: utf-8 -*-

"""
Units not provided by astropy.units
"""

from astropy import units, constants

Bq = units.def_unit("becquerel",
    1/units.s,
    doc="SI derived unit of radioactivity",
    prefixes=True, )

Ci = units.def_unit("curie",
    3.7e10 * Bq,
    "Common, non-SI unit of radioiactivity",
    prefixes=True, )
