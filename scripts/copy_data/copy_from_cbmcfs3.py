#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

A script to copy over the data from the cbmcfs3_data repository to the libcbm_data repository.

Typically you would run this file from a command line like this:

     ipython3 -i -- ~/deploy/libcbm_runner/scripts/copy_data/copy_from_cbmcfs3.py
"""

# Third party modules #
from tqdm import tqdm

# First party modules #
from cbmcfs3_runner.core.continent import continent as cbm_continent

# Internal modules #
from libcbm_runner.core.continent  import continent as lib_continent

# Constants #
delete = False

###############################################################################
for lib_country, cbm_country in tqdm(zip(lib_continent, cbm_continent)):
    # Check we are pairing countries correctly #
    assert lib_country.iso2_code == cbm_country.iso2_code
    # Optionally delete old stuff #
    if delete:
        lib_country.data_dir.remove()
        lib_country.data_dir.create()
    # Define what we will copy #
    orig_files_to_copy = {
        'ageclass':           'age_classes',
        'classifiers':        'classifiers',
        'disturbance_events': 'events',
        'disturbance_types':  'disturbance_types',
        'inventory':          'inventory',
        'transition_rules':   'transitions',
        'yields':             'yield',
    }
    # Main loop #
    for old_name, new_name in orig_files_to_copy.items():
        source = cbm_country.orig_data.paths[old_name]
        destin = lib_country.orig_data.paths[new_name]
        source.copy(destin)
