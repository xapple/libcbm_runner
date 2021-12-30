#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #

# Third party modules #

# First party modules #
from autopaths.auto_paths import AutoPaths
from plumbing.cache       import property_cached

# Internal modules #
from libcbm_runner import libcbm_data_dir
from libcbm_runner.core.country import Country
from libcbm_runner.combos       import combo_classes

###############################################################################
class Continent(object):
    """
    Entry object to the pipeline.

    Aggregates countries together and enables access to a data frame containing
    concatenated data from all countries at once.
    """

    all_paths = """
    /countries/
    /output/
    """

    def __init__(self, base_dir):
        """
        Store the directory paths where there is a directory for every
        country and for every combo.
        """
        # The base directory #
        self.base_dir = base_dir
        # Automatically access paths based on a string of many subpaths #
        self.paths = AutoPaths(libcbm_data_dir, self.all_paths)
        # Where the input data will be stored #
        self.countries_dir = self.paths.countries_dir
        # Where the output data will be stored #
        self.output_dir = self.paths.output_dir

    def __repr__(self):
        return '%s object with %i countries' % (self.__class__, len(self))

    def __getitem__(self, key):
        """Return a runner based on a tuple of combo, country and step."""
        return self.get_runner(*key)

    def __iter__(self): return iter(self.countries.values())
    def __len__(self):  return len(self.countries.values())

    #----------------------------- Properties --------------------------------#
    @property_cached
    def countries(self):
        """Return a dictionary of country iso2 codes to country objects."""
        all_countries = [Country(self, d)
                         for d in self.countries_dir.flat_directories]
        return {c.iso2_code: c for c in all_countries}

    @property_cached
    def combos(self):
        """Return a dictionary of combination names to Combination objects."""
        all_combos = [combo(self) for combo in combo_classes]
        return {s.short_name: s for s in all_combos}

    #------------------------------- Methods ---------------------------------#
    def get_runner(self, combo, country, step):
        """Return a runner based on combo, country and step."""
        return self.combos[combo].runners[country][step]

###############################################################################
# Create singleton #
continent = Continent(libcbm_data_dir)

