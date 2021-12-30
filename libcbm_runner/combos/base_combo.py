#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #
import textwrap

# Third party modules #
import yaml, pandas
from p_tqdm import p_umap, t_map

# First party modules #
from autopaths      import Path
from plumbing.cache import property_cached
from plumbing.timer import Timer

# Internal modules #
from libcbm_runner import libcbm_data_dir
from libcbm_runner.core.runner import Runner

# Constant directory for all the data #
yaml_dir = libcbm_data_dir + 'combos/'

###############################################################################
class Combination(object):
    """
    This object represents a combination of specific scenarios for different
    activities and includes any other customization of a given model run.

    Each Combination subclass must define a list of Runner instances as
    the <self.runners> property. This enables the complete customization of
    any Runner by the specific Combination instance.

    You can run a combo like this:

        >>> from libcbm_runner.core.continent import continent
        >>> combo = continent.combos['historical']
        >>> combo()

    You can run a specific runner from a given country like this:

        >>> from libcbm_runner.core.continent import continent
        >>> combo = continent.combos['historical']
        >>> r = combo.runners['LU'][-1]
        >>> r.run(True, True, True)

    You can then check the output pools:

        >>> r.output.load('pools')
    """

    short_name = None

    def __init__(self, continent):
        # Save parent #
        self.continent = continent
        # The combos dir used for all output #
        self.output_dir = self.continent.output_dir
        # The base dir for our output #
        self.base_dir = Path(self.output_dir + self.short_name + '/')

    def __repr__(self):
        return '%s object with %i runners' % (self.__class__, len(self))

    def __iter__(self): return iter(self.runners.values())
    def __len__(self):  return len(self.runners.values())

    def __getitem__(self, key):
        """Return a runner based on a country code."""
        return self.runners[key]

    #----------------------------- Properties --------------------------------#
    @property_cached
    def config(self):
        """
        The values chosen by the user in the YAML file which decide on every
        scenario choice for every activity and silvicultural practice.
        """
        # The path to our specific YAML file #
        yaml_path = yaml_dir + self.short_name + '.yaml'
        # Read it with a third party library #
        with open(yaml_path, "r") as handle:
            result = yaml.safe_load(handle)
        # Convert silvicultural choices to dataframes #
        key = 'demand'
        value = result[key]
        if not isinstance(value, str):
            df = pandas.DataFrame.from_dict(value,
                                            orient  = 'index',
                                            columns = ['scenario'])
            df = df.rename_axis('year').reset_index()
            result[key] = df
        # Return result #
        return result

    @property_cached
    def runners(self):
        """
        A dictionary of country codes as keys with a list of runners as
        values.
        """
        return {c.iso2_code: [Runner(self, c, 0)] for c in self.continent}

    #------------------------------- Methods ---------------------------------#
    def __call__(self, parallel=False, timer=True):
        """A method to run a combo by simulating all countries."""
        # Message #
        print("Running combo '%s'." % self.short_name)
        # Timer start #
        timer = Timer()
        timer.print_start()
        # Function to run a single country #
        def run_country(args):
            code, steps = args
            for runner in steps:
                return runner.run()
        # Run countries sequentially #
        if not parallel:
            result = t_map(run_country, self.runners.items())
        # Run countries in parallel #
        else:
            result = p_umap(run_country, self.runners.items(), num_cpus=4)
        # Timer end #
        timer.print_end()
        timer.print_total_elapsed()
        # Compile logs #
        self.compile_logs()
        # Return #
        return result

    def compile_logs(self, step=-1):
        # Open file #
        summary = self.base_dir + 'all_logs.md'
        summary.open(mode='w')
        # Write title #
        title = "# Summary of all log files #\n\n"
        summary.handle.write(title)
        # Loop over runners #
        for rs in self.runners.values():
            r = rs[step]
            summary.handle.write("\n## " + r.country.country_name)
            summary.handle.write(' (' + r.country.iso2_code + ')' + '\n\n')
            content = textwrap.indent(r.paths.log.contents, '    ')
            summary.handle.write(content)
        # Close #
        summary.close()
        # Message #
        msg = "Log files compiled at:\n\n%s\n"
        print(msg % summary)
        # Return #
        return summary
