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

# Internal modules #
from libcbm_runner.pump.column_order import events_cols

###############################################################################
#------------------------ Dataframe conversions --------------------------#
def events_wide_to_long(country, events):
    """Reshape disturbance events from wide to long format."""
    # Make a copy of the dataframe #
    df = events.copy()
    # We want to pivot on all columns except two #
    skip  = ['step', 'amount']
    cols  = [col for col in events_cols if col not in skip]
    # Reshape from wide to long format #
    try:
        df = pandas.wide_to_long(df,
                                 stubnames = "amount",
                                 i         = cols,
                                 j         = "year",
                                 sep       = '_')
    # Better error message #
    except ValueError as error:
        if 'uniquely identify each row' not in str(error): raise
        msg = "You probably have two or more rows in your events file " \
              "which both have the same classifier values. Hence one " \
              "cannot convert it from wide to long format."
        raise ValueError(msg) from error
    # Drop rows that don't have an amount #
    df = df.dropna()
    # Reset index #
    df = df.reset_index()
    # Convert years to time steps #
    df['step'] = country.year_to_timestep(df['year'])
    # Drop the year column #
    df = df.drop(columns=['year'])
    # Reorder columns according to the correct input order #
    df = df[events_cols]
    # Return #
    return df

def events_long_to_wide(country, events):
    """Reshape disturbance events from long to wide format."""
    # Make a copy of the dataframe #
    df = events.copy()
    # Convert the step to years #
    df['year'] = country.timestep_to_year(df['step'])
    # Drop the steps column #
    df = df.drop(columns=['step'])
    # We want to pivot on all columns except two #
    skip_cols = ['step', 'amount']
    cols = [col for col in events_cols if col not in skip_cols]
    # Reshape from long to wide format #
    df = df.pivot(index   = cols,
                  columns = 'year',
                  values  = 'amount')
    # We don't want the columns to be called 'year' though #
    df = df.rename_axis(columns=None)
    # Add 'amount_' in front of every column name #
    df = df.add_prefix('amount_')
    # Remove rows that are all NaNs #
    df = df.dropna(how='all')
    # Reset index #
    df = df.reset_index()
    # Sort entries #
    df = df.sort_values(cols)
    # Add the scenario column #
    df.insert(0, 'scenario', 'reference')
    # Return #
    return df
