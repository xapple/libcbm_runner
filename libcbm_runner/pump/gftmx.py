#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Paul Rougieux, Lucas Sinclair

JRC biomass Project.
Unit D1 Bioeconomy.

Usage:

    >>> from libcbm_runner.pump.gftmx import gftmx
    >>> print(gftmx.industrial_roundwood_demand)
    >>> print(gftmx.fuelwood_demand)

"""

# First party modules
from pathlib import Path

# Third party modules
import pandas

# Internal modules
from libcbm_runner import libcbm_data_dir


class Gftmx:
    """
    Demand from the economic model

    The demand from the perspective of the forest dynamics model is the
    production from the perspective of the economic model.
    """

    # Location of the data
    data_dir = Path(libcbm_data_dir) / "common/gftmx"

    @property
    def industrial_roundwood_demand(self):
        """Industrial roundwood demand"""

        return pandas.read_csv(self.data_dir / "indroundprod.csv")

    @property
    def fuelwood_demand(self):
        """Fuelwood demand"""
        return pandas.read_csv(self.data_dir / "fuelprod.csv")

# Make a singleton #
gftmx = Gftmx()
