#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

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
