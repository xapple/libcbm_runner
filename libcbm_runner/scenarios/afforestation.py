#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This scenario represents the additional afforestation.

To use this scenario

    >>> from libcbm_runner.core.continent import continent
    >>> scenario = continent.scenarios['ar']
    >>> r = scenario.runners['AT'][-1]
    >>> r.run()

Check the output pools

    >>> r.output.load('pools')

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
    """This scenario simulates the additional afforestation scenarios."""

    name = "Afforestation"
    short_name = 'ar'

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

    overwrite_csv = ['inventory', 'transitions', 'growth_curves']

    def modify_input(self):
        """
        We would like to overwrite input files with our own specific
        afforestation versions.
        """
        # Load the events table
        file_path = self.scen_orig_dir + 'csv/' + 'events_wide_'
        file_path += self.scenario.short_name + '.csv'
        events_wide = pandas.read_csv(file_path)

        # Reshape from wide to long format
        events_wide["id"] = events_wide.index
        events = pandas.wide_to_long(events_wide, stubnames="amount ", i="id", j="year")
        events = events.reset_index()

        # Convert years to time steps
        events['step'] = self.country.year_to_timestep(events['year'])
        # Remove the space in the amount column name
        events = events.rename(columns={"amount ": "amount"})
        # Reorder columns according to the reference table in the original data
        colname_order = self.country.orig_data.load('events', clfrs_names=False).columns.tolist()
        events = events[colname_order]

        # Overwrite the input events file
        events.to_csv(self.input_data.paths.csv_dir + 'events.csv', index=False)

        # Overwrite other input files
        for csv_name in self.overwrite_csv:
            source = self.scen_orig_dir + 'csv/' + csv_name + '_' + self.scenario.short_name + '.csv'
            destination = self.input_data.paths.csv_dir + csv_name + '.csv'
            source.copy(destination)
