#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A script to add a ninth classifier to every country in order to separate
the initialization period from the historical period. This is useful for
instance to switch all the yield curves of every species as soon as we hit
the country start year.
"""

# Built-in modules #

# Third party modules #
import pandas
from tqdm import tqdm

# First party modules #
from autopaths.auto_paths import AutoPaths

# Internal modules #
from cbmcfs3_runner.core.continent import continent

###############################################################################
# noinspection DuplicatedCode
class ClassifierAdder(object):
    """
    This class takes many of the CSV files in "export/" and changes them.
    It adds an ninth classifier.

    * The classifier is called "yield_period" (it could be just called period).
    * The values are "init", "cur" for the new classifier (see `timeline.svg`).
    """

    all_paths = """
    /export/classifiers.csv
    /export/disturbance_events.csv
    /export/transition_rules.csv
    /export/yields.csv
    /export/historical_yields.csv
    /export/inventory.csv
    """

    def __init__(self, country):
        # Default attributes #
        self.country = country
        # Automatically access paths based on a string of many subpaths #
        self.paths = AutoPaths(self.country.data_dir, self.all_paths)

    def __call__(self):
        # All files #
        self.mod_classifiers()
        self.mod_events()
        self.mod_rules()
        self.mod_ylds()
        self.mod_hist_ylds()
        self.mod_inv()

    #-------------------------- Every file  -----------------------------------#
    def mod_classifiers(self):
        # The path #
        p = self.paths.classifiers
        # Read into memory #
        df = pandas.read_csv(str(p))
        # Change #
        df.loc[len(df)] = (9, '_CLASSIFIER', 'Simulation period (for yields)')
        df.loc[len(df)] = (9, 'Init', 'Initialization period')
        df.loc[len(df)] = (9, 'Cur', 'Current period')
        # Write back to disk #
        df.to_csv(str(p), index=False, float_format='%g')

    def mod_events(self):
        # The path #
        p = self.paths.events
        # Read into memory #
        df = pandas.read_csv(str(p))
        # Change #
        df.insert(loc=8, column='_9', value='Cur')
        # Write back to disk #
        df.to_csv(str(p), index=False, float_format='%g')

    def mod_rules(self):
        # The path #
        p = self.paths.rules
        # Read into memory #
        df = pandas.read_csv(str(p))
        # Change #
        df.insert(loc=8, column='_9', value='Cur')
        df.insert(loc=23, column='_9.1', value='Cur')
        # Write back to disk #
        df.to_csv(str(p), index=False, float_format='%g')
        # Restore header #
        self.restore_header()

    def mod_ylds(self):
        # The path #
        p = self.paths.yields
        # Read into memory #
        df = pandas.read_csv(str(p))
        # Change #
        df.insert(loc=8, column='_9', value='Cur')
        # Write back to disk #
        df.to_csv(str(p), index=False, float_format='%g')

    def mod_hist_ylds(self):
        # The path #
        p = self.paths.historical_yields
        # Read into memory #
        df = pandas.read_csv(str(p))
        # Change #
        df.insert(loc=8, column='_9', value='Init')
        # Write back to disk #
        df.to_csv(str(p), index=False, float_format='%g')

    def mod_inv(self):
        # The path #
        p = self.paths.inventory
        # Read into memory #
        df = pandas.read_csv(str(p))
        # Change #
        df.insert(loc=8, column='_9', value='Init')
        # Write back to disk #
        df.to_csv(str(p), index=False, float_format='%g')

    #-------------------------- Post-processing -------------------------------#
    def restore_header(self):
        """
        In a pandas dataframe, the column names have to be unique, because
        they are implemented as an index. However in the file
        "transition_rules", column names are repeated. So we have to restore
        these headers afterwards.
        """
        # Read from disk #
        header = self.paths.rules.first
        # Modify #
        header = header.split(',')
        header = [n.replace('.1', '') for n in header]
        header = ','.join(header)
        # Write to disk #
        self.paths.rules.remove_first_line()
        self.paths.rules.prepend(header)

###############################################################################
if __name__ == '__main__':
    adders = [ClassifierAdder(c) for c in continent]
    for adder in tqdm(adders): adder()