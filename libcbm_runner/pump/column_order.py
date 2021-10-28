#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #

# Third party modules #

# First party modules #

# Internal modules #

###############################################################################
# We need to record the column order in which data should appear in the
# `events.csv` file.
events_cols = [
    'status',
    'forest_type',
    'region',
    'mgmt_type',
    'mgmt_strategy',
    'climate',
    'con_broad',
    'site_index',
    'growth_period',
    'using_id',
    'sw_start',
    'sw_end',
    'hw_start',
    'hw_end',
    'min_since_last_dist',
    'max_since_last_dist',
    'last_dist_id',
    'min_tot_biom_c',
    'max_tot_biom_c',
    'min_merch_soft_biom_c',
    'max_merch_soft_biom_c',
    'min_merch_hard_biom_c',
    'max_merch_hard_biom_c',
    'min_tot_stem_snag_c',
    'max_tot_stem_snag_c',
    'min_tot_soft_stem_snag_c',
    'max_tot_soft_stem_snag_c',
    'min_tot_hard_stem_snag_c',
    'max_tot_hard_stem_snag_c',
    'min_tot_merch_stem_snag_c',
    'max_tot_merch_stem_snag_c',
    'min_tot_merch_soft_stem_snag_c',
    'max_tot_merch_soft_stem_snag_c',
    'min_tot_merch_hard_stem_snag_c',
    'max_tot_merch_hard_stem_snag_c',
    'efficiency',
    'sort_type',
    'measurement_type',
    'amount',
    'dist_type_name',
    'step',
]