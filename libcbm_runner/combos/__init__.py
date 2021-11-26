#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

A list of all combo classes.
"""

# Built-in modules #

# First party modules #

# Internal modules #
from libcbm_runner.combos.special      import Special
from libcbm_runner.combos.historical   import Historical
from libcbm_runner.combos.harvest_test import HarvestTest

###############################################################################
# List all combo classes to be loaded #
combo_classes = [Historical, Special, HarvestTest]
