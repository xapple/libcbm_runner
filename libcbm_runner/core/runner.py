#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #

# First party modules #
from autopaths            import Path
from autopaths.auto_paths import AutoPaths
from plumbing.cache       import property_cached
from plumbing.logger      import create_file_logger

# Internal modules #
import libcbm_runner
from libcbm_runner.launch.simulation import Simulation
from libcbm_runner.pump.input_data   import InputData

###############################################################################
class Runner(object):
    """This object is capable of running a CBM simulation pipeline, starting
    from a few input tables, such as an inventory and a list of disturbances
    and to bring this data all the way to the predicted carbon stock."""

    all_paths = """
    /input/csv/
    /logs/runner.log
    """

    def __repr__(self):
        return '%s object on "%s"' % (self.__class__, self.data_dir)

    def __bool__(self): return self.paths.log.exists

    def __init__(self, scenario, country, num):
        # Base attributes #
        self.scenario = scenario
        self.country  = country
        self.num      = num
        # How to reference this runner #
        self.short_name  = self.scenario.short_name + '/'
        self.short_name += self.country.iso2_code + '/'
        self.short_name += str(self.num)
        # Where the data will be stored for this run #
        self.data_dir = self.scenario.scenarios_dir + self.short_name + '/'
        # Automatically access paths based on a string of many subpaths #
        self.paths = AutoPaths(self.data_dir, self.all_paths)

    @property_cached
    def log(self):
        """Each runner will have its own logger.
        By default we clear the log file when we start logging."""
        return create_file_logger(self.short_name, self.paths.log)

    @property
    def tail(self):
        """A short summary showing just the end of the log file."""
        msg  = "\n## Runner `%s`\n" % self.short_name
        msg += "\nTail of the log file at `%s`\n" % self.paths.log
        msg += self.paths.log.pretty_tail
        return msg

    @property_cached
    def simulation(self):
        """The object that can run `libcbm` simulations."""
        return Simulation(self)

    @property_cached
    def input_data(self):
        """Use the country object to copy the original input data."""
        return InputData(self)

    #------------------------------- Methods ---------------------------------#
    def run(self):
        """Run the full modelling pipeline for a given country,
        a given scenario and a given step."""
        # Messages #
        self.log.info("Using module at '%s'." % Path(libcbm_runner))
        self.log.info("Runner '%s' starting." % self.short_name)
        # Clean everything from previous run #
        self.remove_directory()
        # Copy the original input data #
        self.copy_orig_from_country()
        # Modify input data #
        pass
        # Run the model #
        self.simulation()
        # Post-processing #
        pass
        # Reporting #
        pass
        # Messages #
        self.log.info("Done.")

    def remove_directory(self):
        """Removes the directory that will be recreated by running this runner.
        Note: we need to keep the log we are writing to currently."""
        # Message #
        self.log.info("Removing directory '%s'." % self.data_dir)
        # The output directory #
        self.paths.input_dir.remove(safe=False)
        self.paths.output_dir.remove(safe=False)
        # Empty all the other logs found there except ours #
        for element in self.paths.logs_dir.flat_contents:
            if element != self.paths.log:
                element.remove()

    def copy_orig_from_country(self):
        """Refresh the input data by copying the immutable original
        CSVs from the current country."""
        destination_dir = self.paths.csv_dir
        destination_dir.remove()
        self.country.paths.csv_dir.copy(destination_dir)
