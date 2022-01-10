#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

This script will add the required flux aggregate indicators to the AIDB of
every country.

If you want to test the script on only one country use:

    >>> if adder.iso2_code != 'ZZ': continue
"""

# Built-in modules #
import os

# Third party modules #
from tqdm import tqdm

# First party modules #
from plumbing.cache import property_cached
from plumbing.timer import Timer

# Internal modules #
from libcbm_runner.core.continent import continent

###############################################################################
class AddIndicators(object):
    """
    This class will open each AIDB and modify three tables in it:

    * `flux_indicator`
    * `flux_indicator_sink`
    * `flux_indicator_source`

    The pool IDs:

        1   SoftwoodMerch
        2   SoftwoodFoliage
        3   SoftwoodOther
        4   SoftwoodCoarseRoots
        5   SoftwoodFineRoots
        6   HardwoodMerch
        7   HardwoodFoliage
        8   HardwoodOther
        9   HardwoodCoarseRoots
        10  HardwoodFineRoots
        18  SoftwoodStemSnag
        19  SoftwoodBranchSnag
        20  HardwoodStemSnag
        21  HardwoodBranchSnag
        26  Products
    """

    def __repr__(self):
        return '%s object code "%s"' % (self.__class__,
                                        self.iso2_code)

    def __init__(self, country):
        # Main attributes #
        self.country = country
        # Shortcuts #
        self.iso2_code = self.country.iso2_code
        self.db = self.country.aidb.db

    useless = ['DisturbanceSoftProduction',
               'DisturbanceHardProduction',
               'DisturbanceDOMProduction']

    new_ones = ['softwood_merch_to_product',
                'softwood_other_to_product',
                'softwood_stem_snag_to_product',
                'softwood_branch_snag_to_product',
                'hardwood_merch_to_product',
                'hardwood_other_to_product',
                'hardwood_stem_snag_to_product',
                'hardwood_branch_snag_to_product']

    nums    = [53, 54, 55, 56, 57, 58, 59, 60]

    sources = [1,   3, 18, 19,  6,  8, 20, 21]

    sink = 26

    def __call__(self, debug=False, remove_legacy=False):
        # Optional debugging messages #
        if debug:
            num_rows = self.db.count_entries('flux_indicator')
            print(self.iso2_code, num_rows)
        # Read tables #
        indics  = self.db.read_df("flux_indicator")
        sources = self.db.read_df("flux_indicator_source")
        sinks   = self.db.read_df("flux_indicator_sink")
        # Drop old useless indicators that were going to products #
        if remove_legacy:
            for indic_name in self.useless:
                # Get the ID #
                num = indics.query("name == '%s'" % indic_name)['id'].item()
                # Drop from main table #
                indic_loc = indics.loc[indics['id'] == num].index
                indics = indics.drop(indic_loc)
                # Drop from secondary tables #
                loc = sources.loc[sources['flux_indicator_id'] == num].index
                sources = sources.drop(loc)
                loc = sinks.loc[sinks['flux_indicator_id'] == num].index
                sinks = sinks.drop(loc)
        # Add our eight new indicators #
        for num, new, source in zip(self.nums, self.new_ones, self.sources):
            # Add to the main table #
            indics = indics.append({'id':              num,
                                    'name':            new,
                                    'flux_process_id': 3 },
                                    ignore_index = True)
            # Add to the source table #
            highest = sources['id'].max()
            sources = sources.append({'id':                highest + 1,
                                      'flux_indicator_id': num,
                                      'pool_id':           source},
                                      ignore_index = True)
            # Add to the sink table #
            highest = sinks['id'].max()
            sinks = sinks.append({'id':                highest + 1,
                                  'flux_indicator_id': num,
                                  'pool_id':           self.sink},
                                  ignore_index = True)
        # Write tables #
        self.db.write_df(indics,  "flux_indicator")
        self.db.write_df(sources, "flux_indicator_source")
        self.db.write_df(sinks ,  "flux_indicator_sink")

###############################################################################
if __name__ == '__main__':
    # Make adder objects, one per country #
    adders = [AddIndicators(c) for c in continent]
    # Message #
    print("Adding flux indicators.")
    print("-------------")
    # Print timer start #
    timer = Timer()
    timer.print_start()
    # Run them all #
    for adder in tqdm(adders):
        adder()
    # Print end #
    timer.print_end()
    timer.print_total_elapsed()

