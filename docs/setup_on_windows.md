# Installation

Setup of `libcbm_data` and `libcbm_runner`

This guide shows how to set up the `libcbm_data` and `libcbm_runner` projects together on a Windows system to run the 26 EU carbon budget simulations with `libcbm_py` automatically.

## Clone repos

The first step is to clone the needed git repositories, using the git bash command line 
for example.

    cd C:\CBM
    git clone https://github.com/cat-cfs/libcbm_py.git
    git clone git@gitlab.com:bioeconomy/libcbm/libcbm_runner.git
    git clone git@gitlab.com:bioeconomy/libcbm/libcbm_data.git


## Install python modules

The modules we have developed rely on some third party (as well as first party) packages that you can install easily with `pip`. 

INstall the various modules These modules themselves have dependencies that will be auto-installed.

    pip install autopaths
    pip install plumbing
    pip install simplejson
    pip install numexpr
    pip install tqdm
    pip install p_tqdm

Pip is likely to already be on your system if you have anaconda installed. However, if
that is not the case, you first need to run a few commands to get `pip` itself:

    curl -O https://bootstrap.pypa.io/get-pip.py
    python3 get-pip.py --user


## Define environment variables

Please define the environment variables as system wide. Otherwise the script that
creates the symbolic links for the AIDB will fail because of a lack of user permissions to
create symlinks. It seems that on some system, administrative permissions are required
to create symlinks.

In the windows start menu environmental variables. The next step is to set the
environment variable `$PYTHONPATH` so that our interpreter can find the repositories we
just cloned. 

In the Windows environment variables setting, the python path should be modified to:

    PYTHONPATH = C:\CBM\libcbm_py
    PYTHONPATH = C:\CBM\libcbm_runner

In fact when editing from the text box, enter the previous two separated by a semicolon
`;` as such: C:\CBM\libcbm_py;C:\CBM\libcbm_runner

Next, a new environmental variable should be added:

    LIBCBM_DATA = C:\CBM\libcbm_data
    AIDB_REPO = c\CBM\libcbm_aidb

Note: you need to restart the console, or the Anaconda environment so that the
environment variables get updated from the system. You can check that the variables
where defined correctly by entering the following commands from a windows command prompt

    echo %PYTHONPATH%
    echo %LIBCBM_DATA%
    echo %AIDB_REPO%


## Link the EU AIDB into libcbm_data

Next, we must obtain a copy the European "cbm_defaults" sqlite3 database. As it's a bit 
larger, it's not included in the `libcbm_data` repository. Instead, it's in a standalone 
one. 

    git clone git@gitlab.com:bioeconomy/libcbm/libcbm_aidb.git

To create symbolic links to the AIDB, you need to run the following as administrator
right click on the conda console and click run as administrator.

    ipython -i -- c:\users\rober\CBM\libcbm_runner\scripts\setup\aidb_symlink.py 

To open the AIDB install the SQLite browser software at
[sqlitebrowser.org](https://sqlitebrowser.org/dl/).
The AIDB tables can also be read by python, using for example the 


## Run the libcbm model

You should now be ready to run the pipeline by entering the following at the python 
console:

    from libcbm_runner.core.continent import continent
    scenario = continent.scenarios['historical']
    runner_libcbm = scenario.runners['LU'][-1]
    runner_libcbm.run(keep_in_ram=True, verbose=True, interrupt_on_error=True)

Alternatively

    $ python3 ~/repos/libcbm_runner/scripts/running/run_zz.py


## Load output data

Load tables without classifiers

    area_lu = runner_libcbm.output.load('area', with_clfrs=False)
    params_lu = runner_libcbm.output.load('params', with_clfrs=False)
    flux_lu = runner_libcbm.output.load('flux', with_clfrs=False)
    state_lu = runner_libcbm.output.load('state', with_clfrs=False)

Load classifiers with their actual values and print the number of rows

    classifiers_lu = runner_libcbm.output.classif_df
    print(f"No of rows in area_lu: {len(area_lu)}")
    print(f" No of rows in flux_lu, with NaNs for timestep 0: {len(flux_lu)}")
    print(f"No of rows in params_lu: {len(params_lu)}")

Join area, age and fluxes together

    index = ['identifier', 'timestep']
    flux_dist = (params_lu
                 .merge(area_lu, 'left', on = index) # Join the area information
                 .merge(flux_lu, 'left', on = index)
                 .merge(state_lu, 'left', on = index) # Join the age information
                 .merge(classifiers_lu, 'left', on = index) # Join the classifiers
                 )
    len(flux_dist)
    flux_dist

