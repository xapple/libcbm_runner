#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A script to update the names of classifiers in every original csv input
file. Replace '_1' and '_2' with the real classifier names.
"""

# Built-in modules #

# Third party modules #
import pandas
from tqdm import tqdm

# First party modules #
from autopaths import Path

# Internal modules #
from libcbm_runner.core.continent import continent

###############################################################################
class OrigClassifRenamer(object):
    """
    `_1` becomes `forest_type` etc.
    """

    mapping = {
        '_1' : 'status',
        '_2' : 'forest_type',
        '_3' : 'region',
        '_4' : 'mgmt_type',
        '_5' : 'mgmt_strategy',
        '_6' : 'climate',
        '_7' : 'con_broad',
        '_8' : 'site_index',
        '_9' : 'growth_period',
    }

    def __init__(self, country):
        # Default attributes #
        self.country = country

    csv_list = ['events.csv', 'inventory.csv', 'transitions.csv',
                'growth_curves.csv']

    def __call__(self):
        for item in self.csv_list:
            csv_path = Path(self.country.data_dir + 'orig/csv/' + item)
            self.rename(csv_path)

    #------------------------------- Methods ---------------------------------#
    def rename(self, csv_path):
        """Loads one CSV files and renames columns."""
        # Load from disk #
        header = csv_path.first
        header = header.split(',')
        # Modify #
        header = map(self.mapping.get, header, header)
        # Write to disk #
        header = ','.join(header)
        csv_path.remove_first_line()
        csv_path.prepend(header)

###############################################################################
if __name__ == '__main__':
    renamers = [OrigClassifRenamer(c) for c in continent]
    for renamer in tqdm(renamers): renamer()