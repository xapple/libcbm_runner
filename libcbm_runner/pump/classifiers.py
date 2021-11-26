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

# Internal modules #

###############################################################################
def make_classif_df(vals, clfrs):
    """
    Produces a dataframe useful for joining classifier values to
    other output dataframes. This dataframe looks like this:

              identifier timestep status forest_type region ...
        0              1        0    For          OB   LU00 ...
        1              2        0    For          OB   LU00 ...
        2              3        0    For          OB   LU00 ...
    """
    # Invert dictionary #
    vals = {v: k for m in vals.values() for k, v in m.items()}
    # Put actual values such as 'For' instead of numbers like '6' #
    clfrs = clfrs.set_index(['identifier', 'timestep'])
    clfrs = clfrs.replace(vals)
    clfrs = clfrs.reset_index()
    # Return #
    return clfrs