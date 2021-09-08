#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Illustrate the additional input data used in this scenario

    >>> from libcbm_runner.core.continent import continent
    >>> scenario = continent.scenarios['bard']
    >>> r_lu = scenario.runners['LU'][-1]

"""

# Built-in modules #

# First party modules #
from plumbing.cache import property_cached

# Internal modules #
from libcbm_runner.scenarios.base_scen import Scenario
from libcbm_runner.core.runner import Runner

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
        return {c.iso2_code: [BardV1Runner(self, c, 0)]
                for c in self.continent}

class BardV1Runner(Runner):
    """Modification of the runner to enable appending input data"""

    append_csv = ['inventory', 'transitions', 'growth_curves']

    def modify_input(self):
        """
        We would like to append input files to the base scenario with additional details
        afforestation versions.


        """
        # A scenario always has at least an events file
        # Overwrite the input events file
        events = self.events_wide_to_long()
        events.to_csv(self.input_data.paths.csv_dir + 'events.csv', index=False)
        # Append to the base file
        for csv_name in self.overwrite_csv:
            source = self.scen_orig_dir + 'csv/' + csv_name + '_' +\
                     self.scenario.code + '.csv'
            destination = self.input_data.paths.csv_dir + csv_name + '.csv'
            if source.exists: source.copy(destination)
