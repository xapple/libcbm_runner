#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #
import copy

# Third party modules #
import pandas

# First party modules #
from plumbing.cache import property_cached
from libcbm.input.sit import sit_cbm_factory
from libcbm.model.cbm import cbm_variables

# Internal modules #
from libcbm_runner.cbm.simulation import Simulation
from libcbm_runner.core.runner import Runner

# Constants #

###############################################################################

class DynamicRunner(Runner):
    """
    Replaces the standard Simulation object with a DynamicSimulation instead.
    """

    @property_cached
    def simulation(self):
        """The object that can run `libcbm` simulations."""
        return DynamicSimulation(self)

###############################################################################
class DynamicSimulation(Simulation):
    """
    This class inherits from the standard Simulation object, and adds
    new functionality. It enables the running of dynamic simulations which
    can specify their disturbances just-in-time as the model is running.
    This is in contrast to standard simulations which must have all
    disturbances predefined before the model run.
    """

    # These are the dataframe (as attributes) returned by `cbm.step()` #
    df_names = ['classifiers', 'parameters', 'inventory',
                'state', 'flux', 'pools']

    # These are the source pools we want to track fluxes from #
    sources = ['softwood_merch',       'hardwood_merch',
               'softwood_other',       'hardwood_other',
               'softwood_stem_snag',   'hardwood_stem_snag',
               'softwood_branch_snag', 'hardwood_branch_snag']

    #--------------------------- Special Methods -----------------------------#
    def dynamics_func(self, timestep, cbm_vars, debug=True):
        """
        First apply predetermined disturbances, then apply demand
        specific to harvesting. The full specification for the "Harvest
        Allocation Tool" (H.A.T.) is described in:

             ../specifications/libcbm_hat_spec.md

        Information used during development included:

        * The example notebook of the `libcbm` package.

            https://github.com/cat-cfs/libcbm_py/blob/master/examples/
            disturbance_iterations.ipynb
        """
        # Check if we want to switch the growth period classifier #
        if timestep == 1: cbm_vars = self.switch_period(cbm_vars)

        # Retrieve the current year #
        year = self.country.timestep_to_year(timestep)

        # Optional debug messages #
        if debug: print(timestep, year, self.country.base_year)

        # Run the usual rule based processor #
        cbm_vars = self.rule_based_proc.pre_dynamics_func(timestep, cbm_vars)

        # Check if we are still in the historical period #
        if year < self.country.base_year: return cbm_vars

        # Copy cbm_vars and hypothetically end the timestep here #
        end_vars = copy.deepcopy(cbm_vars)
        end_vars = cbm_variables.prepare(end_vars)
        end_vars = self.cbm.step(end_vars)

        # Check we always have the same sized dataframes #
        get_num_rows = lambda name: len(getattr(end_vars, name))
        assert len({get_num_rows(name) for name in self.df_names}) == 1

        # Concatenate dataframes together by columns into one big df #
        df = pandas.concat([getattr(end_vars, name)
                            for name in self.df_names], axis=1)

        # Check that the 'Input' column is always one and remove #
        assert all(df['Input'] == 1.0)
        df = df.drop(columns='Input')

        # Fluxes and pools are scaled to one hectare so fix it #
        cols = list(end_vars.flux.columns) + list(end_vars.pools.columns)
        cols.pop(cols.index('Input'))
        df[cols] = df[cols].multiply(df['area'], axis="index")

        # Load the fraction that goes to `irw` and to `fw` #
        irw_frac = self.runner.silv.irw_frac.get_year(year)
        cols = self.runner.silv.irw_frac.cols

        # Get only eight interesting fluxes, summed by disturbance type #
        fluxes = df.query("disturbance_type != 0")
        fluxes = fluxes.groupby(cols)
        fluxes = fluxes.agg({s + '_to_product': 'sum' for s in self.sources})
        fluxes = fluxes.reset_index()

        # Join the fluxes going to `products` with the IRW fractions #
        fluxes = fluxes.merge(irw_frac, how='left', on=cols)

        # Join the wood density and bark fraction parameters #
        pass #TODO

        # Calculate the `flux_irw` and `flux_fw` for this year #
        flux_irw = sum([fluxes[s + '_to_product'] * fluxes[s]
                        for s in self.sources])
        flux_fw  = sum([fluxes[s + '_to_product'] * (1 - fluxes[s])
                        for s in self.sources])

        # Get demand for the current year #
        query  = "year == %s" % year
        fw  = self.runner.demand.irw.query(query)['value']
        irw = self.runner.demand.fw.query(query)['value']

        # Convert to a cubic meter float value #
        self.demand_fw_vol  = fw.values[0]  * 1000
        self.demand_irw_vol = irw.values[0] * 1000



        # Debug test #
        if timestep == 19:
            end_vars = copy.deepcopy(cbm_vars)
            end_vars = cbm_variables.prepare(end_vars)
            end_vars = self.cbm.step(end_vars)
            print(end_vars)
            1/0

        # Compute remaining demand that needs to be satisfied #

        # Return #
        return cbm_vars

    #---------------------------- Exploration --------------------------------#
    def test(self, timestep, cbm_vars):
        # Check the timestep #
        if timestep == 12:
            print('test')

        # Info sources ? #
        # prod has columns:
        # Index(['DisturbanceSoftProduction', 'DisturbanceHardProduction',
        #        'DisturbanceDOMProduction', 'Total'])
        # Aggregate of fluxes,
        prod = self.cbm.compute_disturbance_production(cbm_vars, density=False)
        print(prod)

        # Sit events has columns:
        # Index(['total_eligible_value', 'total_achieved', 'shortfall',
        #        'num_records_disturbed', 'num_splits', 'num_eligible',
        #        'sit_event_index'],
        #        dtype = 'object')#
        print(self.rule_based_proc.sit_event_stats_by_timestep)

        # This is just the same as the input events.csv #
        print(self.sit.sit_data.disturbance_events)

        # This doesn't contain the current timestep, only past ones
        print(self.results.state)

        # Return #
        return cbm_vars

