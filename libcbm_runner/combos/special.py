#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #

# First party modules #
from plumbing.cache import property_cached

# Internal modules #
from libcbm_runner.combos.base_combo import Combination
from libcbm_runner.cbm.dynamic       import DynamicRunner

###############################################################################
class Special(Combination):
    """
    An example Combination.
    """

    short_name = 'special'

    @property_cached
    def runners(self):
        """
        A dictionary of country codes as keys with a list of runners as
        values.
        """
        return {c.iso2_code: [DynamicRunner(self, c, 0)]
                for c in self.continent}
