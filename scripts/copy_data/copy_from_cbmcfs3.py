#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #
import base64, hashlib, warnings

# Third party modules #
import numpy, pandas
from scipy.optimize import curve_fit
from tqdm import tqdm

# First party modules #
from plumbing.cache import property_cached

# Internal modules #
from silvette import conversion
from silvette.conversion.yields_graphs import YieldFitCheck

# Continents #
from cbmcfs3_runner.core.continent import continent as cbm_continent
from silvette.core.continent import continent as silv_continent

###############################################################################
class Yields(object):
    """
    This class will enable us to convert the yield files provided by R.P. from
    their CBM-CFS3 format to a simple triplet of coefficients.
    These coefficients are then stored in a file that will serve as input to
    the silvette model under the name "growth_curves".
    """

    def __init__(self, cbm_country):
        # Main attributes #
        self.cbm_country = cbm_country

    @property_cached
    def silv_country(self):
        """The matching silvette country object."""
        return silv_continent[self.cbm_country.iso2_code]

    #--------------------------- Classifiers ---------------------------------#
    @property_cached
    def cbm_classif_names(self):
        """The list of classifier names for this country.
        Before being renamed to fit our standards."""
        return self.cbm_country.classifiers.names

    @property_cached
    def classif_mapping(self):
        """The mapping between CBM-CFS3 classifiers names and our
        improved silvette classifier names."""
        mapping = conversion.cbm_to_silv_classifiers
        return {k: v for k,v in mapping.items() if k in self.cbm_classif_names}

    @property_cached
    def silv_classif_names(self):
        """The list of classifier names for this country.
        After being renamed to fit our standards."""
        return list(self.classif_mapping.values())

    #--------------------------- Data Frames ---------------------------------#
    @property_cached
    def df_filtered(self):
        """
        The values we get from R.P. filtered to have only growth curves that
        are actually used in the inventory

        Columns are: ['status', 'forest_type', 'region', 'management_type',
                      'management_strategy', 'climatic_unit',
                      'conifers_bradleaves', 'sp', 'Vol0',
                      'Vol1', 'Vol2', 'Vol3', 'Vol4', 'Vol5', 'Vol6', 'Vol7', 'Vol8', 'Vol9',
                      'Vol10', 'Vol11', 'Vol12', 'Vol13', 'Vol14', 'Vol15', 'Vol16', 'Vol17',
                      'Vol18', 'Vol19', 'Vol20', 'Vol21', 'Vol22', 'Vol23', 'Vol24', 'Vol25',
                      'Vol26', 'Vol27', 'Vol28', 'Vol29', 'Vol30']
        """
        # Load the CSV from yields.csv #
        df = self.cbm_country.orig_data.yields
        # Load inventory #
        inventory = self.cbm_country.orig_data.inventory
        # Keep only classifiers columns #
        inv_clsfrs = inventory[self.cbm_classif_names]
        # Make them unique #
        inv_clsfrs = inv_clsfrs.drop_duplicates()
        # Index #
        df         = df.set_index(self.cbm_classif_names)
        inv_clsfrs = inv_clsfrs.set_index(self.cbm_classif_names)
        # Filter #
        df = df[df.index.isin(inv_clsfrs.index)]
        # Reset index #
        df = df.reset_index()
        # Return #
        return df

    @property_cached
    def df_renamed(self):
        """
        Columns are: ['protected', 'species', 'region', 'mgmt_type',
                      'age_struct', 'climate', ..., 'Vol0',
                      'Vol1', 'Vol2', 'Vol3', 'Vol4', 'Vol5', 'Vol6', 'Vol7', 'Vol8', 'Vol9',
                      'Vol10', 'Vol11', 'Vol12', 'Vol13', 'Vol14', 'Vol15', 'Vol16', 'Vol17',
                      'Vol18', 'Vol19', 'Vol20', 'Vol21', 'Vol22', 'Vol23', 'Vol24', 'Vol25',
                      'Vol26', 'Vol27', 'Vol28', 'Vol29', 'Vol30']
        """
        # Make a reference #
        df = self.df_filtered
        # This column is redundant with 'forest_type' #
        df = df.drop(columns=['sp'])
        # This column is also redundant with 'forest_type' #
        df = df.drop(columns=['conifers_broadleaves'])
        # Change some columns names to match our classifiers names #
        df = df.rename(columns=self.classif_mapping)
        # Change some row contents to real names #
        df['mgmt_type']  = df['mgmt_type'].map(conversion.cbm_to_silv_mgmt_type)
        df['age_struct'] = df['age_struct'].map(conversion.cbm_to_silv_age_struct)
        # Return #
        return df

    @property_cached
    def df_reshaped(self):
        """Reshape the data frame to have an extra column
        <age> and single data column <volume>.
        Also assume a linear distribution within a single age class
        and place the center of mass at the middle. Hence:
            * vol1 becomes 5 years.
            * vol2 becomes 15 years.
             ...
            * vol30 becomes 295 years.

        It will look something like this:

           protected species region  climate    mgmt_type mgmt_strat  age   volume
        0        For      QR   LU00       35  high_forest          E    5    39.10
        1        For      QR   LU00       35  high_forest          E   15    84.26
        2        For      QR   LU00       35  high_forest          E   25   132.07
        3        For      QR   LU00       35  high_forest          E   35   180.93
        """
        # Make a reference #
        df = self.df_renamed
        # Remove age zero so it doesn't end at -5 #
        df = df.drop(columns=['vol0'])
        # Melt #
        df = df.melt(id_vars    = self.silv_classif_names,
                     var_name   = "age",
                     value_name = "volume")
        # Remove suffixes and keep just the number #
        df['age'] = df['age'].str.lstrip("vol").astype('int')
        # Actually the age classes are bins of ten years #
        df['age'] = (df['age'] * 10) # - 5
        # Return #
        return df

    @property_cached
    def df_coefs(self):
        """Only the coefficients we will save for use in silvette."""
        columns   = self.silv_classif_names + ['a_opt', 'b_opt', 'c_opt']
        generator = (curve.row for curve in self.growth_curves)
        df        = pandas.DataFrame(generator, columns=columns)
        return df

    #----------------------------- Objects -----------------------------------#
    @property_cached
    def growth_curves(self):
        """
        From the data frame reshaped, create individual growth curve objects.
        For every group of distinct classifiers we will have one growth curve.
        """
        # Group by classifiers #
        groups = self.df_reshaped.groupby(self.silv_classif_names)
        # One object for each group #
        return [GrowthCurveWithPoints(self, grp[0], grp[1]) for grp in groups]

    #------------------------------ Methods ----------------------------------#
    def __call__(self):
        #self.save_dataframe()
        self.make_graphs()

    def save_dataframe(self):
        """Save the data frame to disk in silvette_data."""
        # The file location #
        source      = self.df_coefs
        destination = str(self.silv_country.orig_data.paths.growth_csv)
        # Save #
        source.to_csv(destination)

    def make_graphs(self):
        """Save the graphs to disk in silvette_data."""
        self.growth_curves[0].base_dir.remove()
        for curve in self.growth_curves: curve.graph.plot()

