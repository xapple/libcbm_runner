#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A script to harmonize the names of classifiers in every country to snake_case.
"""

# Built-in modules #

# Third party modules #
import pandas
from tqdm import tqdm

# First party modules #

# Internal modules #
from libcbm_runner.core.continent import continent

###############################################################################
class ClassifierRenamer(object):
    """
    `Forest type` becomes `forest_type` etc.

    """

    mapping = {
        'Status'                         : 'status',
        'Forest type'                    : 'forest_type',
        'Region'                         : 'region',
        'Management type'                : 'mgmt_type',
        'Management strategy'            : 'mgmt_strategy',
        'Climatic unit'                  : 'climate',
        'Conifers/Broadleaves'           : 'con_broad',
        'Site index'                     : 'site_index',
        'Simulation period (for yields)' : 'growth_period',
    }

    def __init__(self, country):
        # Default attributes #
        self.country = country

    def __call__(self):
        path = self.country.orig_data.paths.classifiers
        df = pandas.read_csv(str(path))
        df['name'] = df['name'].replace(self.mapping)
        df.to_csv(str(path), index=False, float_format='%g')

###############################################################################
if __name__ == '__main__':
    renamers = [ClassifierRenamer(c) for c in continent]
    for renamer in tqdm(renamers): renamer()