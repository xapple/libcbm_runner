#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A script.
"""

# Built-in modules #

# Third party modules #
from plumbing.cache import property_cached
from tqdm import tqdm

# First party modules #

# Internal modules #
from libcbm_runner.core.continent import continent as libcbm_continent

# Continents #
from cbmcfs3_runner.core.continent import continent as cbmcfs3_continent

###############################################################################
class ComparisonRunner(object):
    """
    This class

    To access the results instead of doing:

        pools_libcbm_wide = runner_libcbm.simulation.results.pools

    You can do:

        pools_libcbm_wide = runner_libcbm.output['pools']

    To check the number of pools:

        pools_libcbm['pool'].unique()
    """

    def __init__(self, cbmcfs3_country):
        # Main attributes #
        self.cbmcfs3_country = cbmcfs3_country

    #----------------------------- Properties --------------------------------#
    @property_cached
    def libcbm_country(self):
        """The matching libcbm country object."""
        return libcbm_continent.countries[self.cbmcfs3_country.iso2_code]

    #---------- Runners -----------#
    @property
    def runner_cbmcfs3(self):
        return self.runner_cbm3.post_processor.pool_indicators_long

    @property
    def runner_libcbm(self):
        return self.runner_cbm3.post_processor.pool_indicators_long

    #---------- Pools -----------#
    @property
    def pools_cbmcfs3(self):
        return self.runner_cbm3.post_processor.pool_indicators_long

    @property
    def pools_cbmcfs3(self):
        return self.runner_cbm3.post_processor.pool_indicators_long

    #------------------------------- Methods ---------------------------------#
    def __call__(self):
        id_vars = ['identifier', 'timestep', 'Input']
        pools_libcbm = pools_libcbm_wide.melt(id_vars    = id_vars,
                                              var_name   = 'pool',
                                              value_name = 'tc')


###############################################################################
if __name__ == '__main__':
    # Make comparisons objects, one per country #
    comparisons = [ComparisonRunner(c) for c in cbmcfs3_continent]
    # Run them all #
    for compare in tqdm(comparisons):
        compare()
