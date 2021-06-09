# `libcbm_data`

A repository to contain the raw data in CSV format for each country and each scenario intended for `libcbm_runner` runs.

# Installation

## Installation of libcbm and libcbm_py

libcbm is a C++ library with python binding developed by the Canadian Forest Service.
The python module uses pandas data frames to manipulate data.


## Setup of `libcbm_data` and `libcbm_runner`

This guide shows how to setup the `libcbm_data` and `libcbm_runner` projects together on 
a Windows system so as to run the 26 EU carbon budget simulations with `libcbm_py` 
automatically.


## Clone repos

The first step is to clone the needed git repositories. We will clone all the projects inside a directory at `~/repos/`.

      cd C:\CBM
      git clone git@github.com:cat-cfs/libcbm_py.git
      git clone git@github.com:xapple/libcbm_runner.git
      git clone git@github.com:xapple/libcbm_data.git

## The EU AIDB

Next, we must obtain a copy the europeean cbm_defaults sqlite database. As it's a bit 
larger, it's not included in the libcbm_data repository. Instead, it's in a stand alone 
one. `/libcbm_aidb/aidb.db` is an SQLITE database.

      git clone git@github.com:xapple/libcbm_aidb.git

Then copy the AIDB to the folder (because there are no symbolic links on windows)


      cp C:\CBM/libcbm_aidb/aidb.db  C:\CBM/libcbm_data/countries/ZZ/orig/config/aidb.db

## Install pip

The modules we have developed rely on some third party (as well as first party) packages that you can install easily with `pip`. However, you first need to run a few commands to get `pip` itself as it's not included by default.

      sudo apt-get install python3-distutils
      curl -O https://bootstrap.pypa.io/get-pip.py
      python3 get-pip.py --user

## Install dependencies

These modules themselves have dependencies that will be auto-installed, so although there is just two commands, you will end up installing many more packages.

      python3 -m pip install --user autopaths
      python3 -m pip install --user plumbing
      python3 -m pip install --user simplejson


## Environment variables

The next step is to set the environment variable `$PYTHONPATH` so that our interpreter can find the repositories we just cloned. 

When installed in C:\CBM

In the windows environment variables setting, the python path should be modified to:

    PYTHONPATH = C:\CBM\libcbm_py
    PYTHONPATH = C:\CBM\libcbm_runner

And a new environmental variable should be added:

    LIBCBM_DATA = C:\CBM\libcbm_data


# Run

You should now be ready to run the pipeline with the script located at

    /libcbm_runner/scripts/running/run_zz.py


# Notebooks

Some notebooks are available from the `libcbm_py` repository, in the example folder.


