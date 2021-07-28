#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This scenario represents the additional afforestation.


To use this scenario

    from libcbm_runner.core.continent import continent
    scenario = continent.scenarios['afforestation']
    r = scenario.runners['AT'][-1]

    r.run()

"""

# Built-in modules #

# First party modules #
from plumbing.cache import property_cached

# Internal modules #
from libcbm_runner.scenarios.base_scen import Scenario
from libcbm_runner.core.runner import Runner

###############################################################################
class Afforestation(Scenario):
    """
    This scenario simulates additional afforestation scenarios.
    """

    short_name = 'afforestation'

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
    """
    With this class we are able to sub-class any methods from the parent
    `Runner` class and change their behavior in ways that suit this specific
    scenario.
    """

    overwrite_csv = ['events.csv', 'inventory.csv', 'transitions.csv']

    def modify_input(self):
        """
        We would like to overwrite only three files with our own specific
        afforestation versions.
        """
        for csv_name in self.overwrite_csv:
            source = self.scen_orig_dir + 'csv/' + csv_name
            destination = self.input_data.paths.csv_dir + csv_name
            source.copy(destination)
