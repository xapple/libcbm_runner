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
from plumbing.common import camel_to_snake

# Internal modules #

###############################################################################
class InternalData(object):
    """
    This class will provide access to the data of a simulation as it is
    running as several pandas data frames.
    """

    def __init__(self, parent):
        # Default attributes #
        self.parent = parent
        self.runner = parent
        self.sim    = self.runner.simulation

    def __repr__(self):
        return '%s object code "%s"' % (self.__class__, self.runner.short_name)

    #--------------------------- Special Methods -----------------------------#
    def __getitem__(self, item):
        """Read a dataframe from the `results` attribute."""
        # Load #
        df = getattr(self.sim.results, item).copy()
        # Modify column names #
        df.columns = df.columns.to_series().apply(camel_to_snake)
        # Rename column names #
        df = df.rename(columns = {'input': 'area'})
        # Return #
        return df

    #----------------------------- Properties --------------------------------#
    @property
    def classif_df(self):
        return self.make_classif_df(self.sim.sit.classifier_value_ids,
                                    self['classifiers'])

    #------------------------------- Methods ---------------------------------#
    def load(self, name, with_clfrs=True):
        """
        Loads one of the dataframes that is available from the
        `libcbm_py` simulation and adds information to it.
        """
        # Load from CSV #
        df = self[name]
        # Optionally join classifiers #
        cols = ['identifier', 'timestep']
        if with_clfrs: df = df.merge(self.classif_df, 'left', cols)
        # Return #
        return df

    def make_classif_df(self, vals, clfrs):
        """
        Produces a dataframe useful for joining classifier values to
        other output dataframes. This dataframe looks like this:

                  identifier timestep Status Forest type Region ...
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