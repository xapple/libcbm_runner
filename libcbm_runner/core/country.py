#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #

# Third party modules #
import pandas

# First party modules #
from autopaths.dir_path   import DirectoryPath
from plumbing.cache       import property_cached

# Internal modules #
from libcbm_runner                     import libcbm_data_dir
from libcbm_runner.launch.associations import Associations
from libcbm_runner.info.orig_data      import OrigData
from libcbm_runner.info.aidb           import AIDB

# Country codes #
all_country_codes = libcbm_data_dir + 'common/country_codes.csv'
all_country_codes = pandas.read_csv(str(all_country_codes))

# Country reference years #
ref_years = libcbm_data_dir + 'common/reference_years.csv'
ref_years = pandas.read_csv(str(ref_years))

###############################################################################
class Country(object):
    """
    This object gives access to the data pertaining to one country
    amongst the 26 EU member states we are examining.
    """

    def __repr__(self):
        return '%s object code "%s"' % (self.__class__, self.iso2_code)

    def __init__(self, continent, data_dir=None):
        """Store the data directory paths where everything will start from."""
        # Parent #
        self.continent = continent
        # Main directory #
        self.data_dir = DirectoryPath(data_dir)
        # Set country codes #
        self.set_codes()
        # Store the reference years #
        self.set_years()

    #---------------------------- Compositions -------------------------------#
    @property_cached
    def associations(self):
        """
        Associations of admin/eco/species/disturbances names between
        the input and the reference.
        """
        return Associations(self)

    @property_cached
    def aidb(self):
        """Archive Index Database also called `cbm_defaults` in libcbm."""
        return AIDB(self)

    @property_cached
    def orig_data(self):
        """Access to the immutable original data."""
        return OrigData(self)

    @property_cached
    def cbmcfs3_country(self):
        """Access the corresponding country in the `cbmcfs3_runner` module."""
        from cbmcfs3_runner.core.continent import continent as cbm_continent
        return cbm_continent.countries[self.iso2_code]

    #----------------------------- Properties --------------------------------#
    @property_cached
    def combos(self):
        """
        A dictionary linking combo names to a list of runners
        that concern only this country.
        """
        from cbmcfs3_runner.core.continent import continent
        return {n: s.runners[self.iso2_code]
                for n, s in continent.combos.items()}

    #------------------------------- Methods ---------------------------------#
    def set_codes(self):
        """
        Update all the country codes for this country.
        Typically the result will look something like this:

         'iso2_code':      'BE',
         'country_num':     255,
         'country_name':   'Belgium',
         'country_m49':     56,
         'country_iso3':   'BEL',
         'nuts_zero_2006': 'BE',
         'nuts_zero_2016': 'BE',
        """
        # The reference ISO2 code #
        self.iso2_code = self.data_dir.name
        # Load name mappings #
        selector = all_country_codes['iso2_code'] == self.iso2_code
        # Check that we know about this country #
        if not selector.any():
            msg = "The directory '%s' is not a country that is known."
            raise ValueError(msg % self.data_dir)
        # Get the right row #
        row = all_country_codes.loc[selector].iloc[0]
        # Store all the country references codes #
        self.country_num  = row['country_code']
        self.country_name = row['country']
        self.country_m49  = row['m49_code']
        self.country_iso3 = row['iso3_code']
        # More crazy codes #
        self.nuts_zero_2006 = row['nuts_zero_2006']
        self.nuts_zero_2016 = row['nuts_zero_2010']

    def set_years(self):
        """Update all the reference years for this country."""
        # This is the same for all countries #
        self.base_year = 2015
        # This is different for each country.
        # The `inventory_start_year` is the oldest year in the inventory data
        # reported by the national forest inventory.
        row = ref_years.loc[ref_years['country'] == self.iso2_code].iloc[0]
        self.inventory_start_year = row['inv_start_year']

    def timestep_to_year(self, timestep):
        """
        Time step 0 is the output of the makelist (so called "spin-up")
        procedure. It represents the initial state.

        Will convert a Series containing simulation time-steps such as:
           [1, 2, 3, 4, 5]
        to actual corresponding simulation years such as:
           [1990, 1991, 1992, 1993, 1994]
        """
        return timestep + self.inventory_start_year

    def year_to_timestep(self, input_year):
        """
        The reverse operation of `timestep_to_year`.

        Will convert a Series containing years such as:
           [1990, 1991, 1992, 1993, 1994]
        to simulation time-steps such as:
           [1, 2, 3, 4, 5]

        Checking the consistency between the 2 functions:

            >>> from libcbm_runner.core.continent import continent
            >>> country = continent.countries['ZZ']
            >>> year = country.timestep_to_year([1,2])
            >>> country.year_to_timestep(year)
            array([1, 2])
        """
        return input_year - self.inventory_start_year