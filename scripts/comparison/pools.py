#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A script.
"""

# Built-in modules #
import socket, textwrap

# Third party modules #
from tqdm import tqdm

# First party modules #
from autopaths.dir_path   import DirectoryPath
from autopaths.file_path  import FilePath
from autopaths.auto_paths import AutoPaths
from plumbing.cache       import property_cached

# Internal modules #
from libcbm_runner.core.continent import continent as libcbm_continent

# Continents #
from cbmcfs3_runner.core.continent import continent as cbmcfs3_continent

###############################################################################
class ComparisonRunner(object):
    """
    This class can compare the results of european forest simulations
    between the new `libcbm` libarary and the old windows CBM-CFS3 software.

    To access the results instead of doing:

        >>> pools_libcbm_wide = runner_libcbm.simulation.results.pools

    You can do:

        >>> pools_libcbm_wide = runner_libcbm.output['pools']

    To check the number of pools:

        >>> pools_libcbm['pool'].unique()

    To use this class you can do:

        >>> import os
        >>> home = os.environ.get('HOME', '~') + '/'
        >>> from importlib.machinery import SourceFileLoader
        >>> path = home + 'repos/libcbm_runner/scripts/comparison/pools.py'
        >>> comp = SourceFileLoader('pools', path).load_module()
        >>> from cbmcfs3_runner.core.continent import continent
        >>> comps = [comp.ComparisonRunner(c) for c in continent]
        >>> c = comps[17]
        >>> display(c.pools_cbmcfs3)
        >>> display(c.pools_libcbm)
    """

    all_paths = """
    /comp/pools.md
    """

    def __init__(self, cbmcfs3_country):
        # Main attributes #
        self.cbmcfs3_country = cbmcfs3_country
        # Shortcuts #
        self.iso2_code = cbmcfs3_country.iso2_code
        # Where the data will be stored for this comparison #
        self.base_dir = self.cbmcfs3_country.data_dir
        # Automatically access paths based on a string of many subpaths #
        self.paths = AutoPaths(self.base_dir, self.all_paths)

    def __repr__(self):
        return '%s object code "%s"' % (self.__class__, self.iso2_code)

    #----------------------------- Properties --------------------------------#
    @property_cached
    def libcbm_country(self):
        """The matching libcbm country object."""
        return libcbm_continent.countries[self.cbmcfs3_country.iso2_code]

    @property
    def title(self):
        msg = "# %s (%s)\n"
        msg = msg % (self.cbmcfs3_country.country_name, self.iso2_code)
        msg = msg + "## Comparing libcbm -vs- cbmcfs3 \n\n"
        return msg

    #--------- Scenarios ----------#
    @property
    def scen_cbmcfs3(self):
        return cbmcfs3_continent.scenarios['static_demand']

    @property
    def scen_libcbm(self):
        return libcbm_continent.scenarios['historical']

    #---------- Runners -----------#
    @property
    def runner_cbmcfs3(self):
        return self.scen_cbmcfs3[self.iso2_code][-1]

    @property
    def runner_libcbm(self):
        return self.scen_libcbm[self.iso2_code][-1]

    #----------- Pools ------------#
    @property
    def pools_cbmcfs3(self):
        # Load #
        post_proc = self.runner_cbmcfs3.post_processor
        result    = post_proc.pool_indicators_long
        # Rename columns #
        result = result.rename(columns={'time_step': 'timestep'})
        # Return #
        return result

    @property
    def pools_libcbm(self):
        # Load #
        result  = self.runner_libcbm.output['pools']
        id_vars = ['identifier', 'timestep', 'area']
        # Unpivot #
        result = result.melt(id_vars    = id_vars,
                             var_name   = 'pool',
                             value_name = 'tc')
        # Return #
        return result

    #----------- Joined ------------#
    sorted = True
    @property_cached
    def df(self):
        # Load #
        cbmcfs3 = self.pools_cbmcfs3
        libcbm  = self.pools_libcbm
        # Filter years from cbmcfs3 #
        max_timestep = libcbm['timestep'].max()
        cbmcfs3 = cbmcfs3.query(f"timestep <= {max_timestep}")
        # Aggregate both into total carbon, abbreviated `tc` #
        libcbm  = libcbm.groupby(['pool', 'timestep'])
        libcbm  = libcbm.agg(tc_libcbm=('tc', sum), area=('area', sum))
        libcbm  = libcbm.reset_index()
        cbmcfs3 = cbmcfs3.groupby(['pool', 'timestep'])
        cbmcfs3 = cbmcfs3.agg(tc_cbmcfs3=('tc', sum))
        cbmcfs3 = cbmcfs3.reset_index()
        # Load the mapping of the pools names between the two versions #
        from cbmcfs3_runner.pump.libcbm_mapping import libcbm_mapping
        name_map = libcbm_mapping[['libcbm', 'cbmcfs3']]
        name_map = name_map.rename(columns={'libcbm':  'pool_libcbm'})
        name_map = name_map.rename(columns={'cbmcfs3': 'pool_cbmcfs3'})
        # Add the mapping of the pools to libcbm #
        libcbm = libcbm.rename(columns={'pool': 'pool_libcbm'})
        # Add the mapping of the pools to cbmcfs3 #
        cbmcfs3 = cbmcfs3.rename(columns={'pool': 'pool_cbmcfs3'})
        cbmcfs3 = cbmcfs3.merge(name_map, 'left', 'pool_cbmcfs3')
        # Join #
        df = libcbm.merge(cbmcfs3, 'outer', ['pool_libcbm', 'timestep'])
        # Drop rows if any NaN values in two columns #
        df = df.dropna(subset=['pool_libcbm', 'pool_cbmcfs3'])
        # Drop rows if both carbon totals are zero #
        both_zeros = (df['tc_cbmcfs3'] == 0) & (df['tc_libcbm'] == 0)
        df = df.drop(both_zeros.index)
        # Compute difference between the two models #
        df['tc_diff_tot'] = df['tc_libcbm'] - df['tc_cbmcfs3']
        # Add a column showing the mass per hectare for libcbm values #
        df['tc_per_ha'] = df['tc_libcbm'] / df['area']
        # Compute per hectare total difference #
        df['tc_diff_per_ha'] = df['tc_diff_tot'] / df['area']
        # Compute proportion in percent #
        df['diff_perc'] = 100 * ((df['tc_libcbm'] / df['tc_cbmcfs3']) - 1)
        # Optionally sort based on the proportion #
        if self.sorted: df = df.sort_values('tc_per_ha', ascending=False)
        # If both the percent diff and absolute diff are both high, mark it #
        df['problems'] = (df['tc_diff_tot'] > 1) & (df['diff_perc'] > 1)
        df['problems'] = df['problems'].replace({False: '', True: '**'})
        # Return #
        return df

    #------------------------------- Methods ---------------------------------#
    def __call__(self):
        with self.paths.pools.open('w') as handle:
            # Make a nice title #
            handle.write(self.title)
            # Loop over every timestep #
            for i, group in self.df.groupby('timestep'):
                handle.write("### Time step %s\n" % i)
                data = group.to_string(index=False, float_format='%.2f')
                data = textwrap.indent(data, '    ')
                handle.write(data + '\n')
        # Return #
        return self.paths.pools

###############################################################################
class Bundle:
    """
    A bundle object will regroup various result files into a single zip file
    useful for delivery and distribution.
    Once the bundle is ready, you can simply download it to your local
    computer with a simple rsync command.
    """

    def __init__(self, comps, base_dir, archive=None):
        # The objects to keep #
        self.comparisons = comps
        # Where the results will be aggregated #
        self.base_dir = DirectoryPath(base_dir)
        # Default if none specified #
        if archive is None: archive = self.base_dir.path[:-1] + '.zip'
        # Where the zip archive will be placed #
        self.archive = FilePath(archive)

    #------------------------------- Methods ---------------------------------#
    def __call__(self, verbose=True):
        # Remove the directory if it was created previously #
        self.base_dir.remove()
        self.base_dir.create()
        # Loop every country #
        for c in self.comparisons:
            c.paths.pools.copy(self.base_dir + c.iso2_code + '.md')
        # Zip it #
        self.base_dir.zip_to(self.archive)
        # Remove the directory #
        self.base_dir.remove()
        # Return #
        return self.archive

    #----------------------------- Properties --------------------------------#
    @property_cached
    def rsync(self):
        """
        Will return an rsync bash command as a string that can be later used
        to easily download the bundle.
        """
        # Get the hostname #
        host = socket.gethostname()
        # Make the command #
        cmd = 'rsync -avz %s:%s ~/Downloads/%s'
        cmd = cmd % (host, self.archive, self.archive.name)
        # Return #
        return cmd

###############################################################################
if __name__ == '__main__':
    # Skip these countries #
    skip = ['GB', 'ZZ']
    # Make comparisons objects, one per country #
    comparisons = [ComparisonRunner(c) for c in cbmcfs3_continent
                   if c.iso2_code not in skip]
    # Run them all #
    for compare in tqdm(comparisons): compare()
    # Bundle them #
    bundle = Bundle(comparisons, '~/test/libcbm_comp/')
    bundle()
    # Print result #
    print("\nDone.")
    print("You can get the results with the following command:")
    print(bundle.rsync)
