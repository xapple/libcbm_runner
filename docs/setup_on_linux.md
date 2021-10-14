# Installation

Setup of `libcbm_data` and `libcbm_runner`

This guide shows how to set up the `libcbm_data` and `libcbm_runner` projects together on a fresh Ubuntu system to run the 26 EU carbon budget simulations with `libcbm_py` automatically.

## Fresh OS

In this guide we will be using an "Ubuntu Server 20 LTS" operating system. Specifically we will have tested the commands with the pre-made AMI image offered by the EC2 service from Amazon. We used the x86 image version (not ARM). Still, this should work the same on more or less any Linux distribution.

## Clone repos

The first step is to clone the needed git repositories. We will clone all the projects inside a directory at `~/repos/`.

    $ cd ~
    $ mkdir repos
    $ cd repos
    $ git clone git@github.com:cat-cfs/libcbm_py.git
    $ git clone git@github.com:xapple/libcbm_runner.git
    $ git clone git@github.com:xapple/libcbm_data.git

## The EU AIDB

Next, we must obtain a copy the European "cbm_defaults" sqlite3 database. As it's a bit larger, it's not included in the `libcbm_data` repository. Instead, it's in a standalone one.

    $ git clone git@gitlab.com:bioeconomy/libcbm/libcbm_aidb.git

## Install pip

The modules we have developed rely on some third party (as well as first party) packages that you can install easily with `pip`. However, you first need to run a few commands to get `pip` itself as it's not included by default.

    $ sudo apt update
    $ sudo apt install python3-pip

## Install dependencies

These modules themselves have dependencies that will be auto-installed.

    $ python3 -m pip install autopaths
    $ python3 -m pip install plumbing
    $ python3 -m pip install simplejson
    $ python3 -m pip install numexpr
    $ python3 -m pip install tqdm

## Environment variables

The next step is to set the environment variable `$PYTHONPATH` so that our interpreter can find the repositories we just cloned. We will edit the `~/.profile` file and add these lines to it:

    export PYTHONPATH="$HOME/repos/libcbm_py/":$PYTHONPATH
    export PYTHONPATH="$HOME/repos/libcbm_runner/":$PYTHONPATH
    export LIBCBM_DATA="$HOME/repos/libcbm_data/"

## Run

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

