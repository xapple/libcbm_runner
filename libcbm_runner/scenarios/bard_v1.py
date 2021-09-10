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
import pandas

###############################################################################
class BardV1(Scenario):
    """
    This scenario represents the combination of base, afforestation,
    reforestation and deforestation. Version number 1.
    """

    short_name = 'bard'
    code = short_name

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
        We would like to append events files to the base scenario with additional details
        afforestation versions.
        We also need to append inventory, growth and transition rules
        """
        # Parameters
        afforestation_sub_scenario = "baseline"
        deforestation_sub_scenario = "baseline"
        # Base events
        file_path = self.country.data_dir + "orig/csv/events.csv"
        events_base = pandas.read_csv(file_path)

        # Afforestation events
        file_path = self.country.data_dir + "afforestation/csv/events_wide_ar.csv"
        events_ar_wide = (pandas.read_csv(file_path)
                          .query(scenario == afforestation_sub_scenario))
        # Keep only one scenario
        events_ar = self.events_wide_to_long(events_ar_wide)

        # Deforestation events
        file_path = self.country.data_dir + "deforestation/csv/events_wide_d.csv"
        events_d_wide = pandas.read_csv(file_path)
        events_d = self.events_wide_to_long(events_d_wide)

        # Concatenate events files
        events = pandas.concat([events_base, events_ar, events_d])

        # Write to csv
        events.to_csv(self.input_data.paths.csv_dir + 'events.csv', index=False)
        # Append to the base file
        for csv_name in self.overwrite_csv:
            source = self.scen_orig_dir + 'csv/' + csv_name + '_' +\
                     self.scenario.code + '.csv'
            destination = self.input_data.paths.csv_dir + csv_name + '.csv'
            if source.exists: source.copy(destination)
