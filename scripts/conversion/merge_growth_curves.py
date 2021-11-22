#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

This script will combine the two files:

* /export/yields.csv
* /export/historical_yields.csv

into one single file.

The word "yield" will be dropped because it is a reserved keyword in python and
replaced by "growth".

* /export/growth_curves.csv

This is useful to switch all the yield curves of every species as soon as we
hit the country start year.
"""

# Built-in modules #

# Third party modules #
from tqdm import tqdm

# First party modules #
from plumbing.cache import property_cached

# Internal modules #
from libcbm_runner.core.continent import continent as libcbm_continent

# Continents #
from cbmcfs3_runner.core.continent import continent as cbmcfs3_continent

###############################################################################
class MergeGrowthCurves(object):

    def __init__(self, cbmcfs3_country):
        # Main attributes #
        self.cbmcfs3_country = cbmcfs3_country

    @property_cached
    def libcbm_country(self):
        """The matching libcbm country object."""
        return libcbm_continent.countries[self.cbmcfs3_country.iso2_code]

    def __call__(self, verbose=False):
        # Get paths #
        hist_curves = self.cbmcfs3_country.orig_data.paths.yields
        curr_curves = self.cbmcfs3_country.orig_data.paths.historical_yields
        destination = self.libcbm_country.orig_data.paths.growth_curves
        # Print output #
        if verbose:
            print(hist_curves)
            print(curr_curves)
            print(destination)
            print('----')
        # Combine #
        hist_curves.copy(destination)
        lines = iter(curr_curves)
        next(lines)
        destination.writelines(lines, mode='a')
        # Check headers are the same #
        assert hist_curves.first == curr_curves.first == destination.first
        # Remove old file #
        old_file = self.libcbm_country.data_dir + '/orig/csv/yield.csv'
        old_file.remove()

###############################################################################
if __name__ == '__main__':
    # Make converter objects, one per country #
    mergers = [MergeGrowthCurves(c) for c in cbmcfs3_continent]
    # Run them all #
    for merger in tqdm(mergers):
        merger()

