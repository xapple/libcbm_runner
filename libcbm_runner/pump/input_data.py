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
class InputData(object):
    """
    This class will provide access to the input data of a Runner
    as several pandas data frames.
    """

    all_paths = """
    /input/csv/
    /input/csv/yield.csv
    /input/csv/transitions.csv
    /input/csv/events.csv
    /input/csv/inventory.csv
    /input/csv/classifiers.csv
    /input/csv/disturbance_types.csv
    /input/csv/age_classes.csv
    """

    def __init__(self, parent):
        # Default attributes #
        self.parent = parent
        # Directories #
        self.paths = AutoPaths(self.parent.data_dir, self.all_paths)

    def __getitem__(self, item):
        return pandas.read_csv(str(self.paths[item]))
