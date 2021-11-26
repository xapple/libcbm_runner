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
from libcbm_runner.info.internal_data import InternalData

###############################################################################
class OutputData(InternalData):
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
    /output/csv/parameters.csv.gz
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

    #--------------------------- Special Methods -----------------------------#
    def __getitem__(self, item):
        """Read any CSV or pickle file with the passed name."""
        # Find the path #
        path = self.paths[item]
        # If it is a CSV #
        if '.csv' in path.name:
            return pandas.read_csv(str(path), compression='gzip')
        # If it is a python pickle file #
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

    #------------------------------- Methods ---------------------------------#
    def save(self):
        """
        Save all the information of interest from the simulation to disk before
        the whole cbm object is removed from memory.
        """
        # Message #
        self.parent.log.info("Saving final simulations results to disk.")
        # The classifier values #
        self['values']      = self.sim.sit.classifier_value_ids
        # All the tables that are within the SimpleNamespace of `sim.results` #
        self['area']        = self.runner.internal['area']
        self['classifiers'] = self.runner.internal['classifiers']
        self['flux']        = self.runner.internal['flux']
        self['parameters']  = self.runner.internal['parameters']
        self['pools']       = self.runner.internal['pools']
        self['state']       = self.runner.internal['state']

