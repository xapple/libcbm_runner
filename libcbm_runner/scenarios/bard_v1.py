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
from libcbm_runner.core.runner import Runner

###############################################################################
class Bard1(Scenario):
    """
    This scenario represents the combination of base, afforestation,
    reforestation and deforestation. Version number 1.

    To use this scenario:

        >>> from libcbm_runner.core.continent import continent
        >>> scenario = continent.scenarios['ar']
        >>> r = scenario.runners['AT'][-1]
        >>> r.run()

    Check the output pools:

        >>> r.output.load('pools')
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

###############################################################################
class Bard1Runner(Runner):
    #TODO remove duplicated code bellow

    overwrite_csv = ['inventory', 'transitions', 'growth_curves']

    def modify_input(self):
        """
        We would like to overwrite input files with our own specific
        afforestation versions.
        """
        # A scenario always has at least an events file
        # Overwrite the input events file
        events = self.events_wide_to_long()
        events.to_csv(self.input_data.paths.csv_dir + 'events.csv', index=False)

        # Overwrite other input files, only if they are present in the data
        for csv_name in self.overwrite_csv:
            source = self.scen_orig_dir + 'csv/' + csv_name + '_'
            source += self.scenario.abbreviation + '.csv'
            if source.exists:
                destination = self.input_data.paths.csv_dir + csv_name + '.csv'
                source.copy(destination)
            else:
                print(f"Skipping {source} as the file doesn't exist.")
