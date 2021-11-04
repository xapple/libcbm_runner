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
from libcbm_runner.pump.column_order import events_cols

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

    def reshape_events(self, debug=True):
        """Reshape the events file from the wide to the long format"""
        # The events file #
        path = self.input.paths.events
        # Optionally make a copy #
        if debug: path.copy(path.prefix_path + '_wide.csv')
        # Load it as a dataframe #
        wide = pandas.read_csv(str(path))
        # Reshape it #
        long = self.events_wide_to_long(wide)
        # Write to disk #
        long.to_csv(str(path), index=False)

    def raise_bad_timestep(self):
        """
        Raise an Exception if there are are timesteps with a value below 0.
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
        # Warn #
        msg = "The file '%s' has %i negative values for the timestep column." \
              " This means you are attempting to apply disturbances to a" \
              " year that is anterior to the inventory start year configured."
        raise Exception(msg % (path, negative_values.sum()))

    #------------------------ Dataframe conversions --------------------------#
    def events_wide_to_long(self, events):
        """Reshape disturbance events from wide to long format."""
        # Make a copy of the dataframe #
        df = events.copy()
        # We want to pivot on all columns except two #
        skip  = ['step', 'amount']
        cols  = [col for col in events_cols if col not in skip]
        # Reshape from wide to long format #
        df = pandas.wide_to_long(df,
                                 stubnames = "amount",
                                 i         = cols,
                                 j         = "year",
                                 sep       = '_')
        # Drop rows that don't have an amount #
        df = df.dropna()
        # Reset index #
        df = df.reset_index()
        # Convert years to time steps #
        df['step'] = self.country.year_to_timestep(df['year'])
        # Drop the year column #
        df = df.drop(columns=['year'])
        # Reorder columns according to the correct input order #
        df = df[events_cols]
        # Return #
        return df

    def events_long_to_wide(self, events):
        """Reshape disturbance events from long to wide format."""
        # Make a copy of the dataframe #
        df = events.copy()
        # Convert the step to years #
        df['year'] = self.country.timestep_to_year(df['step'])
        # Drop the steps column #
        df = df.drop(columns=['step'])
        # We want to pivot on all columns except two #
        skip_cols = ['step', 'amount']
        cols = [col for col in events_cols if col not in skip_cols]
        # Reshape from long to wide format #
        df = df.pivot(index   = cols,
                      columns = 'year',
                      values  = 'amount')
        # We don't want the columns to be called 'year' though #
        df = df.rename_axis(columns=None)
        # Add 'amount_' in front of every column name #
        df = df.add_prefix('amount_')
        # Remove rows that are all NaNs #
        df = df.dropna(how='all')
        # Reset index #
        df = df.reset_index()
        # Sort entries #
        df = df.sort_values(cols)
        # Add the scenario column #
        df.insert(0, 'scenario', 'reference')
        # Return #
        return df
