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
from plumbing.cache import property_cached

# Internal modules #

###############################################################################
class Associations(object):
    """
    This class parses the file "associations.csv" and returns
    a dictionary useful to produce the JSON for consumption by SIT.
    """

    keys = ['MapAdminBoundary', 'MapEcoBoundary', 'MapSpecies',
            'MapDisturbanceType', 'MapNonForestType']

    def __init__(self, parent):
        # Default attributes #
        self.parent = parent
        # The associations.csv file path #
        self.path = self.parent.paths.associations

    @property_cached
    def df(self):
        """Load the CSV that is 'associations.csv'."""
        return pandas.read_csv(str(self.path))

    def key_to_rows(self, mapping_name):
        """
        Here is an example call:

        >>> self.key_to_rows('MapDisturbanceType')
        {'10% commercial thinning': '10% Commercial thinning',
         'Deforestation': 'Deforestation',
         'Fire': 'Wild Fire',
         'Generic 15%': 'generic 15% mortality',
         'Generic 20%': 'generic 20% mortality',
         'Generic 30%': 'generic 30% mortality',
         'Spruce Beetle 2% mortality (Ice sleet)': 'Spruce Beetle 2% mortality'}
        """
        query   = "A == '%s'" % mapping_name
        mapping = self.df.query(query).set_index('B')['C'].to_dict()
        return mapping

    def rows_to_list(self, mapping_name, user, default):
        """Create a list string by picking the appropriate rows in the CSV file.

        Here is an example call:

        >>> self.key_to_rows('MapSpecies', 'user_species', 'default_species')
        {...}
        """
        return [{user:k, default:v} for k,v in self.key_to_rows(mapping_name).items()]

    @property_cached
    def all_mappings(self):
        """Return a dictionary for creation of the JSON file."""
        return {
           'map_admin_bound': self.rows_to_list(self.keys[0],
                                                'user_admin_boundary',
                                                'default_admin_boundary'),
           'map_eco_bound':   self.rows_to_list(self.keys[1],
                                                'user_eco_boundary',
                                                'default_eco_boundary'),
           'map_species':     self.rows_to_list(self.keys[2],
                                                'user_species',
                                                'default_species'),
           'map_disturbance': self.rows_to_list(self.keys[3],
                                                'user_dist_type',
                                                'default_dist_type'),
           'map_nonforest':   self.rows_to_list(self.keys[4],        # Not always present
                                                'user_nonforest_type',
                                                'default_nonforest_type'),
        }

