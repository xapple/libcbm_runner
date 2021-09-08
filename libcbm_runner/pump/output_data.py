#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #
import pickle

# Third party modules #
import pandas

# First party modules #
from autopaths.auto_paths import AutoPaths

# Internal modules #

###############################################################################
class OutputData(object):
    """
    This class will provide access to the output data of a Runner
    as several pandas data frames.

        >>> print(runner.output.load('pools'))
        >>> print(runner.output.load('flux'))
    """

    all_paths = """
    /output/csv/
    /output/csv/values.pickle
    /output/csv/area.csv.gz
    /output/csv/classifiers.csv.gz
    /output/csv/flux.csv.gz
    /output/csv/params.csv.gz
    /output/csv/pools.csv.gz
    /output/csv/state.csv.gz
    """

    def __init__(self, parent):
        # Default attributes #
        self.parent = parent
        self.runner = parent
        self.sim    = self.runner.simulation
        # Directories #
        self.paths = AutoPaths(self.parent.data_dir, self.all_paths)

    def __repr__(self):
        return '%s object code "%s"' % (self.__class__, self.runner.short_name)

    #--------------------------- Special Methods -----------------------------#
    def __getitem__(self, item):
        """Read any CSV or pickle file with the passed name."""
        # Find the path #
        path = self.paths[item]
        # If it is a CSV #
        if '.csv' in path.name:
            return pandas.read_csv(str(path), compression='gzip')
        # If it is a python object #
        with path.open('rb') as handle: return pickle.load(handle)

    def __setitem__(self, item, df):
        """
        Record a dataframe or python object to disk using the file with the
        passed name.
        """
        # Find the path #
        path = self.paths[item]
        # If it is a DataFrame #
        if isinstance(df, pandas.DataFrame):
            return df.to_csv(str(path),
                             index        = False,
                             float_format = '%g',
                             compression  = 'gzip')
        # If it is a python object #
        with path.open('wb') as handle: return pickle.dump(df, handle)

    #----------------------------- Properties --------------------------------#
    @property
    def classif_df(self):
        return self.runner.internal.make_classif_df(self['values'],
                                                    self['classifiers'])

    #------------------------------- Methods ---------------------------------#
    def save(self):
        """
        Save all the information of interest from the simulation to disk before
        the whole simulation object is removed from memory.
        """
        # Message #
        self.parent.log.info("Saving final simulations results to disk.")
        # The classifier values #
        self['values']      = self.sim.sit.classifier_value_ids
        # All the tables that are within the SimpleNamespace of `sim.results` #
        self['area']        = self.runner.internal['pools']
        self['classifiers'] = self.runner.internal['classifiers']
        self['flux']        = self.runner.internal['flux']
        self['params']      = self.runner.internal['params']
        self['pools']       = self.runner.internal['pools']
        self['state']       = self.runner.internal['state']

    def load(self, name, with_clfrs=True):
        """
        Loads one of the dataframes that was previously saved from the
        `libcbm_py` simulation and adds information to it.
        """
        # Load from CSV #
        df = self[name]
        # Optionally join classifiers #
        cols = ['identifier', 'timestep']
        if with_clfrs:
            # Add classifiers
            df = df.merge(self.classif_df, 'left', cols)
        # Add year if there is a timestep column
        if 'timestep' in df.columns:
            df['year'] = self.runner.country.timestep_to_year(df['timestep'])
        ## Add age class information to merge with inventory
        if 'age' in df.columns:
            df['age_class'] = df.age//10 + 1
            df['age_class'] = 'AGEID' + df.age_class.astype(str)
        ## Return #
        return df
