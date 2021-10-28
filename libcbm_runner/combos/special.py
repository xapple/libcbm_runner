#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #

# First party modules #

# Internal modules #
from libcbm_runner.combos.base_combo import Combination

###############################################################################
class Special(Combination):
    """
    An example Combination.
    """

    short_name = 'special'

    transitions = {'afforestation': 'enhanced_growth',
                   'mgmt':          'reference',
                   'nd_nsr':        'insect_outbreak',
                   'nd_sr':         'high_windstorms'}

    inventory   = {'afforestation': 'more_afforestation',
                   'mgmt':          'reference'}
