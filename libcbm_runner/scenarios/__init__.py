#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A list of all scenarios classes.
"""

# Built-in modules #

# First party modules #

# Internal modules #
from libcbm_runner.scenarios.historical    import Historical
from libcbm_runner.scenarios.afforestation import Afforestation
from libcbm_runner.scenarios.products      import Products

###############################################################################
# List all scenario classes #
scen_classes = [Historical, Afforestation, Products]
