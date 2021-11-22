#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you would run this file from a command line like this:

     ipython3 -i -- ~/deploy/libcbm_runner/scripts/setup/aidb_symlink.py
"""

# Built-in modules #
from libcbm_runner.core.continent import continent

# Create symlinks to every AIDB from every countries
for country in continent: country.aidb.symlink_all_aidb()

