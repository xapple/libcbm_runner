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
from libcbm_runner.pump.classifiers import make_classif_df

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
        # Special case for values #
        if item == 'values': return self.sim.sit.classifier_value_ids
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
        return make_classif_df(self['values'], self['classifiers'])

    #------------------------------- Methods ---------------------------------#
    def load(self, name, with_clfrs=True, add_year=True):
        """
        Loads one of the files that was previously saved from the `libcbm_py`
        simulation and adds information to it.
        """
        # Load from CSV #
        df = self[name]
        # Optionally join classifiers #
        if with_clfrs:
            df = df.merge(self.classif_df, 'left', ['identifier', 'timestep'])
        # Add year if there is a timestep column #
        if add_year:
            if 'timestep' in df.columns:
                df['year'] = self.runner.country.timestep_to_year(df['timestep'])
                df = df.drop(columns='timestep')
        # Add age class information to merge with inventory #
        if 'age' in df.columns:
            df['age_class'] = df.age // 10 + 1
            df['age_class'] = 'AGEID' + df.age_class.astype(str)
        # Return #
        return df
