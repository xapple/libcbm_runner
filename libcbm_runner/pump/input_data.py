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
from plumbing.cache import property_cached

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

    #----------------------------- Properties --------------------------------#
    @property_cached
    def classif_names(self):
        # Load #
        result = self['classifiers']
        # Query #
        result = result.query("classifier_value_id == '_CLASSIFIER'")
        # Get a series #
        result = result.set_index('classifier_number')['name']
        # Link number to name #
        result = {'_' + str(k): v for k,v in result.items()}
        # Return #
        return result

    #------------------------------- Methods ---------------------------------#
    def load(self, name, clfrs_names=True):
        """
        Loads one of the dataframes in the input data and adds information
        to it.
        """
        # Load from CSV #
        df = self[name]
        # Optionally rename classifiers #
        if clfrs_names: df = df.rename(columns=self.classif_names)
        # Return #
        return df

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
