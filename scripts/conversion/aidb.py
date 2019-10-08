#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you would run this file from a command line like this:

     ipython3.exe -i -- /deploy/libcbm_runner/scripts/conversion/aidb.py
"""

# Built-in modules #

# Third party modules #
from tqdm import tqdm

# First party modules #
import cbm_defaults.app
from plumbing.cache import property_cached

# Internal modules #
from libcbm_runner.core.continent import continent as libcbm_continent

# Continents #
from cbmcfs3_runner.core.continent import continent as cbmcfs3_continent

###############################################################################
class ConvertAIDB(object):
    """
    This class will enable us to convert the old AIDB format (Access DB)
    from CBMCFS3 to an SQLITE3 database compatible with libcbm.
    """

    template = {
        "output_path": None,
        "schema_path": "/deploy/cbm_defaults/schema/cbmDefaults.ddl",
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

    def __init__(self, cbmcfs3_country):
        # Main attributes #
        self.cbmcfs3_country = cbmcfs3_country

    @property_cached
    def libcbm_country(self):
        """The matching libcbm country object."""
        return libcbm_continent.countries[self.cbmcfs3_country.iso2_code]

    def __call__(self):
        # Make a copy of the template #
        config = self.template.copy()
        # Specify paths #
        config['output_path'] = self.libcbm_country.aidb.paths.db
        config['archive_index_data'][0]['path'] = self.cbmcfs3_country.paths.aidb_eu
        # Delete previous version of the db
        self.libcbm_country.aidb.paths.db.remove()
        # Call script #
        cbm_defaults.app.run(config)

###############################################################################
if __name__ == '__main__':
    # Make yield objects #
    converters = [ConvertAIDB(c) for c in cbmcfs3_continent]
    # Run them #
    for converter in tqdm(converters):
        if converter.cbmcfs3_country.iso2_code != 'ZZ': continue
        converter()



