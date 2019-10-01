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
    """This class will generate the JSON file.

    The mapping mode "SeparateAdminEcoClassifiers" is used by
    libcbm/input/sit/sit_mapping.py to assign the spatial unit IDs.
    """

    template = {"import_config": {
        "classifiers":       {"type": "csv", "params": {"path": None}},
        "disturbance_types": {"type": "csv", "params": {"path": None}},
        "age_classes":       {"type": "csv", "params": {"path": None}},
        "inventory":         {"type": "csv", "params": {"path": None}},
        "yield":             {"type": "csv", "params": {"path": None}},
        "events":            {"type": "csv", "params": {"path": None}},
        "transitions":       {"type": "csv", "params": {"path": None}},
      },
      "mapping_config": {
        "spatial_units": {
          "mapping_mode":     "SeparateAdminEcoClassifiers",
          "admin_classifier": "Region",
          "eco_classifier":   "Climatic unit",
          "admin_mapping":    None,
          "eco_mapping":      None,
        },
        "disturbance_types": None,
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