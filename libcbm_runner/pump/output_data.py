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
from autopaths.auto_paths import AutoPaths

# Internal modules #

###############################################################################
class OutputData(object):
    """
    This class will provide access to the output data of a Runner
    as several pandas data frames.

    >>> print(runner.output['pools'])
    """

    all_paths = """
    /output/csv/
    /output/csv/clasif_val.csv.gz
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

    def __getitem__(self, item):
        return pandas.read_csv(str(self.paths[item]),
                               compression='gzip')

    def __setitem__(self, item, df):
        df.to_csv(str(self.paths[item]),
                  index        = False,
                  float_format = '%g',
                  compression  = 'gzip')
    @property
    def clasif_val(self):
        # Load #
        result = self.sim.sit.classifier_value_ids
        # Transform #
        result = pandas.DataFrame(result)
        # Return #
        return result

    def save(self):
        """
        Save the information of interest from the simulation to disk before
        the whole simulation object is removed from memory.
        """
        # Message #
        self.parent.log.info("Saving final simulations results to disk.")
        # The classifier values #
        self['clasif_val'] = self.clasif_val
        # All the tables that are within the SimpleNamespace of `sim.results` #
        self['area']        = self.sim.results.pools
        self['classifiers'] = self.sim.results.classifiers
        self['flux']        = self.sim.results.flux
        self['params']      = self.sim.results.params
        self['pools']       = self.sim.results.pools
        self['state']       = self.sim.results.state

