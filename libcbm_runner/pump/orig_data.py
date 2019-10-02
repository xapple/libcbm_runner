#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #

# Third party modules #

# First party modules #
from autopaths.auto_paths import AutoPaths

# Internal modules #

###############################################################################
class OrigData(object):
    """
    This class will provide access to the original data of a Country
    as several pandas data frames.
    """

    all_paths = """
    /orig/associations.csv
    /orig/csv/
    /orig/csv/yield.csv
    /orig/csv/transitions.csv
    /orig/csv/events.csv
    /orig/csv/inventory.csv
    /orig/csv/classifiers.csv
    /orig/csv/disturbance_types.csv
    /orig/csv/age_classes.csv
    """

    def __init__(self, parent):
        # Default attributes #
        self.parent = parent
        # Directories #
        self.paths = AutoPaths(self.parent.data_dir, self.all_paths)