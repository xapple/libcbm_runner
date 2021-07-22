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

# Internal modules #

###############################################################################
class Simulation(object):
    """
    This class will run a `libcbm_py` simulation.
    """

    def __init__(self, parent):
        # Default attributes #
        self.parent  = parent
        self.runner  = parent
        self.country = self.runner.country

    #--------------------------- Special Methods -----------------------------#
    def dynamics_func(self, timestep, cbm_vars):
        """
        See the simulate method of the libcbm simulator:

            https://github.com/cat-cfs/libcbm_py/blob/master/libcbm/
            model/cbm/cbm_simulator.py#L148

        If t=1, we know this is the first timestep, and nothing has yet been
        done to the post-spinup pools. It is at this moment that we want to
        change the growth curves, and this can be done by switching the
        classifier value of each inventory record.
        """
        # Check the timestep #
        self.parent.log.info(f"Time step {timestep}")
        if timestep == 1:
            self.parent.log.info("Carbon pool initialization period is finished.")
            self.parent.log.info("Now starting the current period.")
            # The name of our extra classifier #
            key = 'Simulation period (for yields)'
            # Get the corresponding ID in the libcbm simulation #
            id_of_cur = self.sit.classifier_value_ids[key]["Cur"]
            # Modify the whole column of the dataframe #
            cbm_vars.classifiers[key] = id_of_cur
        # Return #
        return self.rule_based_processor.pre_dynamic_func(timestep, cbm_vars)

    #------------------------------- Methods ---------------------------------#
    def run(self):
        """
        Call `libcbm_py` to run the cbm simulation.

        The interaction with `libcbm_py` is decomposed in several calls to pass
        a `.json` config, a default database (also called aidb) and csv files.
        """
        self.parent.log.info("Prepare input data.")
        # The 'AIDB' path as it was called previously #
        db_path = self.parent.country.aidb.paths.db
        # Create a SIT object #
        self.sit = sit_cbm_factory.load_sit(str(self.parent.paths.json),
                                            db_path = str(db_path))
        # Do some initialization #
        self.clfrs, self.inv = sit_cbm_factory.initialize_inventory(self.sit)
        # Create a CBM object #
        self.cbm = sit_cbm_factory.initialize_cbm(self.sit)
        # This will contain results #
        self.results, reporting_func = \
            cbm_simulator.create_in_memory_reporting_func()
        # Create a function to apply rule based events and transition rules #
        self.rule_based_processor = \
            sit_cbm_factory.create_sit_rule_based_processor(self.sit, self.cbm)
        # Run #
        self.parent.log.info("Start the simulation.")
        cbm_simulator.simulate(
            self.cbm,
            n_steps              = self.runner.num_timesteps,
            classifiers          = self.clfrs,
            inventory            = self.inv,
            pool_codes           = self.sit.defaults.get_pools(),
            flux_indicator_codes = self.sit.defaults.get_flux_indicators(),
            pre_dynamics_func    = self.dynamics_func,
            reporting_func       = reporting_func
        )
        # Return for convenience #
        return self.results
