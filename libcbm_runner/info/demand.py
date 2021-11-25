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

The wood prodcut demand used in the `libcbm_runner` simulations is seen as the
production from the perspective of the economic model.

Usage:

    >>> from libcbm_runner.info.demand import fuelwood, roundwood
"""

# Built-in modules #

# Third party modules #
import pandas

# First party modules #

# Internal modules #
from libcbm_runner import libcbm_data_dir

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
roundwood = wide_to_long(pandas.read_csv(demand_dir + "indroundprod.csv"))
fuelwood  = wide_to_long(pandas.read_csv(demand_dir + "fuelprod.csv"))