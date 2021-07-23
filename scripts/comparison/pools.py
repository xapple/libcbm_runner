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
        # Shortcuts #
        self.iso2_code = cbmcfs3_country.iso2_code

    #----------------------------- Properties --------------------------------#
    @property_cached
    def libcbm_country(self):
        """The matching libcbm country object."""
        return libcbm_continent.countries[self.cbmcfs3_country.iso2_code]

    @property
    def title(self):
        msg = "# %s (%s)\n"
        msg = msg % (self.cbmcfs3_country.country_name, self.iso2_code)
        msg = msg + "### Comparing libcbm -vs- cbmcfs3 \n\n"
        return msg

    #--------- Scenarios ----------#
    @property
    def scen_cbmcfs3(self):
        return cbmcfs3_continent.scenarios['historical']

    @property
    def scen_libcbm(self):
        return libcbm_continent.scenarios['historical']

    #---------- Runners -----------#
    @property
    def runner_cbmcfs3(self):
        return self.scen_cbmcfs3[self.iso2_code][-1]

    @property
    def runner_libcbm(self):
        return self.scen_libcbm[self.iso2_code][-1]

    #----------- Pools ------------#
    @property
    def pools_cbmcfs3(self):
        # Load #
        post = self.runner_cbmcfs3.post_processor
        result = post.pool_indicators_long
        # Return #
        return result

    @property
    def pools_cbmcfs3(self):
        # Load #
        result = self.runner_libcbm.output['pools']
        id_vars = ['identifier', 'timestep', 'Input']
        # Unpivot #
        result = result.melt(id_vars    = id_vars,
                             var_name   = 'pool',
                             value_name = 'tc')
        # Return #
        return result

    #------------------------------- Methods ---------------------------------#
    def __call__(self):
        print(self.title)
        

###############################################################################
if __name__ == '__main__':
    # Make comparisons objects, one per country #
    comparisons = [ComparisonRunner(c) for c in cbmcfs3_continent]
    # Run them all #
    for compare in tqdm(comparisons):
        compare()
