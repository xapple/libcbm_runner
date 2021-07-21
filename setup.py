#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC biomass Project.
Unit D1 Bioeconomy.
"""

# Imports #
from setuptools import setup, find_namespace_packages
from os import path

# Load the contents of the README file #
this_dir = path.abspath(path.dirname(__file__))
readme_path = path.join(this_dir, 'README.md')
with open(readme_path, encoding='utf-8') as handle: readme = handle.read()

# Call setup #
setup(
    name             = 'libcbm_runner',
    version          = '0.2.0',
    description      = 'libcbm_runner is a python package for running carbon'
                       ' budget simulations.',
    license          = 'MIT',
    url              = 'https://github.com/xapple/libcbm_runner',
    author           = 'Lucas Sinclair',
    author_email     = 'lucas.sinclair@me.com',
    packages         = find_namespace_packages(),
    install_requires = ['autopaths>=1.5.2', 'plumbing>=2.10.4',
                        'pymarktex>=1.4.6', 'pandas', 'pystache', 'simplejson',
                        'matplotlib', 'tqdm', 'p_tqdm'],
    python_requires  = ">=3.8",
    long_description = readme,
    long_description_content_type = 'text/markdown',
    include_package_data = True,
)