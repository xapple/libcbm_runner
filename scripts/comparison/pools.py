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
    This class can compare the results of european forest simulations
    between the new `libcbm` libarary and the old windows CBM-CFS3 software.

    To access the results instead of doing:

        >>> pools_libcbm_wide = runner_libcbm.simulation.results.pools

    You can do:

        >>> pools_libcbm_wide = runner_libcbm.output['pools']

    To check the number of pools:

        >>> pools_libcbm['pool'].unique()

    To use this class you can do:

        >>> import os
        >>> home = os.environ.get('HOME', '~') + '/'
        >>> from importlib.machinery import SourceFileLoader
        >>> path = home + 'repos/libcbm_runner/scripts/comparison/pools.py'
        >>> comp = SourceFileLoader('pools', path).load_module()
        >>> from cbmcfs3_runner.core.continent import continent as cbmcfs3_continent
        >>> comparisons = [ComparisonRunner(c) for c in cbmcfs3_continent]
    """

    def __init__(self, cbmcfs3_country):
        # Main attributes #
        self.cbmcfs3_country = cbmcfs3_country
        # Shortcuts #
        self.iso2_code = cbmcfs3_country.iso2_code

    def __repr__(self):
        return '%s object code "%s"' % (self.__class__, self.iso2_code)

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
        return cbmcfs3_continent.scenarios['static_demand']

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
    def pools_libcbm(self):
        # Load #
        result = self.runner_libcbm.output['pools']
        id_vars = ['identifier', 'timestep', 'Input']
        # Unpivot #
        result = result.melt(id_vars    = id_vars,
                             var_name   = 'pool',
                             value_name = 'tc')
        # Return #
        return result

    #----------- Joined ------------#
    @property_cached
    def df(self):
        # Load #
        cbmcfs3 = 0
        libcbm  = 0
        # Lorem #
        # Return #
        return df

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
