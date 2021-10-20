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
class Reference(Combination):
    """
    This combo represents the combination of base, afforestation,
    reforestation and deforestation.
    """

    short_name = 'bard'
    code       = 'bard'

    @property_cached
    def runners(self):
        """
        A dictionary of country codes as keys with a list of runners as
        values.
        """
        return {c.iso2_code: [ReferenceRunner(self, c, 0)]
                for c in self.continent}

###############################################################################
class ReferenceRunner(Runner):
    """
    With this class we are able to sub-class any methods from the parent
    `Runner` class and change their behavior in ways that suit this specific
    combo.
    """

    def modify_input(self):
        pass