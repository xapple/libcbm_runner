#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #

# Third party modules #

# First party modules #

# Internal modules #

###############################################################################
class InternalData(object):
    """
    This class will provide access to the data of a simulation as it is
    running as several pandas data frames.
    """

    def __init__(self, parent):
        # Default attributes #
        self.parent = parent
        self.runner = parent
        self.sim    = self.runner.simulation

    def __repr__(self):
        return '%s object code "%s"' % (self.__class__, self.runner.short_name)

    #----------------------------- Properties --------------------------------#
    @property
    def classif_df(self):
        return self.make_classif_df(self.sim.sit.classifier_value_ids,
                                    self.sim.results.classifiers)

    #------------------------------- Methods ---------------------------------#
    def make_classif_df(self, vals, clfrs):
        """
        Produces a dataframe useful for joining classifier values to
        other output dataframes. This dataframe looks like this:

                  identifier timestep Status Forest type Region ...
            0              1        0    For          OB   LU00 ...
            1              2        0    For          OB   LU00 ...
            2              3        0    For          OB   LU00 ...
        """
        # Invert dictionary #
        vals = {v: k for m in vals.values() for k, v in m.items()}
        # Put actual values such as 'For' instead of numbers like '6' #
        clfrs = clfrs.set_index(['identifier', 'timestep'])
        clfrs = clfrs.replace(vals)
        clfrs = clfrs.reset_index()
        # Return #
        return clfrs