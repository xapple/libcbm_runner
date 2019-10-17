#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #
import os

# Third party modules #

# First party modules #
from autopaths            import Path
from autopaths.auto_paths import AutoPaths
from plumbing.cache       import property_cached

# Where is the data, default case #
libcbm_data_dir = Path("~/deploy/libcbm_data/")

# But you can override that with an environment variable #
if os.environ.get("LIBCBM_DATA"):
    libcbm_data_dir = Path(os.environ['LIBCBM_DATA'])

# Internal modules #
from libcbm_runner.core.country import Country
from libcbm_runner.scenarios    import scen_classes

###############################################################################
class Continent(object):
    """Entry object to the pipeline.

    Aggregates countries together and enables access to a data frame containing
    concatenated data from all countries at once."""

    all_paths = """
    /countries/
    /scenarios/
    """

    def __init__(self, base_dir):
        """Store the directory paths where there is a directory for every
        country and for every scenario."""
        # The base directory #
        self.base_dir = base_dir
        # Automatically access paths based on a string of many subpaths #
        self.paths = AutoPaths(libcbm_data_dir, self.all_paths)
        # Where the data will be stored for this run #
        self.countries_dir = self.paths.countries_dir
        self.scenarios_dir = self.paths.scenarios_dir

    def __getitem__(self, key):
        """Return a runner based on a tuple of scenario, country and step."""
        return self.get_runner(*key)

    def __iter__(self): return iter(self.countries.values())
    def __len__(self):  return len(self.countries.values())

    @property_cached
    def countries(self):
        """Return a dictionary of country iso2 codes to country objects."""
        all_countries = [Country(self, d) for d in self.countries_dir.flat_directories]
        return {c.iso2_code: c for c in all_countries}

    @property_cached
    def scenarios(self):
        """Return a dictionary of scenario names to Scenario objects."""
        all_scenarios = [Scen(self) for Scen in scen_classes]
        return {s.short_name: s for s in all_scenarios}

    #------------------------------- Methods ---------------------------------#
    def get_runner(self, scenario, country, step):
        """Return a runner based on scenario, country and step."""
        return self.scenarios[scenario].runners[country][step]

###############################################################################
# Create singleton #
continent = Continent(libcbm_data_dir)

