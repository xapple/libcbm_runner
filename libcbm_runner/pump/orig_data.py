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
class OrigData(object):
    """
    This class will provide access to the original data of a Country
    as several pandas data frames.

    This data was taken from the original cbmcfs3 dataset composed by
    Roberto P. and thus depends on the `cbmcfs3_runner` python module
    to be generated.

    To copy all the data from the `cbmcfs3_data` repository do the following:

        >>> from libcbm_runner.core.continent import continent
        >>> for country in continent: country.orig_data.copy_from_cbmcfs3()
    """

    all_paths = """
    /orig/config/associations.csv
    /orig/csv/
    /orig/csv/growth_curves.csv
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
        self.runner = parent
        # Directories #
        self.paths = AutoPaths(self.parent.data_dir, self.all_paths)

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
        Loads one of the dataframes in the orig data and adds information
        to it.
        """
        # Load from CSV #
        df = self[name]
        # Optionally rename classifiers #
        if clfrs_names: df = df.rename(columns=self.classif_names)
        # Return #
        return df

    #----------------------------- Conversions -------------------------------#
    # Define what we will copy #
    orig_files_to_copy = {
        'ageclass':           'age_classes',
        'classifiers':        'classifiers',
        'disturbance_events': 'events',
        'disturbance_types':  'disturbance_types',
        'inventory':          'inventory',
        'transition_rules':   'transitions',
    }

    def copy_from_cbmcfs3(self):
        """
        A method to copy over the data from the cbmcfs3_data repository to the
        libcbm_data repository for this particular country.
        """
        # The two country objects #
        lib_country = self.parent
        cbm_country = self.parent.cbmcfs3_country
        # Check we are pairing countries correctly #
        assert lib_country.iso2_code == cbm_country.iso2_code
        # Main loop #
        for old_name, new_name in self.orig_files_to_copy.items():
            source = cbm_country.orig_data.paths[old_name]
            destin = lib_country.orig_data.paths[new_name]
            source.copy(destin)
        # We also need the 'associations' file #
        source = cbm_country.paths.associations
        destin = lib_country.orig_data.paths.associations
        source.copy(destin)
