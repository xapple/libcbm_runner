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
scenario = continent.scenarios['historical']
runner   = scenario.runners['ZZ'][-1]

runner.run()

