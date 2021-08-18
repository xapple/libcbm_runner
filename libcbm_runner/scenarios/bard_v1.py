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
from libcbm_runner.scenarios.base_scen import Scenario
from libcbm_runner.scenarios.afforestation import AfforestationRunner

###############################################################################
class BardV1(Scenario):
    """
    This scenario represents the combination of base, afforestation,
    reforestation and deforestation. Version number 1.
    """

    short_name = 'bard'

    @property_cached
    def runners(self):
        """
        A dictionary of country codes as keys with a list of runners as
        values.
        """
        return {c.iso2_code: [AfforestationRunner(self, c, 0)]
                for c in self.continent}
