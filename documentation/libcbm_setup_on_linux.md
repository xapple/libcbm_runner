

# Installation

## Installation of libcbm and libcbm_py

libcbm is a C++ library with python binding developed by the Canadian Forest Service.
The python module uses pandas data frames to manipulate data.


## Setup of `libcbm_data` and `libcbm_runner`

This guide shows how to setup the `libcbm_data` and `libcbm_runner` projects together on a fresh Ubuntu system so as to run the 26 EU carbon budget simulations with `libcbm_py` automatically.

## Fresh OS

In this guide we will be using an "Ubuntu Server 18.04 LTS" operating system. Specifically we will have tested the commands with the pre-made AMI image offered by the EC2 service from Amazon. The exact reference on AWS is "ami-02df9ea15c1778c9c". This is the x86 image version (not ARM). Still, this should work the same on more or less any Linux distribution.

## Clone repos

The first step is to clone the needed git repositories. We will clone all the projects inside a directory at `~/repos/`.

    $ cd ~
    $ mkdir repos
    $ cd repos
    $ git clone git@github.com:cat-cfs/libcbm_py.git
    $ git clone git@gitlab.com:bioeconomy/libcbm/libcbm_runner.git
    $ git clone git@gitlab.com:bioeconomy/libcbm/libcbm_data.git

## The EU AIDB

Next, we must obtain a copy the europeean cbm_defaults sqlite database. As it's a bit larger, it's not included in the libcbm_data repository. Instead, it's in a standalone one.

    $ git clone git@gitlab.com:bioeconomy/libcbm/libcbm_aidb.git
    $ ln -s ~/repos/libcbm_aidb/aidb.db  ~/repos/libcbm_data/countries/ZZ/orig/config/aidb.db

## Install pip

The modules we have developed rely on some third party (as well as first party) packages that you can install easily with `pip`. However, you first need to run a few commands to get `pip` itself as it's not included by default.

    $ sudo apt-get install python3-distutils
    $ curl -O https://bootstrap.pypa.io/get-pip.py
    $ python3 get-pip.py --user

## Install dependencies

These modules themselves have dependencies that will be auto-installed, so although there is just two commands, you will end up installing many more packages.

    $ python3 -m pip install --user autopaths
    $ python3 -m pip install --user plumbing
    $ python3 -m pip install --user simplejson

## Paths variables

The next step is to set the environment variable `$PYTHONPATH` so that our interpreter can find the repositories we just cloned. We will edit the `~/.profile` file and add these lines to it:

    export PYTHONPATH="$HOME/repos/libcbm_py/":$PYTHONPATH
    export PYTHONPATH="$HOME/repos/libcbm_runner/":$PYTHONPATH
    export LIBCBM_DATA="$HOME/repos/libcbm_data/"

## Run

You should now be ready to run the pipeline with the following command:

    $ python3 ~/repos/libcbm_runner/scripts/running/run_zz.py

This will likely result in an error message and the production of a traceback, as the pipeline is still under heavy development.
