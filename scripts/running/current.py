#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A script to run the current feature that is being developed and test it.

Typically you would run this file from a command line like this:

     ipython3 -i -- ~/deploy/libcbm_runner/scripts/running/current.py
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
print(runner.simulation.results)
print(runner.simulation.inventory)