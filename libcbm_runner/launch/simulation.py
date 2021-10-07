#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
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
    """This class will run a `libcbm_py` simulation."""

    def __init__(self, parent):
        # Default attributes #
        self.parent  = parent
        self.runner  = parent
        self.country = self.runner.country
        # Record if we ended with an error or not #
        self.error = None

    def __repr__(self):
        return '%s object code "%s"' % (self.__class__, self.runner.short_name)

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
        if timestep == 1:
            # Print message #
            msg = "Carbon pool initialization period is finished." \
                  " Now starting the current period."
            self.parent.log.info(msg)
            # The name of our extra classifier #
            key = 'growth_period'
            # The value that the classifier should take for all timesteps #
            val = "Cur"
            # Get the corresponding ID in the libcbm simulation #
            id_of_cur = self.sit.classifier_value_ids[key][val]
            # Modify the whole column of the dataframe #
            cbm_vars.classifiers[key] = id_of_cur
        # Print a message #
        self.parent.log.info(f"Time step {timestep} is about to run.")
        # Return #
        return self.rule_based_processor.pre_dynamic_func(timestep, cbm_vars)

    #------------------------------- Methods ---------------------------------#
    # noinspection PyBroadException
    def __call__(self, interrupt_on_error=False):
        """
        Wrap the `run()` method by catching any type of exception
        and logging it.
        """
        try:
            self.run()
        except Exception:
            message = "Runner '%s' encountered an exception. See log file."
            self.runner.log.error(message % self.runner.short_name)
            self.runner.log.exception("Exception", exc_info=True)
            self.error = True
            if interrupt_on_error: raise

    def run(self):
        """
        Call `libcbm_py` to run the actual CBM simulation after creating some
        objects.

        The interaction with `libcbm_py` is decomposed in several calls to pass
        a `.json` config, a default database (also called aidb) and csv files.
        """
        # Message #
        self.runner.log.info("Setting up the libcbm_py objects.")
        # The 'AIDB' path as it was called previously #
        db_path = self.runner.country.aidb.paths.db
        assert db_path
        # Create a SIT object #
        self.sit = sit_cbm_factory.load_sit(str(self.runner.paths.json),
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
        # Message #
        self.runner.log.info("Calling the cbm_simulator.")
        # Run #
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
        # If we got here then we did not encounter any simulation error #
        self.error = False
        # Return for convenience #
        return self.results

    def clear(self):
        """
        Remove all objects from RAM otherwise the kernel will kill the python
        process after a couple countries being run.
        """
        if hasattr(self, 'sit'):     del self.sit
        if hasattr(self, 'clfrs'):   del self.clfrs
        if hasattr(self, 'inv'):     del self.inv
        if hasattr(self, 'cbm'):     del self.cbm
        if hasattr(self, 'results'): del self.results
