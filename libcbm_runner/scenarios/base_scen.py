#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux

JRC biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #
import textwrap

# Third party modules #
from p_tqdm import p_umap, t_map

# First party modules #
from autopaths      import Path
from plumbing.timer import Timer

# Internal modules #

###############################################################################
class Scenario(object):
    """
    This object represents a harvest and economic scenario.
    Each Scenario subclass must define a list of Runner instances as
    the <self.runners> property.

    You can run a scenario like this:

        >>> from libcbm_runner.core.continent import continent
        >>> scen = continent.scenarios['historical']
        >>> scen()
    """

    def __init__(self, continent):
        # Save parent #
        self.continent = continent
        # This scenario dir #
        self.base_dir = Path(self.scenarios_dir + self.short_name + '/')

    def __repr__(self):
        return '%s object with %i runners' % (self.__class__, len(self))

    def __iter__(self): return iter(self.runners.values())
    def __len__(self):  return len(self.runners.values())

    #----------------------------- Properties --------------------------------#
    @property
    def scenarios_dir(self):
        """Shortcut to the scenarios directory."""
        return self.continent.scenarios_dir

    @property
    def runners(self):
        msg = "You should inherit from this class and implement this property."
        raise NotImplementedError(msg)

    #------------------------------- Methods ---------------------------------#
    def __call__(self, parallel=False, timer=True):
        """A method to run a scenarios by simulating all countries."""
        # Message #
        print("Running scenario '%s'." % self.short_name)
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
            return t_map(run_country, self.runners.items())
        # Run countries in parallel #
        if parallel:
            return p_umap(run_country, self.runners.items(), num_cpus=4)
        # Timer end #
        timer.print_end()
        timer.print_total_elapsed()

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
        # Return #
        return summary