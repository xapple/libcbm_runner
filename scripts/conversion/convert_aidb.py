#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

This script will convert the AIDB from the old MS Access format supported by
CBM-CFS3 to the new SQLite format supported by libcbm.

Typically you would run this file from a command line like this on a windows
 system which has repositories in the home directory:

     ipython3.exe -i -- %HOMEPATH%/repos/libcbm_runner/scripts/conversion/aidb.py

You need to run this on a machine that has a Microsoft Access driver installed.
So likely this will require a Windows machine.

If you try on a Unix machine, even with `unixodbc` installed you will get an
error such as:

    Error: ('01000', "[01000] [unixODBC][Driver Manager]
    Can't open lib 'Microsoft Access Driver (*.mdb, *.accdb)'
    : file not found (0) (SQLDriverConnect)")

If you want to run only one country for testing, you can place
this line in the main loop:

        if converter.cbmcfs3_country.iso2_code != 'ZZ': continue
"""

# Built-in modules #
import os

# Third party modules #
from tqdm import tqdm

# First party modules #
import cbm_defaults.app
from plumbing.cache import property_cached
from plumbing.timer import Timer

# Internal modules #
from libcbm_runner.core.continent import continent as libcbm_continent

# Continents #
from cbmcfs3_runner.core.continent import continent as cbmcfs3_continent

# Constants #
home = os.path.expanduser("~")
ddl_path = home + r"\repos\cbm_defaults\schema\cbmDefaults.ddl"

###############################################################################
class ConvertAIDB(object):
    """
    This class will enable us to convert the old AIDB format (Access DB)
    from CBMCFS3 to an SQLite3 database compatible with `libcbm_py`.
    We will use only one locale, and keep "en-CA".
    """

    template = {
        "output_path": None,
        "schema_path": ddl_path,
        "default_locale": "en-CA",
        "locales": [
            {
             "id":    1,
             "code": "en-CA"
             }
        ],
        "archive_index_data": [
            {
             "locale": "en-CA",
             "path":   None
             }
        ]
    }

    def __repr__(self):
        return '%s object code "%s"' % (self.__class__,
                                        self.cbmcfs3_country.iso2_code)

    def __init__(self, cbmcfs3_country):
        # Main attributes #
        self.cbmcfs3_country = cbmcfs3_country

    @property_cached
    def libcbm_country(self):
        """The matching libcbm country object."""
        return libcbm_continent.countries[self.cbmcfs3_country.iso2_code]

    def __call__(self, verbose=True, aidb_repo=True):
        # Get the source path #
        source = self.cbmcfs3_country.paths.aidb_eu
        # Get the destination path #
        if aidb_repo: destin = self.libcbm_country.aidb.repo_file
        else:         destin = self.libcbm_country.aidb.paths.db
        # Messages #
        if verbose:
            print("\nCountry: " + self.cbmcfs3_country.iso2_code)
            print("Source: " + source)
            print("Destination: " + destin)
            print("-------------")
        # Make a copy of the template dictionary #
        config = self.template.copy()
        # Specify paths in this dictionary #
        config['archive_index_data'][0]['path'] = source
        config['output_path'] = destin
        # Delete previous version of the database #
        destin.remove()
        # Call method in `cbm_defaults` #
        cbm_defaults.app.run(config)

###############################################################################
if __name__ == '__main__':
    # Make converter objects, one per country #
    converters = [ConvertAIDB(c) for c in cbmcfs3_continent]
    # Show which version of the repository we are using #
    print("Using %s." % cbm_defaults.app)
    print("-------------")
    # Print timer start #
    timer = Timer()
    timer.print_start()
    # Run them all #
    for converter in tqdm(converters):
        converter()
    # Print end #
    timer.print_end()
    timer.print_total_elapsed()

