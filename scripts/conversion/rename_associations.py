#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

This script will rename the header column of the file:

* /common/associations.csv

Before running this script the headers are simply "A", "B", "C".

After running this script, the new headers will be:

* "category"
* "name_input"
* "name_aidb"
"""

# Built-in modules #

# Third party modules #
import pandas
from tqdm import tqdm

# First party modules #

# Internal modules #
from libcbm_runner.core.continent import continent

###############################################################################
class RenameAssociations(object):

    def __init__(self, country):
        # Main attributes #
        self.country = country

    def __call__(self, verbose=False):
        # Get path #
        path = self.country.orig_data.paths.associations
        # Load dataframe #
        df = pandas.read_csv(str(path))
        # Modify dataframe #
        df.columns = ["category", "name_input", "name_aidb"]
        # Write dataframe back to disk #
        df.to_csv(str(path), index=False, float_format='%g')

###############################################################################
if __name__ == '__main__':
    # Make renamer objects, one per country #
    renamers = [RenameAssociations(c) for c in continent]
    # Run them all #
    for merger in tqdm(renamers):
        merger()
