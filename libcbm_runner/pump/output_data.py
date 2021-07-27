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
    """

    all_paths = """
    /output/csv/
    /output/csv/clasif.csv
    /output/csv/pools.csv
    """

    def __init__(self, parent):
        # Default attributes #
        self.parent = parent
        self.runner = parent
        self.sim    = self.runner.simulation
        # Directories #
        self.paths = AutoPaths(self.parent.data_dir, self.all_paths)

    def __getitem__(self, item):
        return pandas.read_csv(str(self.paths[item]))

    def __setitem__(self, item, df):
        df.to_csv(str(self.paths[item]), index=False, float_format='%g')

    @property
    def clasif(self):
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
        # The classifiers #
        self['clasif'] = self.clasif
        # The pools #
        self['pools'] = self.sim.simulation.results.pools
