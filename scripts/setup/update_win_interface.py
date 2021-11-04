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
from make_activities import makers

###############################################################################
# See script "make_activities.py" for documentation
if __name__ == '__main__':
    print([maker.make_interface(True, True) for maker in tqdm(makers)])

