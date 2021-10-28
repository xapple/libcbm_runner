# Installation

This guide shows how to set up the `libcbm_data` and `libcbm_runner` projects together on a fresh Ubuntu system to run the 26 EU carbon budget simulations with `libcbm_py` automatically.

## Fresh OS

In this guide we will be using an "Ubuntu Server 20 LTS" operating system. Specifically we will have tested the commands with the pre-made AMI image offered by the EC2 service from Amazon. We used the x86 image version (not ARM). Still, this should work the same on more or less any Linux distribution.

## Clone repos

The first step is to clone the needed git repositories. We will clone all the projects inside a directory at `~/repos/`.

    $ cd ~
    $ mkdir repos
    $ cd repos
    $ git clone git@github.com:cat-cfs/libcbm_py.git
    $ git clone https://gitlab.com/bioeconomy/libcbm/libcbm_runner.git
    $ git clone https://gitlab.com/bioeconomy/libcbm/libcbm_data.git

## The EU AIDB

Next, we must obtain a copy the European "cbm_defaults" sqlite3 database. As it's a bit larger, it's not included in the `libcbm_data` repository. Instead, it's in a standalone one.

    $ git clone git@gitlab.com:bioeconomy/libcbm/libcbm_aidb.git

 To link to those aidb inside `libcbm_data` use the `symlink_all_aidb` method provided in `libcbm_runner/pump/aidb.py`.

 This temporary solution with a single AIDB for each country is meant to be changed once the AIDBs have been harmonized to a single AIDB for all countries.

## Install pip

The modules we have developed rely on some third party (as well as first party) packages that you can install easily with `pip`. However, you first need to run a few commands to get `pip` itself as it's not included by default.

    $ sudo apt update
    $ sudo apt install python3-pip

## Install python modules

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
    export LIBCBM_AIDB="$HOME/repos/libcbm_aidb/"

## Run one country

Run a given country from the historical scenario.

You can use these commands in python:

    >>> from libcbm_runner.core.continent import continent
    >>> scenario = continent.scenarios['historical']
    >>> runner_libcbm = scenario.runners['LU'][-1]
    >>> runner_libcbm.run(keep_in_ram=True, verbose=True, interrupt_on_error=True)

## Run all countries

To run a full scenario, proceed as so:

     >>> from libcbm_runner.core.continent import continent
     >>> scen = continent.scenarios['historical']
     >>> scen()