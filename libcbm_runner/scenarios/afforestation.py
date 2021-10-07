#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

    >>> from libcbm_runner.core.continent import continent
    >>> scenario = continent.scenarios['afforestation']
    >>> runner   = scenario.runners['LU'][0]
    >>> runner.run()

"""

# Built-in modules #

# First party modules #
from plumbing.cache import property_cached

# Third party modules
import pandas

# Internal modules #
from libcbm_runner.scenarios.base_scen import Scenario
from libcbm_runner.core.runner import Runner

###############################################################################
class Afforestation(Scenario):
    """
    This scenario simulates the additional afforestation scenarios.
    """

    short_name = 'afforestation'
    code       = 'ar'

    @property_cached
    def runners(self):
        """
        A dictionary of country codes as keys with a list of runners as
        values.
        """
        return {c.iso2_code: [AfforestationRunner(self, c, 0)]
                for c in self.continent}

###############################################################################
class AfforestationRunner(Runner):
    """Modification of the runners to enable overwriting the input data."""

    overwrite_csv = ['inventory', 'transitions', 'growth_curves']

    def modify_input(self):
        """
        We would like to overwrite input files with our own specific
        afforestation versions.
        """
        # A scenario always has at least an events file
        # Overwrite the input events file
        # Load the events table
        file_path = self.scen_orig_dir + 'csv/' + 'events_wide_'
        file_path += self.scenario.code + '.csv'
        events_wide = pandas.read_csv(file_path)
        events = self.events_wide_to_long(events_wide)
        events.to_csv(self.input_data.paths.csv_dir + 'events.csv', index=False)
        # Overwrite other input files, only if they are present in the data
        for csv_name in self.overwrite_csv:
            source = self.scen_orig_dir + 'csv/' + csv_name + '_' +\
                     self.scenario.code + '.csv'
            destination = self.input_data.paths.csv_dir + csv_name + '.csv'
            if source.exists: source.copy(destination)
