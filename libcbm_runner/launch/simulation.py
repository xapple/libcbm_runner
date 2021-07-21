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

    def pre_dynamics_func(self, timestep, cbm_vars):
        if timestep == 1:
            print("Carbon pool initialization is finished, now starting the current period")
            # see the simulate method of the libcbm simulator
            # https://github.com/cat-cfs/libcbm_py/blob/e9e37ce5a91cb2bcb07011812a7d49c859d88fa4/libcbm/model/cbm/cbm_simulator.py#L148
            # if t=1 we know this is the first timestep, and nothing has yet been done to the post-spinup pools
            # it is here that you want to change the yields,
            # And this can be done by changing the classifier set of each inventory record
            cbm_vars.classifiers.initialization = self.sit.classifier_value_ids["initialization"]["c"]

        return self.rule_based_processor.pre_dynamic_func(timestep, cbm_vars)

    #------------------------------- Methods ---------------------------------#
    def run(self):
        """
        Call `libcbm_py` to run the cbm simulation.

        The interaction with `libcbm_py` is decomposed in several calls to pass a
        `.json` config, a default database (also called aidb) and csv files.
        """
        print("Preparing the data")
        # Create the JSON #
        self.create_json()
        # The 'AIDB' path as it was called previously #
        db_path = self.parent.country.aidb.paths.db
        # Create a SIT object #
        self.sit = sit_cbm_factory.load_sit(str(self.paths.json_config), db_path=str(db_path))
        # Do some initialization #
        self.classifiers, self.inventory = sit_cbm_factory.initialize_inventory(self.sit)
        # Create a CBM object #
        self.cbm = sit_cbm_factory.initialize_cbm(self.sit)
        # This will contain results #
        self.results, reporting_func = cbm_simulator.create_in_memory_reporting_func()
        # Create a function to apply rule based events and transition rules #
        self.rule_based_processor = sit_cbm_factory.create_sit_rule_based_processor(self.sit, self.cbm)
        print("Running the libcbmsimulation")
        # Run #
        cbm_simulator.simulate(
            self.cbm,
            n_steps              = 100,
            classifiers          = self.classifiers,
            inventory            = self.inventory,
            pool_codes           = self.sit.defaults.get_pools(),
            flux_indicator_codes = self.sit.defaults.get_flux_indicators(),
            pre_dynamics_func    = self.pre_dynamics_func,
            reporting_func       = reporting_func
        )
        # Return for convenience #
        return self.results
