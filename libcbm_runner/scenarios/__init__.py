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
from libcbm_runner.scenarios.afforestation import Afforestation
from libcbm_runner.scenarios.bard_v1       import BardV1
from libcbm_runner.scenarios.historical    import Historical

###############################################################################
# List all scenario classes to be loaded #
scen_classes = [Historical, Afforestation, BardV1]
