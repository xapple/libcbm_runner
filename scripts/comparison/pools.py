#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A script.
"""

# Built-in modules #

# Third party modules #
from plumbing.cache import property_cached

# First party modules #

# Internal modules #
from libcbm_runner.core.continent import continent as libcbm_continent

# Continents #
from cbmcfs3_runner.core.continent import continent as cbmcfs3_continent

###############################################################################
class ComparisonRunner(object):
    """
    This class
    """

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
    # Make comparisons objects, one per country #
    comparisons = [ComparisonRunner(c) for c in cbmcfs3_continent]
    # Run them all #
    for compare in tqdm(comparisons):
        compare()