###############################################################################
class ExampleHarvestProcessor:
    """
    This class can dynamically generate disturbance events using an
    event template to meet the specified production target.

    This class was copied and adapted from the following notebook:

        https://github.com/cat-cfs/libcbm_py/blob/master/examples/
        disturbance_iterations.ipynb
    """

    def __init__(self, sit, cbm, production_target):
        # Base attributes #
        self.sit = sit
        self.cbm = cbm
        # User attributes #
        self.production_target = production_target
        # List to accumulate information #
        self.dynamic_stats_list     = []
        self.base_production_totals = []
        # Function shortcuts #
        self.calc_prod = self.cbm.compute_disturbance_production
        self.create_proc = sit_cbm_factory.create_sit_rule_based_processor
        # Extras #
        self.base_processor = self.create_proc(self.sit, self.cbm)

    sit_events_path = "~/repos/sinclair/work/freelance_clients/ispra_italy/" \
                      "repos/libcbm_py/libcbm/resources/test/cbm3_tutorial2" \
                      "/disturbance_events.csv"

    def get_event_template(self):
        """Return a prototypical disturbance event ready to be customized."""
        # Make dataframe #
        df = pandas.read_csv(self.sit_events_path).iloc[[0]]
        # Reset #
        df = df.reset_index(drop=True)
        # Return #
        return df

    def pre_dynamics_func(self, timestep, cbm_vars):
        """
        Use a production target (tonnes C) to apply across all years.
        This will be partially met by the base tutorial2 events,
        then fully met by a second dynamically generated event.
        """
        # Get CBM variables #
        cbm_vars = self.base_processor.pre_dynamics_func(timestep, cbm_vars)

        # Compute the total production resulting from the sit_events
        # bundled in the tutorial2 dataset.
        production_df = self.calc_prod(cbm_vars, density=False)
        total_production = production_df["Total"].sum()

        # Append #
        self.base_production_totals.append([timestep, total_production])

        # Subtract #
        remaining_production = self.production_target - total_production

        # If the target is already met we stop here #
        if remaining_production <= 0: return cbm_vars

        # Otherwise we create a dynamic event #
        dynamic_event = self.get_event_template()
        dynamic_event["disturbance_year"] = timestep
        dynamic_event["target_type"]      = "M"
        dynamic_event["target"]           = remaining_production

        # See the documentation:
        # `libcbm.input.sit.sit_cbm_factory.create_sit_rule_based_processor`
        dynamic_processor = self.create_proc(
            self.sit,
            self.cbm,
            reset_parameters = False,
            sit_events = dynamic_event
        )

        # Apply the disturbance #
        cbm_vars = dynamic_processor.pre_dynamics_func(timestep, cbm_vars)

        # Merge #
        df = dynamic_processor.sit_event_stats_by_timestep[timestep]
        df = df.merge(
            dynamic_event,
            left_on     = "sit_event_index",
            right_index = True
        )

        # Append #
        self.dynamic_stats_list.append(df)

        # Return CBM variables #
        return cbm_vars

    #----------------------------- Reporting ---------------------------------#
    def get_base_process_stats(self):
        """
        Gets the stats for all disturbances in:
        `sit.sit_data.disturbance_events`.
        """
        # Get stats #
        stats_df = pandas.concat(
            self.base_processor.sit_event_stats_by_timestep.values()
        )
        # Merge #
        df = stats_df.merge(
            self.sit.sit_data.disturbance_events,
            left_on     = "sit_event_index",
            right_index = True
        )
        # Return #
        return df

    def base_prod_totals_to_df(self):
        # Make dataframe #
        df = pandas.DataFrame(
            columns = ["timestep", "total_production"],
            data    = self.base_production_totals
        )
        # Return #
        return df

    def dynamic_proc_stats_to_df(self):
        # Make dataframe #
        df = pandas.concat(self.dynamic_stats_list).reset_index(drop=True)
        # Return #
        return df