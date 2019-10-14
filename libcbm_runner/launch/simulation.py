#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #

# Third party modules #
from libcbm.input.sit import sit_cbm_factory
from libcbm.model.cbm import cbm_simulator

# First party modules #
from autopaths.auto_paths import AutoPaths
from plumbing.cache       import property_cached

# Internal modules #
from libcbm_runner.launch.create_json import CreateJSON

###############################################################################
class Simulation(object):
    """
    This class will run a `libcbm_py` simulation.
    """

    all_paths = """
    /input/json/config.json
    /output/
    """

    def __init__(self, parent):
        # Default attributes #
        self.parent = parent
        # Automatically access paths based on a string of many subpaths #
        self.paths = AutoPaths(self.parent.data_dir, self.all_paths)

    @property_cached
    def create_json(self):
        return CreateJSON(self)

    #------------------------------- Methods ---------------------------------#
    def run(self):
        # Create the JSON #
        self.create_json()
        # The 'AIDB' path as it was called previously #
        db_path = self.parent.country.aidb.paths.db
        # Create a SIT object #
        sit = sit_cbm_factory.load_sit(self.paths.json_config, db_path=db_path)
        # Do some initialization #
        classifiers, inventory = sit_cbm_factory.initialize_inventory(sit)
        # Create a CBM object #
        cbm = sit_cbm_factory.initialize_cbm(sit)
        # Not sure about this #
        results, reporting_func = cbm_simulator.create_in_memory_reporting_func()
        # Run #
        cbm_simulator.simulate(
            cbm,
            n_steps              = 100,
            classifiers          = classifiers,
            inventory            = inventory,
            pool_codes           = sit.defaults.get_pools(),
            flux_indicator_codes = sit.defaults.get_flux_indicators(),
            pre_dynamics_func    = lambda x: x,
            reporting_func       = reporting_func
        )
        # This will contain results #
        self.results = results
        # Return for convenience #
        return self.results