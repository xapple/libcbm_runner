#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #

# Third party modules #
import simplejson as json

# First party modules #

###############################################################################
class CreateJSON(object):
    """
    This class will generate the JSON file consumed by `libcbm`.

    The mapping mode "SeparateAdminEcoClassifiers" is used by
    libcbm/input/sit/sit_mapping.py to assign the spatial unit IDs.
    """

    def __init__(self, parent):
        # Default attributes #
        self.parent = parent
        self.runner = parent

    def __repr__(self):
        return '%s object code "%s"' % (self.__class__, self.runner.short_name)

    def __call__(self):
        self.runner.paths.json.write(json.dumps(self.content,
                                                indent     = 4,
                                                ignore_nan = True))

    template = {
        "import_config": {
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
            }
        }
    }

    @property
    def content(self):
        # Make a copy of the template #
        config = self.template.copy()
        # Get the mapping config sub dictionary #
        maps = config['mapping_config']
        # Retrieve the four classifiers mappings #
        mappings = self.runner.country.associations.all_mappings
        # Set the admin and eco classifiers #
        maps['spatial_units']['admin_mapping'] = mappings['map_admin_bound']
        maps['spatial_units']['eco_mapping']   = mappings['map_eco_bound']
        # Set the disturbances and species classifiers #
        maps['disturbance_types']              = mappings['map_disturbance']
        maps['species']['species_mapping']     = mappings['map_species']
        # Get the names of all the CSVs #
        all_files_names = config['import_config'].keys()
        # Finally set the paths to all the CSVs #
        for file_name in all_files_names:
            name = file_name if file_name != 'yield' else 'growth_curves'
            full_path = self.runner.input_data.paths[name]
            config['import_config'][file_name]['params']['path'] = full_path
        # Return result #
        return config