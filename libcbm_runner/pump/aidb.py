#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #
import os

# First party modules #
from autopaths.dir_path   import DirectoryPath
from autopaths.auto_paths import AutoPaths
from plumbing.cache       import property_cached

# Where is the data, default case #
aidb_repo = DirectoryPath("~/repos/libcbm_aidb/")

# But you can override that with an environment variable #
if os.environ.get("LIBCBM_AIDB"):
    aidb_repo = DirectoryPath(os.environ['LIBCBM_AIDB'])

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

    #----------------------------- Properties --------------------------------#
    @property_cached
    def db(self):
        """
        Returns a `plumbing.databases.sqlite_database.SQLiteDatabase` object
        useful for reading and modifying entries and tables.

        In addition one can also read/write to the AIDB files easily. To do this:

            `df = country.aidb.db.read_df('species')`

        To overwrite a table with a df

             `country.aidb.db.write_df(df, 'species')`
        """
        from plumbing.databases.sqlite_database import SQLiteDatabase
        return SQLiteDatabase(self.paths.aidb)

    #------------------------------- Methods ---------------------------------#
    def symlink_single_aidb(self):
        """
        During development, and for testing purposes we have a single AIDB
        that all countries can share and that is found in another repository.
        """
        # The path to the SQLite3 file #
        source = DirectoryPath(aidb_repo + 'aidb.db')
        # Check it exists #
        try:
            assert source
        except AssertionError:
            msg = "The sqlite3 database at '%s' does not seems to exist."
            raise AssertionError(msg % source)
        # Symlink #
        destin = self.paths.aidb
        source.link_to(destin)

    def symlink_all_aidb(self):
        """In production, every country has its own AIDB."""
        # The source #
        country_dir = aidb_repo + 'countries/' + self.parent.iso2_code
        source = country_dir + '/orig/config/aidb.db'
        # Check the AIDB exists #
        assert source
        # The destination #
        destin = self.paths.aidb
        # Remove destination if it already exists #
        destin.remove()
        # Symlink #
        source.link_to(destin)
        # Return #
        return 'Symlink success for ' + self.parent.iso2_code + '.'
