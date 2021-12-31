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

    Example use:

        >>> from libcbm_runner.core.continent import continent
        >>> combo = continent.combos['historical']
        >>> r = combo.runners['LU'][-1]
        >>> print(r.input_data.classifiers_list)
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
        # Shortcuts #
        self.orig    = self.runner.country.orig_data
        self.combo   = self.runner.combo
        self.code    = self.runner.country.iso2_code
        self.act_dir = self.orig.paths.activities_dir

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

    def __call__(self, debug=False):
        """
        Create the input data files based on the scenario chosen for each
        different activity in the current combination.
        """
        # Message #
        self.parent.log.info("Preparing input data.")
        # Get the destination #
        csv_dir = self.paths.csv_dir
        csv_dir.remove()
        # The common static files just need to be copied over #
        common = self.orig.paths.common_dir
        common.copy(csv_dir)
        # Create the four dynamic files #
        for input_file in self.orig.files_to_be_generated:
            # The path to the file that we will create #
            out_path = self.paths[input_file]
            # What scenarios choices were made for this input file #
            choices = self.combo.config.get(input_file, {})
            # Initialize #
            result = pandas.DataFrame()
            # Optional debug message #
            msg = "Input file '%s' and combo '%s' for country '%s':"
            params = (input_file, self.combo.short_name, self.code)
            if debug: print(msg % params)
            # Iterate over every activity that is defined #
            for activity in choices:
                # Check it exists #
                if activity not in self.orig.activities:
                    msg = "The activity '%s' is not defined in '%s'."
                    raise FileNotFoundError(msg % (activity, self.act_dir))
                # Get the path to the file we will read #
                in_path = self.act_dir + activity + '/' + input_file + '.csv'
                # Read the file, but it's ok if it is empty or absent #
                try:
                    # We want to keep all values as objects and not floats #
                    df = pandas.read_csv(str(in_path), dtype=str)
                except (FileNotFoundError, pandas.errors.EmptyDataError):
                    continue
                # The scenario chosen for this activity and this input #
                scenario = choices[activity]
                # Filter rows to take only this scenario #
                df = df.query("scenario == '%s'" % scenario)
                # Optional debug message #
                msg = "   * for activity '%s', scenario '%s': %i rows"
                if debug: print(msg % (activity, scenario, len(df)))
                # Append #
                result = result.append(df)
            # Remove the scenario column #
            if not result.empty: result = result.drop(columns=['scenario'])
            # Optional debug messages #
            if debug:
                print("   * result -> %i rows total\n" % len(result))
                print(result.dtypes[0:10], '\n-----------\n')
            # Write output #
            result.to_csv(str(out_path), index=False)
        # Return #
        return csv_dir
