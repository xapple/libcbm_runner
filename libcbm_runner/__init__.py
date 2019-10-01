#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC biomass Project.
Unit D1 Bioeconomy.
"""

# Special variables #
__version__ = '0.1.0'

# Built-in modules #
import os, sys

# First party modules #
from autopaths import Path
from plumbing.git import GitRepo

# Constants #
project_name = 'libcbm_runner'
project_url  = 'https://github.com/xapple/libcbm_runner'

# Get paths to module #
self       = sys.modules[__name__]
module_dir = Path(os.path.dirname(self.__file__))

# The repository directory #
repos_dir = module_dir.directory

# The module is maybe in a git repository #
git_repo = GitRepo(repos_dir, empty=True)
