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
from libcbm_runner.core.runner import Runner

###############################################################################
class Historical(Combination):
    """
    This combo simulates the historical period ranging from
    the <country.start_year> until 2015, but no further.

    It uses the `reference` scenario for all activities.

    This combo represents a demand that is pre-calculated and is not a
    function of the maximum wood supply. There is no interaction yet with the
    GFTM model.
    """

    short_name = 'historical'

    @property_cached
    def runners(self):
        """
        A dictionary of country codes as keys with a list of runners as
        values.
        """
        return {c.iso2_code: [HistoricalRunner(self, c, 0)]
                for c in self.continent}

###############################################################################
class HistoricalRunner(Runner):
    """
    Like a normal runner, but we redefine the num_timesteps property.
    """

    @property_cached
    def num_timesteps(self):
        """
        Compute the number of years we have to run the simulation for.
        Print all resulting years for each country:

            >>> from libcbm_runner.core.continent import continent
            >>> combo = continent.combos['historical']
            >>> for code, steps in combo.runners.items():
            >>>     r = steps[-1]
            >>>     print(code, ': ', r.num_timesteps)
        """
        # Retrieve parameters that are country specific #
        base_year      = self.country.base_year
        inv_start_year = self.country.inventory_start_year
        # Compute the number of years to simulate #
        period_max     = base_year - inv_start_year + 1
        # Return #
        return period_max
