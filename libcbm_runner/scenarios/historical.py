#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC biomass Project.
Unit D1 Bioeconomy.

This scenarios represents a demand that is pre-calculated and is not a
function of the maximum wood supply (no interaction yet with the GFTM model).
"""

# Built-in modules #

# First party modules #
from plumbing.cache import property_cached

# Internal modules #
from libcbm_runner.scenarios.base_scen import Scenario
from libcbm_runner.core.runner import Runner

###############################################################################
class Historical(Scenario):
    """
    This scenario simulates the historical period ranging from
    the <country.start_year> until 2015, but no further.
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
    With this class we are able to sub-class any methods from the parent
    `Runner` class and change their behavior in ways that suit this specific
    scenario.
    """

    @property
    def set_num_timesteps(self):
        """
        Compute the number of years we have to run the simulation for.
        Print all resulting years:

            >>> from libcbm_runner.core.continent import continent
            >>> scen = continent.scenarios['historical']
            >>> for code, steps in scen.runners.items():
            >>>     r = steps[0]
            >>>     print(code, ': ', r.set_num_timesteps)
        """
        # Retrieve parameters that are country specific #
        base_year      = self.country.base_year
        inv_start_year = self.country.inventory_start_year
        # Compute the number of years to simulate #
        period_max     = base_year - inv_start_year + 1
        # Return #
        return period_max
