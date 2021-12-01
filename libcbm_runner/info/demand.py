#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

This script loads the demand that originates from the economic model
called "GFTMX". This economic model is not run dymamically, instead it
was run once in the past and the outputs recorded in the `libcbm_data`
repository.

The wood product demand used in the `libcbm_runner` simulations is seen as the
production from the perspective of the economic model.

Usage:

    >>> from libcbm_runner.info.demand import fuelwood, roundwood

Related issues:

* https://gitlab.com/bioeconomy/libcbm/libcbm_runner/-/issues/8
"""

# Built-in modules #

# Third party modules #
import pandas

# First party modules #
from plumbing.cache import property_cached

# Internal modules #
from libcbm_runner import libcbm_data_dir
from libcbm_runner.core.country import all_country_codes

# Constants #
demand_dir = libcbm_data_dir + 'common/gftmx/'

###############################################################################
def wide_to_long(df):
    """Convert a demand dataset to the long format."""
    # List columns for pivot #
    cols = ['faostat_name', 'element', 'unit', 'country']
    # Convert #
    df = pandas.wide_to_long(df,
                             stubnames = 'value',
                             i         = cols,
                             j         = 'year')
    # Reset index #
    df = df.reset_index()
    # Return #
    return df

###############################################################################
class Demand:

    def __init__(self, csv_path):
        self.csv_path = csv_path

    @property_cached
    def raw(self):
        return pandas.read_csv(self.csv_path)

    @property_cached
    def df(self):
        # Load #
        df = self.raw.copy()
        # Wide to long #
        df = wide_to_long(df)
        # Add country codes (remove all unknown countries) #
        country_to_iso2 = all_country_codes[['country', 'iso2_code']]
        df = df.merge(country_to_iso2, on='country')
        # Return #
        return df

###############################################################################
# Make two singletons #
roundwood = Demand(demand_dir + "indroundprod.csv")
fuelwood  = Demand(demand_dir + "fuelprod.csv")