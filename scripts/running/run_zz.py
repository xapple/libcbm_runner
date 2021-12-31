#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

A script to run the imaginary ZZ country to test the pipeline.

Typically you would run this file from a command line like this:

     ipython3 -i -- ~/deploy/libcbm_runner/scripts/running/run_zz.py
"""

# Built-in modules #

# Third party modules #

# First party modules #

# Internal modules #
from libcbm_runner.core.continent import continent

################################################################################
combo  = continent.combos['special']
runner = combo.runners['ZZ'][-1]
runner.num_timesteps = 30
runner.run(keep_in_ram=True, verbose=True, interrupt_on_error=True)

