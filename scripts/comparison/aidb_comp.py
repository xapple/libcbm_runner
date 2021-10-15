#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #
import os

# Third party modules #
from tqdm import tqdm

# First party modules #
from plumbing.cache import property_cached

# Internal modules #
from libcbm_runner.core.continent import continent as libcbm_continent

# Continents #
from cbmcfs3_runner.core.continent import continent as cbmcfs3_continent

###############################################################################
class CompareAIDB(object):
    """
    This class will enable us to compare the AIDB from the old MS Access
    format supported by CBM-CFS3 with the new SQLite format supported by
    libcbm.

    You instantiate the class with a Country object from cbmcfs_runner.
    Then you get access to the corresponding Country object from libcbm_runner.

    Typically you would run this file from a command line like this:

         ipython3 -i -- ~/repos/libcbm_runner/scripts/comparison/aidb_comp.py

    Then you can inspect object as so:

        >>> comp = comparisons[3]
        >>> print(comp.libcbm_aidb.db.read_df('slow_mixing_rate'))
        >>> print(comp.cbmcfs3_aidb.database['tblSlowAGtoBGTransferRate'])
    """

    def __init__(self, cbmcfs3_country):
        # Main attributes #
        self.cbmcfs3_country = cbmcfs3_country

    @property_cached
    def libcbm_country(self):
        """The matching libcbm country object."""
        return libcbm_continent.countries[self.cbmcfs3_country.iso2_code]

    @property_cached
    def cbmcfs3_aidb(self):
        return self.cbmcfs3_country.aidb

    @property_cached
    def libcbm_aidb(self):
        return self.libcbm_country.aidb

    def __call__(self):
        msg = "Comparing %s with %s."
        print(msg % (self.cbmcfs3_aidb, self.libcbm_aidb))

    def compare_table(self, table_name):
        df1 = self.libcbm_aidb.db.read_df(table_name)
        df2 = self.cbmcfs3_aidb.database[table_name]

###############################################################################
if __name__ == '__main__':
    # Make comparison objects, one per country #
    comparisons = [CompareAIDB(c) for c in cbmcfs3_continent]
    # Run them all #
    for comp in tqdm(comparisons):
        comp()



