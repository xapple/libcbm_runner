#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #

# Third party modules #
from libcbm_runner.pump.pre_processor import PreProcessor
from tqdm import tqdm
import pandas

# First party modules #
from autopaths.auto_paths import AutoPaths

# Internal modules #
from libcbm_runner.core.continent import continent, libcbm_data_dir

# Constants #
interface_dir = libcbm_data_dir + 'interface/'

###############################################################################
class MakeActivities(object):
    """
    This class will change the structure of the input data directory for
    each country, and set it up for the new features containing both
    activities, scenarios and combinations of the latter.

    More information is contained in the notebooks of the `bioeconomy_notes`
    repository. An example directory structure is the following:

        LU
        ├── activities
        │   ├── afforestation
        │   │   ├── events.csv
        │   │   ├── growth_curves.csv
        │   │   ├── inventory.csv
        │   │   └── transitions.csv
        │   ├── deforestation
        │   │   └── events.csv
        │   ├── mgmt
        │   │   ├── events.csv
        │   │   ├── growth_curves.csv
        │   │   ├── inventory.csv
        │   │   └── transitions.csv
        │   ├── nd_nsr
        │   │   ├── events.csv
        │   │   └── transitions.csv
        │   └── nd_sr
        │       ├── events_wide.csv
        │       └── transitions.csv
        ├── common
        │   ├── age_classes.csv
        │   ├── classifiers.csv
        │   └── disturbance_types.csv
        ├── orig
        │   ├── aidb.db -> libcbm_aidb/countries/LU/orig/config/aidb.db
        │   └── associations.csv
        └── silv
            ├── product_types.csv
            └── silvicultural_practices.csv

    It will also create symlinks to these files in a flat hierarchy, in essence
    providing a user interface to the input data which is compatible with
    Excel that has the ridiculous limitation of not being able to open two
    files with the same name.
    """

    #------------------------------ File lists -------------------------------#
    common_list = ['disturbance_types.csv', 'classifiers.csv',
                   'age_classes.csv']

    silv_list = ['product_types.csv', 'silvicultural_practices.csv']

    config_list = ['associations.csv', 'aidb.db']

    mgmt_list = ['events.csv', 'inventory.csv', 'transitions.csv',
                 'growth_curves.csv']

    #------------------------------ Autopaths --------------------------------#
    old_all_paths = """
    /orig/
    /orig/csv/
    /orig/csv/age_classes.csv        
    /orig/csv/classifiers.csv        
    /orig/csv/disturbance_types.csv  
    /orig/csv/events.csv             
    /orig/csv/inventory.csv          
    /orig/csv/transitions.csv        
    /orig/csv/growth_curves.csv      
    /orig/config/
    /orig/config/associations.csv        
    /orig/config/aidb.db       
    """

    new_all_paths = """
    /common/
    /common/age_classes.csv         
    /common/classifiers.csv         
    /common/disturbance_types.csv   
    /activities/         
    /activities/mgmt/events.csv           
    /activities/mgmt/inventory.csv        
    /activities/mgmt/transitions.csv      
    /activities/mgmt/growth_curves.csv  
    /config/
    /config/associations.csv
    /config/aidb.db       
    /silv/  
    /silv/product_types.csv
    /silv/silvicultural_practices.csv
    """

    #------------------------------- Methods ---------------------------------#
    def __repr__(self):
        return '%s object code "%s"' % (self.__class__, self.country.iso2_code)

    def __init__(self, country):
        # Default attributes #
        self.country = country
        # AutoPaths #
        self.old_paths = AutoPaths(self.country.data_dir, self.old_all_paths)
        self.new_paths = AutoPaths(self.country.data_dir, self.new_all_paths)

    def __call__(self):
        # Move existing files
        self.move_stuff()
        # Create empty files for all possible activities #
        self.create_activities()
        # Switch events files to the wide format #
        self.make_events_wide()
        # Add the scenario column to every file #
        self.add_scen_column()
        # Fix the transitions file #
        self.restore_header()
        # Makes lots of flat symlinks #
        self.make_interface()
        # Return #
        return self.country_interface_dir

    def move_stuff(self):
        # Common #
        for item in self.common_list:
            self.old_paths[item].move_to(self.new_paths[item])
        # Silv #
        for item in self.silv_list:
            self.new_paths[item].touch()
        # Config #
        for item in self.config_list:
            self.old_paths[item].move_to(self.new_paths[item])
        # Mgmt #
        for item in self.mgmt_list:
            self.old_paths[item].move_to(self.new_paths[item])
        # Remove old directories #
        self.country.data_dir.remove_empty_dirs()

    activities = ['afforestation', 'deforestation', 'mgmt', 'nd_nsr', 'nd_sr']

    def create_activities(self):
        # Other activities #
        for act in self.activities:
            if act == 'mgmt': continue
            for item in self.mgmt_list:
                directory = self.new_paths.activities_dir + act + '/'
                directory.create_if_not_exists()
                file = directory + item
                file.touch()

    def make_events_wide(self):
        # The path to the mgmt events file #
        path = self.new_paths.events
        # Read it #
        long = pandas.read_csv(str(path))
        # Get a pre-processor #
        pre_proc = PreProcessor(type('X', (), {'country': self.country}))
        # Transform it #
        wide = pre_proc.events_long_to_wide(long)
        # Write it #
        wide.to_csv(str(path), index=False)
        # Return #
        return str(path)

    def add_scen_column(self):
        # LU was already done previously #
        if self.country.iso2_code == 'LU': return
        # The files #
        files_to_be_modify = ['growth_curves',
                              'transitions',
                              'inventory']
        # Create the four dynamic files #
        for input_file in files_to_be_modify:
            # The path to the file that we will modify #
            path = self.new_paths[input_file]
            # Read the file #
            df = pandas.read_csv(str(path))
            # Add column #
            df.insert(0, 'scenario', 'reference')
            # Write output #
            df.to_csv(str(path), index=False, float_format='%g')

    #-------------------------- Post-processing -------------------------------#
    def restore_header(self):
        """
        In a pandas dataframe, the column names have to be unique, because
        they are implemented as an index. However in the file
        "transition_rules", column names are repeated. So we have to restore
        these headers afterwards.
        """
        # Read from disk #
        header = self.new_paths.transitions.first
        # Modify #
        header = header.split(',')
        header = [n.replace('.1', '') for n in header]
        header = ','.join(header)
        # Write to disk #
        self.new_paths.transitions.remove_first_line()
        self.new_paths.transitions.prepend(header)

    #------------------------- The flat symlinks ------------------------------#
    @property
    def country_interface_dir(self):
        return interface_dir + self.country.iso2_code + '/'

    def make_interface(self):
        # Create the directory #
        self.country_interface_dir.create_if_not_exists()
        # Shortcut #
        base = self.country_interface_dir + self.country.iso2_code + '_'
        # Common #
        for item in self.common_list:
            file = self.new_paths[item]
            file.link_to(base + 'config_' + file.name)
        # Silv #
        for item in self.silv_list:
            file = self.new_paths[item]
            file.link_to(base + 'config_' + file.name)
        # Config #
        for item in self.config_list:
            file = self.new_paths[item]
            file.link_to(base + 'config_' + file.name)
        # Activities #
        for subdir in self.new_paths.activities_dir.flat_directories:
            act = subdir.name
            for file in subdir.flat_files:
                file.link_to(base + act + '_' + file.name)
        # Return #
        return base

###############################################################################
if __name__ == '__main__':
    makers = [MakeActivities(c) for c in continent]
    print([maker.make_interface() for maker in tqdm(makers)])

