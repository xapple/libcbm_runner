#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This scenarios represents a demand that is pre-calculated and is not a function of the
maximum wood supply (no interaction yet with the GFTM model).
"""

# Built-in modules #

# First party modules #
from plumbing.cache import property_cached

# Internal modules #
from libcbm_runner.scenarios.base_scen import Scenario
from libcbm_runner.core.runner import Runner

###############################################################################
class Historical(Scenario):
    short_name = 'historical'

    @property_cached
    def runners(self):
        """A dictionary of country codes as keys with a list of runners as values."""
        result = {c.iso2_code: [Runner(self, c, 0)] for c in self.continent}
        return result

