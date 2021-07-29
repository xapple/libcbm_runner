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
    /input/csv/growth_curves.csv
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
        self.runner = parent
        # Directories #
        self.paths = AutoPaths(self.parent.data_dir, self.all_paths)

    def __repr__(self):
        return '%s object code "%s"' % (self.__class__, self.runner.short_name)

    def __getitem__(self, item):
        return pandas.read_csv(str(self.paths[item]))

    #------------------------------- Methods ---------------------------------#
    def copy_orig_from_country(self):
        """
        Refresh the input data by copying the immutable original
        CSVs from the current country to this runner's input.
        """
        # Message #
        self.parent.log.info("Preparing input data.")
        # Get the destination #
        destination_dir = self.paths.csv_dir
        destination_dir.remove()
        # Get the origin #
        origin_dir = self.runner.country.orig_data.paths.csv_dir
        # Copy #
        origin_dir.copy(destination_dir)
