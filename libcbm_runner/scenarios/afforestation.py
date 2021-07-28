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

    def modify_input(self):
        pass #TODO
