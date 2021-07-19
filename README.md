# `libcbm_runner` version 0.1.2

`libcbm_runner` is a python package for dealing with the automation and running of a complex series of models involving forest growth, the European economy, carbon budgets and their interactions. It uses the `libcbm` model developed by Canada under the hood.

This python module uses pandas data frames to manipulate and store most data.

## Prerequisites are `libcbm` and `libcbm_py`

`libcbm` is a C++ library with python binding developed by the Canadian Forest Service.


## Installation

Installation instructions are available for two different platforms:

* [Installation on Linux](docs/setup_on_linux.md)
* [Installation on Windows](docs/setup_on_windows.md)


## Notebooks

Some notebooks are available from the `libcbm_py` repository, in the example directory.


## Extra documentation

More documentation is available at:

<http://xapple.github.io/libcbm_runner/libcbm_runner>

This documentation is simply generated with:

    $ pdoc --html --output-dir docs --force libcbm_runner