#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #
import os

# Third party modules #

# First party modules #
from autopaths.dir_path import DirectoryPath
from autopaths.auto_paths import AutoPaths

# Where is the data, default case #
aidb_repo = DirectoryPath("~/repos/libcbm_aidb/")

# But you can override that with an environment variable #
if os.environ.get("AIDB_REPO"):
    aidb_repo = DirectoryPath(os.environ['AIDB_REPO'])

###############################################################################
class AIDB(object):
    """
    This class will provide access to the archive index database
    also called 'cbm_defaults' in libcbm.
    It is an SQLite3 database that weighs approx 18 MiB.

    To symlink the single test database to all countries do the following:

        >>> from libcbm_runner.core.continent import continent
        >>> for country in continent: country.aidb.symlink_single_aidb()

    To symlink every AIDB from every countries do the following:

        >>> from libcbm_runner.core.continent import continent
        >>> for country in continent: country.aidb.symlink_all_aidb()
    """

    all_paths = """
    /orig/config/aidb.db
    """

    def __init__(self, parent):
        # Default attributes #
        self.parent = parent
        # Directories #
        self.paths = AutoPaths(self.parent.data_dir, self.all_paths)

    def __bool__(self):
        return bool(self.paths.aidb)

    #------------------------------- Methods ---------------------------------#
    def symlink_single_aidb(self):
        """
        During development, and for testing purposes we have a single AIDB
        that all countries can share and that is found in another repository.
        """
        # Check it exists #
        source = aidb_repo + 'aidb.db'
        assert source
        # Symlink #
        destin = self.paths.aidb
        source.link_to(destin)

    def symlink_all_aidb(self):
        # Check it exists #
        country_dir = aidb_repo + 'countries/' + self.parent.iso2_code
        source = country_dir + '/orig/config/aidb.db'
        assert source
        # Symlink #
        destin = self.paths.aidb
        source.link_to(destin)
