#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #

# Third party modules #

# First party modules #

# Internal modules #

###############################################################################
class PostProcessor(object):
    """
    This class will xxxx.
    """

    def __init__(self, parent):
        # Default attributes #
        self.parent = parent
        self.runner = parent

    def __repr__(self):
        return '%s object code "%s"' % (self.__class__, self.runner.short_name)

    def __call__(self):
        """
        xxxx.
        """
        return
        # Message #
        self.parent.log.info("Post-processing results.")
        # Lorem #
        pass