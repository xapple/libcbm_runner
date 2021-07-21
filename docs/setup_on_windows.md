# Installation

## Setup of `libcbm_data` and `libcbm_runner`

This guide shows how to set up the `libcbm_data` and `libcbm_runner` projects together on a Windows system to run the 26 EU carbon budget simulations with `libcbm_py` automatically.

## Clone repos

The first step is to clone the needed git repositories.

    cd C:\CBM
    git clone git@github.com:cat-cfs/libcbm_py.git
    git clone git@github.com:xapple/libcbm_runner.git
    git clone git@github.com:xapple/libcbm_data.git

## The EU AIDB

Next, we must obtain a copy the European "cbm_defaults" sqlite3 database. As it's a bit larger, it's not included in the `libcbm_data` repository. Instead, it's in a standalone one.

    git clone git@gitlab.com:bioeconomy/libcbm/libcbm_aidb.git

## Install pip

The modules we have developed rely on some third party (as well as first party) packages that you can install easily with `pip`. However, you first need to run a few commands to get `pip` itself as it's not included by default.

    curl -O https://bootstrap.pypa.io/get-pip.py
    python3 get-pip.py --user

## Install dependencies

These modules themselves have dependencies that will be auto-installed.

    python3 -m pip install autopaths
    python3 -m pip install plumbing
    python3 -m pip install simplejson
    python3 -m pip install numexpr
    python3 -m pip install tqdm

## Environment variables

The next step is to set the environment variable `$PYTHONPATH` so that our interpreter can find the repositories we just cloned. 

In the Windows environment variables setting, the python path should be modified to:

    PYTHONPATH = C:\CBM\libcbm_py
    PYTHONPATH = C:\CBM\libcbm_runner

Next, a new environmental variable should be added:

    LIBCBM_DATA = C:\CBM\libcbm_data

## Run

You should now be ready to run the pipeline with the script located at

    /libcbm_runner/scripts/running/run_zz.py

This will likely result in an error message and the production of a traceback, as the pipeline is still under heavy development.
