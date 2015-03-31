# -*- coding: utf-8 -*-
from astropy import units
from tec.utils.units import *

sr90 = {"name": "90Sr",
    "decay_mode": "beta",
    "specific_activity": units.Quantity(5.21e12, "Bq/g"),
    "density": units.Quantity(2.606318802830404, "g/cm3"),
    "beta_energy": units.Quantity(0.546, "MeV"),
    "halflife": units.Quantity(28.79, "year"), }

# name: 147Pm
# specific_activity: 928. Ci/g
# density:
# beta_energy: 0.2 MeV
# halflife: 2.6 year
# decay_mode: beta

# name: 63Ni
# specific_activity:
# density:
# beta_energy:
# halflife: 100.1 year
# decay_mode: beta

# name: 3H
# specific_activity:
# density:
# beta_energy:
# halflife:
# decay_mode: beta
# """