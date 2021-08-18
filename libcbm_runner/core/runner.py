#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #

# First party modules #
from autopaths.auto_paths import AutoPaths
from plumbing.cache       import property_cached
from plumbing.logger      import create_file_logger
from plumbing.timer       import LogTimer

# Internal modules #
import libcbm_runner
from libcbm_runner.launch.create_json  import CreateJSON
from libcbm_runner.launch.simulation   import Simulation
from libcbm_runner.pump.input_data     import InputData
from libcbm_runner.pump.output_data    import OutputData
from libcbm_runner.pump.internal_data  import InternalData
from libcbm_runner.pump.pre_processor  import PreProcessor
from libcbm_runner.pump.post_processor import PostProcessor

# Third party modules
import pandas

###############################################################################
class Runner(object):
    """
    This object is capable of running a CBM simulation pipeline, starting
    from a few input tables, such as an inventory and a list of disturbances
    and to bring this data all the way to the predicted carbon stock and
    fluxes.

    You can run a scenario like this:

        >>> from libcbm_runner.core.continent import continent
        >>> scenario = continent.scenarios['historical']
        >>> runner   = scenario.runners['LU'][0]
        >>> runner.run()

    The runner has an attribute `output` that only deals with final output
    data that can be reached after closing and reopening your interpreter.

    The runner has an attribute `internal` that only deals with getting the
    data from the libcbm objects as they are while still in RAM and not
    written to disk. Examples:

    >>> runner.internal.classif_df
    If you are running a simluation and want to get the information from RAM.

    >>> runner.output.classif_df
    If you are analyzing results that were run in the past and want to get the
    information from disk.
    """

    all_paths = """
    /input/
    /input/json/config.json
    /output/
    /logs/runner.log
    """

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

    def __repr__(self):
        return '%s object on "%s"' % (self.__class__, self.data_dir)

    def __bool__(self): return self.paths.log.exists

    #---------------------------- Compositions -------------------------------#
    @property_cached
    def create_json(self):
        return CreateJSON(self)

    @property_cached
    def simulation(self):
        """The object that can run `libcbm` simulations."""
        return Simulation(self)

    @property_cached
    def pre_processor(self):
        """Update the input data to this run using some rules."""
        return PreProcessor(self)

    @property_cached
    def post_processor(self):
        """Update or convert the output data to this run using some rules."""
        return PostProcessor(self)

    @property_cached
    def input_data(self):
        """
        Access the input data to this run. This data can be
        a modified version of the original country's CSV files.
        """
        return InputData(self)

    @property_cached
    def output(self):
        """Create and access the output data to this run."""
        return OutputData(self)

    @property_cached
    def internal(self):
        """
        Access and format data concerning the simulation as it is being
        run.
        """
        return InternalData(self)

    #----------------------------- Properties --------------------------------#
    @property
    def scen_orig_dir(self):
        """
        A directory that contains original data specific only to the current
        scenario. Typically this can be a directory such as:
        `libcbm_data/countries/AT/afforestation/`
        """
        return self.country.data_dir + self.scenario.short_name + '/'

    @property_cached
    def log(self):
        """
        Each runner will have its own logger.
        By default we clear the log file when we start logging.
        """
        # Pick console level #
        level = 'error'
        if hasattr(self, 'verbose'):
            if isinstance(self.verbose, bool):
                if self.verbose:
                    level = 'debug'
            else: level = self.verbose
        # Create #
        logger = create_file_logger(self.short_name,
                                    self.paths.log,
                                    console_level = level)
        # Return #
        return logger

    @property
    def tail(self):
        """A short summary showing just the end of the log file."""
        msg  = "\n## Runner `%s`\n" % self.short_name
        msg += "\nTail of the log file at `%s`\n" % self.paths.log
        msg += self.paths.log.pretty_tail
        return msg

    @property_cached
    def num_timesteps(self):
        """
        Compute the default number of years we have to run the simulation for.
        To do this, we select the disturbance with the highest time step.
        """
        # Load #
        df = self.input_data.load('events')
        # Compute #
        period_max = df['step'].max()
        # Return #
        return period_max

    #------------------------------- Methods ---------------------------------#
    def run(self, keep_in_ram=False, verbose=True, interrupt_on_error=False):
        """
        Run the full modelling pipeline for a given country, a given scenario
        and a given step.
        """
        # Verbosity level #
        self.verbose = verbose
        # Messages #
        self.log.info("Using %s." % libcbm_runner)
        self.log.info("Runner '%s' starting." % self.short_name)
        # Start the timer #
        self.timer = LogTimer(self.log)
        self.timer.print_start()
        # Clean everything from previous run #
        self.remove_directories()
        # Copy the original input data #
        self.input_data.copy_orig_from_country()
        # Modify input data, scenarios can subclass this #
        self.modify_input()
        # Pre-processing #
        self.pre_processor()
        # Create the JSON configuration #
        self.create_json()
        # Run the model #
        self.timer.print_elapsed()
        self.simulation(interrupt_on_error)
        self.timer.print_elapsed()
        # Save the results to disk #
        if self.simulation.error is not True: self.output.save()
        # Free memory #
        if not keep_in_ram: self.simulation.clear()
        # Post-processing #
        self.post_processor()
        # Messages #
        self.timer.print_end()
        self.timer.print_total_elapsed()
        # Final message #
        if self.simulation.error is not True: msg = "Done."
        else: msg = "Done with errors."
        self.log.info(msg)
        # Return #
        return self.output

    def remove_directories(self):
        """
        Removes the directory that will be recreated by running this runner.
        This guarantees that all output data is regenerated.
        Note: we need to keep the log we are writing to currently.
        """
        # Message #
        self.log.info("Removing directory '%s'." % self.data_dir.with_tilda)
        # The output directory #
        self.paths.input_dir.remove(safe=False)
        self.paths.output_dir.remove(safe=False)
        # Empty all the other logs found there except ours #
        for element in self.paths.logs_dir.flat_contents:
            if element != self.paths.log:
                element.remove()

    #--------------------------- Special Methods -----------------------------#
    def get_orig_data(self):
        return self.input_data.copy_orig_from_country()

    def events_wide_to_long(self):
        """
        Reshape disturbance events from wide to long format.
        #TODO move this method out of the runner. It is specific to scenarios.
        """
        # Load the events table
        file_path = self.scen_orig_dir + 'csv/' + 'events_wide_'
        file_path += self.scenario.abbreviation + '.csv'
        events_wide = pandas.read_csv(file_path)
        # Reshape from wide to long format
        events_wide["id"] = events_wide.index
        events = pandas.wide_to_long(events_wide,
                                     stubnames = "amount ",
                                     i         = "id",
                                     j         = "year")
        events = events.reset_index()
        # Convert years to time steps
        events['step'] = self.country.year_to_timestep(events['year'])
        # Remove the space in the amount column name
        events = events.rename(columns={"amount ": "amount"})
        # Reorder columns according to the reference table in the orig data
        col_name_order = self.country.orig_data.load('events', False)
        events         = events[col_name_order.columns.tolist()]
        # Return #
        return events

    def modify_input(self):
        """Scenarios can subclass this at will."""
        pass
