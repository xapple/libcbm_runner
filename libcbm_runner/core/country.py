#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #

# Third party modules #
import pandas

# First party modules #
from autopaths.dir_path   import DirectoryPath
from autopaths.auto_paths import AutoPaths
from plumbing.cache       import property_cached

# Internal modules #
from libcbm_runner.core.continent      import libcbm_data_dir
from libcbm_runner.launch.associations import Associations
from libcbm_runner.pump.orig_data      import OrigData
from libcbm_runner.pump.aidb           import AIDB

# Country codes #
all_country_codes = libcbm_data_dir + 'common/country_codes.csv'
all_country_codes = pandas.read_csv(str(all_country_codes))

###############################################################################
class Country(object):
    """This object gives access to the data pertaining to one country
    amongst the 26 EU member states we are examining."""

    all_paths = """
    """

    def __repr__(self):
        return '%s object code "%s"' % (self.__class__, self.iso2_code)

    def __init__(self, continent, data_dir=None):
        """Store the data directory paths where everything will start from."""
        # Parent #
        self.continent = continent
        # Main directory #
        self.data_dir = DirectoryPath(data_dir)
        # Automatically access paths based on a string of many subpaths #
        self.paths = AutoPaths(self.data_dir, self.all_paths)
        # Set country codes #
        self.set_codes()

    @property_cached
    def scenarios(self):
        """A dictionary linking scenario names to a list of runners
        that concern only this country."""
        from cbmcfs3_runner.core.continent import continent
        return {n: s.runners[self.iso2_code] for n,s in continent.scenarios.items()}

    @property_cached
    def associations(self):
        """Associations of admin/eco/species/disturbances names between
        the input and the reference."""
        return Associations(self)

    @property_cached
    def aidb(self):
        """Archive Index Database also called cbm_defaults in libcbm"""
        return AIDB(self)

    @property_cached
    def orig_data(self):
        """Access the non-changing original data."""
        return OrigData(self)

    #------------------------------- Methods ---------------------------------#
    def set_codes(self):
        """Update all the country codes for this country.
        Typically the result will look something like this:

         'iso2_code':      'BE',
         'country_num':    255,
         'country_name':   'Belgium',
         'country_m49':    56,
         'country_iso3':   'BEL',
         'nuts_zero_2006': 'BE',
         'nuts_zero_2016': 'BE',
        """
        # The reference ISO2 code #
        self.iso2_code = self.data_dir.name
        # Load name mappings #
        selector = all_country_codes['iso2_code'] == self.iso2_code
        row      = all_country_codes.loc[selector].iloc[0]
        # Store all the country references codes #
        self.country_num  = row['country_code']
        self.country_name = row['country']
        self.country_m49  = row['m49_code']
        self.country_iso3 = row['iso3_code']
        # More crazy codes #
        self.nuts_zero_2006 = row['nuts_zero_2006']
        self.nuts_zero_2016 = row['nuts_zero_2010']
