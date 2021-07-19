#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux

JRC biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #

# Third party modules #

# First party modules #
from autopaths            import Path
from autopaths.auto_paths import AutoPaths

# Internal modules #

###############################################################################
class Scenario(object):
    """
    This object represents a harvest and economic scenario.
    Each Scenario subclass must define a list of Runner instances as
    the <self.runners> property.
    """

    all_paths = """
    """

    def __init__(self, continent):
        # Save parent #
        self.continent = continent
        # This scenario dir #
        self.base_dir = Path(self.scenarios_dir + self.short_name + '/')
        # Automatically access paths based on a string of many subpaths #
        self.paths = AutoPaths(self.base_dir, self.all_paths)

    def __repr__(self):
        return '%s object with %i runners' % (self.__class__, len(self))

    def __iter__(self): return iter(self.runners.values())
    def __len__(self):  return len(self.runners.values())

    @property
    def scenarios_dir(self):
        """Shortcut to the scenarios directory."""
        return self.continent.scenarios_dir