###############################################################################
class GrowthCurveWithPoints(object):
    """
    Create a GrowthCurve when starting with an actual set of data points
    in a 2D coordinate system describing volume per hectare.
    This class will interpolate the data points to fit a function.
    """

    def __repr__(self): return '<%s object "%s">' % (self.__class__.__name__,
                                                     self.long_name)

    def __init__(self, parent, classif_values, df):
        """
        *classif_values* is a tuple like:
            ('For', 'AA', 'BG00', 25, 'high_forest', 'E', 4)

        *df* has columns:
            protected, species, [...], age, volume

        and age goes from 5 to 295 usually.
        In each *df* all classifiers are homogeneous.
        """
        # Save attributes #
        self.parent = parent
        self.classif_values = classif_values
        self.df = df
        # Where the graphs are saved #
        self.base_dir = self.parent.silv_country.paths.conversion_growth_dir

    @property_cached
    def long_name(self): return '-'.join(map(str, self.classif_values))

    @property_cached
    def short_name(self):
        """
        Turn the set of classifiers into a unique short string by hashing.
        Here "For-AA-BG00-25-high_forest-E-4" becomes "7IheoCHxR".
        """
        short_name = hashlib.md5(self.long_name.encode()).digest()[:6]
        short_name = base64.urlsafe_b64encode(short_name).decode()
        short_name = short_name.replace('=','')
        return short_name

    @property_cached
    def x(self):
        x = list(self.df['age'])
        x.insert(0, 0.0)
        return x

    @property_cached
    def y(self):
        y = list(self.df['volume'])
        y.insert(0, 0.0)
        return y

    @property_cached
    def params(self):
        """
        Calculate the optimal parameters a, b and c to fit a curve to
        the points. Use like this: print(self.params.a_opt)
        """
        # Interpolate #
        try:
            params_opt, param_errors = self.interpolate()
        except RuntimeError:
            params_opt   = (numpy.nan, numpy.nan, numpy.nan)
            param_errors = (0, 0, 0)
            message      = "The '%s' curve at '%s' failed to be fitted."
            warnings.warn(message % (self.long_name, self.short_name))
        # All the six params #
        params = {'a_opt': params_opt[0],
                  'b_opt': params_opt[1],
                  'c_opt': params_opt[2],
                  'a_err': param_errors[0],
                  'b_err': param_errors[1],
                  'c_err': param_errors[2]}
        # Return a dummy object with attributes #
        return type('Params', (object,), params)

    def interpolate(self):
        """
        We are going to interpolate using the The Chapman-Richards growth function.
        See https://blogg.slu.se/forest-biometrics/2017/03/11/the-chapman-richards-growth-function/
        """
        # The function #
        def bertalanffy(t, a, b, c):
            return a * (1 - numpy.exp(-b*t))**3 + c
        def chapman_richards(t, a, b, c):
            return a * (1 - numpy.exp(-b*t))**c
        def korf(t, a, b, c):
            return a * numpy.exp(-b*t**(-c))
        # Starting point for parameter exploration #
        p_start = (300, 6, 0.5)
        # Fit with method Levenberg-Marquardt (lm) #
        params_opt, params_cov = curve_fit(korf, self.x, self.y, p_start,
                                           maxfev = 1200, method='lm')
        # Save one standard deviation errors on the parameters #
        param_errors = numpy.sqrt(numpy.diag(params_cov))
        # Return #
        return params_opt, param_errors

    @property_cached
    def row(self):
        """For building a data frame with all curves inside."""
        coefs = (self.params.a_opt, self.params.b_opt, self.params.c_opt)
        return self.classif_values + coefs

    @property_cached
    def graph(self):
        """For checking goodness of fit."""
        return YieldFitCheck(self, self.base_dir)

###############################################################################
if __name__ == '__main__':
    # Make yield objects #
    yields_objs = [Yields(c) for c in cbm_continent]
    # Run them #
    for cur_yields in tqdm(yields_objs):
        if cur_yields.cbm_country.iso2_code != 'IT': continue
        cur_yields()



