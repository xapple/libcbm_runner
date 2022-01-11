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
from plumbing.cache import property_cached

# Internal modules #

###############################################################################
class Silviculture:
    """
    Access to silvicultural information pertaining to a given country.
    This includes the following files:

    * irw_frac_by_dist.csv
    * vol_to_mass_coefs.csv
    * events_templates.csv
    * harvest_factors.csv

    Each is accessed by its own corresponding attribute:

    * `silv.irw_frac`
    * `silv.coefs`
    * `silv.events`
    * `silv.harvest`
    """

    def __init__(self, runner):
        # Default attributes #
        self.runner = runner
        # Shortcuts #
        self.country = self.runner.country

    @property_cached
    def irw_frac(self):
        return IRWFractions(self)

    @property_cached
    def coefs(self):
        return 0

    @property_cached
    def events(self):
        return 0

    @property_cached
    def harvest(self):
        return 0

###############################################################################
class IRWFractions:
    """
    Gives access the industrial roundwood fractions, per disturbance type,
    for the current simulation run.
    """

    def __init__(self, silv):
        # Default attributes #
        self.silv = silv
        # Shortcuts #
        self.runner  = self.silv.runner
        self.country = self.silv.country
        self.combo   = self.runner.combo
        self.code    = self.country.iso2_code
        # Choices made for irw_frac in the current combo #
        self.choices = self.combo.config['irw_frac_by_dist']

    #----------------------------- Properties --------------------------------#
    @property
    def csv_path(self):
        return self.country.orig_data.paths.irw_csv

    @property
    def cols(self):
        return list(self.country.orig_data.classif_names.values()) + \
                    ['disturbance_type']

    @property_cached
    def raw(self):
        return pandas.read_csv(self.csv_path,
                               dtype = {c:'str' for c in self.cols})

    @property_cached
    def df(self):
        """
        This will fail if you call `df` before a simulation is launched,
        because we need the internal SIT classifier and disturbance mapping.
        """
        # Make a consistency check between dist_name and dist_id #
        self.consistency_check()
        # Load #
        df = self.raw.copy()
        # Drop the names which are useless #
        df = df.drop(columns='dist_type_name')
        # Convert the disturbance IDs to the real internal IDs #
        id_to_id = self.runner.simulation.sit.disturbance_id_map
        id_to_id = {v:k for k,v in id_to_id.items()}
        df['disturbance_type'] = df['disturbance_type'].map(id_to_id)
        # Convert the classifier IDs to the real internal IDs #
        all_maps = self.runner.simulation.sit.classifier_value_ids.items()
        for classif_name, str_to_id in all_maps:
            df[classif_name] = df[classif_name].map(str_to_id)
        # Return #
        return df

    #------------------------------- Methods ---------------------------------#
    def consistency_check(self):
        # Get mapping dictionary from ID to full description #
        id_to_name = self.country.orig_data['disturbance_types']
        id_to_name = dict(zip(id_to_name['dist_type_name'],
                              id_to_name['dist_desc_input']))
        # Compare #
        names = self.raw['disturbance_type'].map(id_to_name)
        orig  = self.raw['dist_type_name']
        comp  = orig == names
        # Raise exception #
        if not all(comp):
            msg = "Names don't match IDs in '%s'.\n" % self.csv_path
            msg += str(orig[~comp]) + '' + str(names[~comp])
            raise Exception(msg)

    def get_year(self, year):
        # Case number 1: there is only a single scenario specified #
        if isinstance(self.choices, str): scenario = self.choices
        # Case number 2: the scenarios picked vary according to the year #
        else: scenario = self.choices[year]
        # Retrieve by query #
        df = self.df.query("scenario == '%s'" % scenario)
        # Drop the scenario column #
        df = df.drop(columns='scenario')
        # Check there is data left #
        assert not df.empty
        # Return #
        return df
