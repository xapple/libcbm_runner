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
from autopaths.auto_paths import AutoPaths

# Internal modules #

###############################################################################
class InputData:
    """
    This class will provide access to the input data of a Runner
    as several pandas data frames.
    The files listed here are the ones used to create the JSON that is
    consumed by `libcbm`.
    """

    all_paths = """
    /input/csv/
    /input/csv/age_classes.csv         # Static
    /input/csv/classifiers.csv         # Static
    /input/csv/disturbance_types.csv   # Static
    /input/csv/events.csv              # Dynamic based on scenarios picked
    /input/csv/inventory.csv           # Dynamic based on scenarios picked
    /input/csv/transitions.csv         # Dynamic based on scenarios picked
    /input/csv/growth_curves.csv       # Dynamic based on scenarios picked
    """

    def __init__(self, parent):
        # Default attributes #
        self.parent = parent
        self.runner = parent
        # Directories #
        self.paths = AutoPaths(self.parent.data_dir, self.all_paths)

    def __repr__(self):
        return '%s object code "%s"' % (self.__class__, self.runner.short_name)

    def __getitem__(self, item):
        return pandas.read_csv(str(self.paths[item]))

    #------------------------------- Methods ---------------------------------#
    def load(self, name):
        """Loads one of the dataframes."""
        # Load from CSV #
        df = self[name]
        # Return #
        return df

    def __call__(self):
        #TODO
        pass