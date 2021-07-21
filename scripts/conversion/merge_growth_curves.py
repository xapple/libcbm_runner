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

This is useful to switch all the yield curves of every species as soon as we hit
the country start year.
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

    def __call__(self):
        pass

###############################################################################
if __name__ == '__main__':
    # Make converter objects, one per country #
    mergers = [MergeGrowthCurves(c) for c in cbmcfs3_continent]
    # Run them all #
    for merger in tqdm(mergers):
        merger()

