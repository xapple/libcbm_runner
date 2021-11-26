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

# Internal modules #
from libcbm_runner.pump.long_or_wide import events_wide_to_long

###############################################################################
class PreProcessor(object):
    """
    This class will update the input data of a runner based on a set of rules.
    """

    def __init__(self, parent):
        # Default attributes #
        self.parent  = parent
        self.runner  = parent
        self.country = parent.country
        # Shortcuts #
        self.input = self.runner.input_data

    def __repr__(self):
        return '%s object code "%s"' % (self.__class__, self.runner.short_name)

    #--------------------------- Special Methods -----------------------------#
    def __call__(self):
        # Message #
        self.parent.log.info("Pre-processing input data.")
        # Check empty lines in all CSV inputs #
        for csv_path in self.all_csv: self.raise_empty_lines(csv_path)
        # Reshape the events file #
        self.reshape_events()
        # Check there are no negative timesteps #
        self.raise_bad_timestep()

    #----------------------------- Properties --------------------------------#
    @property
    def all_csv(self):
        """Get all CSV inputs in a list."""
        return [item.path_obj for item in self.input.paths._paths
                if item.path_obj.extension == 'csv']

    #------------------------------- Methods ---------------------------------#
    @staticmethod
    def raise_empty_lines(csv_path):
        """
        Loads one CSV files and raise an exception if there are any empty
        lines.
        """
        # Load from disk #
        try: df = pandas.read_csv(str(csv_path))
        # If the file is empty we can skip it #
        except pandas.errors.EmptyDataError: return
        # Get empty lines #
        empty_lines = df.isnull().all(1)
        # Check if there are any #
        if not any(empty_lines): return
        # Warn #
        msg = "The file '%s' has %i empty lines."
        raise Exception(msg % (csv_path, empty_lines.sum()))

    def reshape_events(self, debug=False):
        """Reshape the events file from the wide to the long format."""
        # The events file #
        path = self.input.paths.events
        # Optionally make a copy #
        if debug: path.copy(path.prefix_path + '_wide.csv')
        # Load it as a dataframe #
        wide = pandas.read_csv(str(path))
        # Reshape it #
        long = events_wide_to_long(self.country, wide)
        # Write to disk #
        long.to_csv(str(path), index=False)

    def raise_bad_timestep(self):
        """
        Raise an Exception if there are are timesteps with a value below zero.
        """
        # Path to the file we want to check #
        path = str(self.input.paths.events)
        # Load from disk #
        try: df = pandas.read_csv(path)
        # If the file is empty we can skip it #
        except pandas.errors.EmptyDataError: return
        # Get negative values #
        negative_values = df['step'] < 0
        # Check if there are any #
        if not any(negative_values): return
        # Message #
        msg = "The file '%s' has %i negative values for the timestep column." \
              " This means you are attempting to apply disturbances to a" \
              " year that is anterior to the inventory start year configured."
        # Raise #
        raise Exception(msg % (path, negative_values.sum()))