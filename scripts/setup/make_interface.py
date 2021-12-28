#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #

# Third party modules #
from tqdm import tqdm

# First party modules #

# Internal modules #
from libcbm_runner.core.continent import continent
from activities_creation import MakeActivities

###############################################################################
makers = [MakeActivities(c) for c in continent]

if __name__ == '__main__':
    print([maker.make_interface() for maker in tqdm(makers)])