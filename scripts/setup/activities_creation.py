#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #
import os

# Third party modules #
from tqdm import tqdm
import pandas

# First party modules #
from autopaths.auto_paths import AutoPaths

# Internal modules #
from libcbm_runner                    import libcbm_data_dir
from libcbm_runner.core.continent     import continent
from libcbm_runner.pump.long_or_wide  import events_long_to_wide
from libcbm_runner.pump.pre_processor import PreProcessor

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

        ZZ
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
        │   ├── aidb.db -> libcbm_aidb/countries/ZZ/orig/config/aidb.db
        │   └── associations.csv
        └── silv
            ├── product_types.csv
            └── silvicultural_practices.csv
    """

    #------------------------------ File lists -------------------------------#
    common_list = ['disturbance_types.csv', 'classifiers.csv',
                   'age_classes.csv']

    silv_list = ['product_types.csv', 'silvicultural_practices.csv']

    config_list = ['associations.csv', 'aidb.db']

    mgmt_list = ['events.csv', 'inventory.csv', 'transitions.csv',
                 'growth_curves.csv']

    activities = ['afforestation', 'deforestation', 'mgmt', 'nd_nsr', 'nd_sr']

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

    #--------------------------- Special Methods -----------------------------#
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

    #------------------------------- Methods ---------------------------------#
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
        wide = events_long_to_wide(self.country, long)
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

    def restore_header(self):
        """
        In a pandas dataframe, the column names have to be unique, because
        they are implemented as an index. However in the file
        "transition_rules.csv", column names are repeated.
        So we have to restore these headers afterwards.
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

    #------------------------- The flat symlinks -----------------------------#
    @property
    def country_interface_dir(self):
        return interface_dir + self.country.iso2_code + '/'

    @property
    def interface_base(self):
        return  self.country_interface_dir + self.country.iso2_code + '_'

    def make_interface(self, hardlinks=True, debug=False):
        """
        This method can create symlinks to the input files in a flat hierarchy,
        in essence providing a user interface to the input data.

        This was originally developed to be compatible with Excel. The Excel
        software has the ridiculous limitation of not being able to open two
        files with the same name.

        Moreover, in the case of windows, symbolic links don't overcome this
        limitation and Excel still complains when it opens two symbolic links
        that point to different files.

        This issue is not fixed by using hard links instead of symbolic links.
        This is because Excel never modifies a given file. When saving, it
        creates a temporary file in the same directory, then deletes the
        original file and renames the temporary file to the name of the
        original file. This destroys the hard links upon every save operation.
        """
        # Create the directory #
        self.country_interface_dir.create_if_not_exists()
        # Same case for all of: "Common, Silv, Config" #
        for item in self.common_list + self.silv_list + self.config_list:
            file = self.new_paths[item]
            dest = self.interface_base + 'config_' + file.name
            dest.remove()
            if debug: print(str(file), " -> ", str(dest))
            if hardlinks: os.link(str(file), str(dest))
            else:                 file.link_to(dest)
        # Different case for "Activities" #
        for subdir in self.new_paths.activities_dir.flat_directories:
            act = subdir.name
            for file in subdir.flat_files:
                dest = self.interface_base + act + '_' + file.name
                dest.remove()
                if debug: print(str(file), " -> ", str(dest))
                if hardlinks: os.link(str(file), str(dest))
                else:                 file.link_to(dest)
        # Return #
        return self.interface_base

    #------------------------ Copying files back -----------------------------#
    def save_interface(self, debug=False):
        """
        In the end, the only way to make this `interface` work is to have a
        script copy every file in the flat hierarchy back to it's expected
        place within the `libcbm_data` repository.
        """
        # Same case for all of: "Common, Silv, Config" #
        for item in self.common_list + self.silv_list + self.config_list:
            file = self.new_paths[item]
            source = self.interface_base + 'config_' + file.name
            if debug: print(str(source), " -> ", str(file))
            source.copy_to(file)
        # Different case for "Activities" #
        for subdir in self.new_paths.activities_dir.flat_directories:
            act = subdir.name
            for file in subdir.flat_files:
                source = self.interface_base + act + '_' + file.name
                if debug: print(str(source), " -> ", str(file))
                source.copy_to(file)
        # Return #
        return self.interface_base

###############################################################################
makers = [MakeActivities(c) for c in continent]
if __name__ == '__main__': print([maker() for maker in tqdm(makers)])

