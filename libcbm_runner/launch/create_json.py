#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #

# Third party modules #
import simplejson as json

# First party modules #
from autopaths.auto_paths import AutoPaths

###############################################################################
class CreateJSON(object):
    """This class will generate the JSON file."""

    template = {
      "output_path": None,
      "import_config": {
        "path":                          None,
        "ageclass_table_name":           "AgeClasses$",
        "classifiers_table_name":        "Classifiers$",
        "disturbance_events_table_name": "DistEvents$",
        "disturbance_types_table_name":  "DistType$",
        "inventory_table_name":          "Inventory$",
        "transition_rules_table_name":   "Transitions$",
        "yield_table_name":              "Growth$"
      },
      "mapping_config": {
        "spatial_units": {
          "mapping_mode":     "SeperateAdminEcoClassifiers",
              # Don't fix the 'Separate' spelling mistake
          "admin_classifier": "Region",
          "eco_classifier":   "Climatic unit",
          "admin_mapping":    None,
          "eco_mapping":      None,
        }
        ,
        "disturbance_types": {
          "disturbance_type_mapping": None,
        },
        "species": {
          "species_classifier": "Forest type",
          "species_mapping":    None,
        },
        "nonforest": None
      }
    }

    def __init__(self, parent):
        # Default attributes #
        self.parent = parent
        self.runner = parent.parent
        # Automatically access paths based on a string of many subpaths #
        self.paths = AutoPaths(self.runner.data_dir, self.parent.all_paths)

    def __call__(self):
        self.paths.json.write(json.dumps(self.content, indent=4, ignore_nan=True))

    @property
    def content(self):
        # Make a copy of the template #
        config = self.template.copy()
        # Two main paths #
        config['output_path']           = self.parent.paths.mdb
        config['import_config']['path'] = self.parent.create_xls.paths.tables_xls
        # Retrieve the four classifiers mappings #
        mappings = self.runner.country.associations.all_mappings
        # Set the four classifiers mappings #
        maps = config['mapping_config']
        maps['spatial_units']['admin_mapping']                = mappings['map_admin_bound']
        maps['spatial_units']['eco_mapping']                  = mappings['map_eco_bound']
        maps['disturbance_types']['disturbance_type_mapping'] = mappings['map_disturbance']
        maps['species']['species_mapping']                    = mappings['map_species']
        # The extra non-forest classifiers #
        if mappings['map_nonforest']:
            maps['nonforest'] = {
                "nonforest_classifier": "Forest type",
                "nonforest_mapping": mappings['map_nonforest']}
        # Return result #
        return config