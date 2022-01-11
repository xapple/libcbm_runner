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
from plumbing.cache import property_cached

# Internal modules #
from libcbm_runner.pump.long_or_wide import events_wide_to_long

###############################################################################
class OrigData(object):
    """
    This class will provide access to the original data of a Country
    as several pandas data frames.

    The data content itself for the historical period was taken from the
    original `cbmcfs3` dataset composed by Roberto P.

    To copy all the data from the `cbmcfs3_data` repository do the following:

        >>> from libcbm_runner.core.continent import continent
        >>> for country in continent: country.orig_data.copy_from_cbmcfs3()

    This was done at some point before the data was reorganized and changed
    by Viorel B. It can still be seen in `f42fb77` and it depends on the
    `cbmcfs3_runner` python module to be run.
    """

    all_paths = """
    /config/associations.csv               # Static
    /common/age_classes.csv                # Static
    /common/classifiers.csv                # Static
    /common/disturbance_types.csv          # Static
    /silv/irw_frac_by_dist.csv             # Has scenario column
    /silv/vol_to_mass_coefs.csv            # Has scenario column
    /silv/events_templates.csv             # Has scenario column
    /silv/harvest_factors.csv              # Has scenario column
    /activities/                           # Dynamic
    """

    # These files are not listed in the paths above because they depend on
    # different activities.
    files_to_be_generated = ['growth_curves',
                             'transitions',
                             'events',
                             'inventory']

    def __init__(self, parent):
        # Default attributes #
        self.parent  = parent
        self.country = parent
        # Directories #
        self.paths = AutoPaths(self.parent.data_dir, self.all_paths)

    def __getitem__(self, item):
        # A single argument is used for the static files #
        if isinstance(item, str):
            return pandas.read_csv(str(self.paths[item]), dtype=str)
        # Two arguments as a tuple indicates an activity #
        elif len(item) == 2:
            activity, file = item
            path = self.paths.activities_dir + activity + '/' + file + '.csv'
            return pandas.read_csv(str(path), dtype=str)
        # Wrong number of arguments #
        raise Exception("Undefined input data access '%s'." % str(item))

    #----------------------------- Properties --------------------------------#
    @property_cached
    def activities(self):
        """All the activities that exist for the current country."""
        return [d.name for d in self.paths.activities_dir.flat_directories]

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
    def load(self, name, clfrs_names=False, to_long=False):
        """
        Loads one of the dataframes in the orig data and adds information
        to it.
        """
        # Load from CSV #
        df = self[name]
        # Optionally rename classifiers #
        if clfrs_names: df = df.rename(columns=self.classif_names)
        # Optionally convert to the long format #
        if to_long: df = events_wide_to_long(self.country, df)
        # Return #
        return df