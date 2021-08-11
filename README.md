# `libcbm_runner` version 0.2.2

`libcbm_runner` is a python package for dealing with the automation and running of a complex series of models involving forest growth, the European economy, carbon budgets and their interactions. It uses the `libcbm` model developed by Canada under the hood.

This python module uses pandas data frames to manipulate and store most data.


## Dependencies

* `libcbm` is a C++ library with python binding developed by the Canadian Forest Service. It is bundled into the libcbm_py python package available at https://github.com/cat-cfs/libcbm_py

* `libcbm_data` contains the model's input and output data located at https://gitlab.com/bioeconomy/libcbm/libcbm_data

* `libcbm_aidb` contains the "Archive Index Databases" in a separate repository located at https://github.com/xapple/libcbm_aidb to link to those aidb inside `libcbm_data` use the `symlink_all_aidb` method provided in `libcbm_runner/pump/aidb.py`. This temporary solution with a single AIDB for each country is meant to be changed once the AIDBs have been harmonized to a single AIDB for all countries. Alternatively, one can create symbolic links with `cp -rs ~/rp/libcbm_aidb/countries/ ~/rp/libcbm_data/`.


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
