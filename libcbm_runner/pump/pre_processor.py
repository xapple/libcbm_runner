#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #

# Third party modules #
import pandas

# First party modules #

# Internal modules #

###############################################################################
class PreProcessor(object):
    """
    This class will update the input data of a runner based on a set of rules.
    """

    def __init__(self, parent):
        # Default attributes #
        self.parent = parent
        self.runner = parent
        # Shortcuts #
        self.input  = self.runner.input_data

    def __repr__(self):
        return '%s object code "%s"' % (self.__class__, self.runner.short_name)

    #--------------------------- Special Methods -----------------------------#
    def __call__(self):
        # Message #
        self.parent.log.info("Pre-processing input data.")
        # Check empty lines in all inputs #
        for item in self.input.paths._paths:
            csv_path = item.path_obj
            if csv_path.extension != 'csv': continue
            self.raise_empty_lines(csv_path)

    #------------------------------- Methods ---------------------------------#
    @staticmethod
    def raise_empty_lines(csv_path):
        """
        Loads one CSV files and raise an exception if there are any empty
        lines.
        """
        # Load from disk #
        df = pandas.read_csv(str(csv_path))
        # Get empty lines #
        empty_lines = df.isnull().all(1)
        # Check if there are any #
        if not any(empty_lines): return
        # Warn #
        msg = "The file '%s' has %i empty lines."
        raise Exception(msg % (csv_path, empty_lines.sum()))
