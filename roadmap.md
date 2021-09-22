# Bring libcbm_runner to feature parity with cbmcfs3_runner

- Show comparison of output pool from cbmcfs3 and libcbm. To illustrate the similarities.

- Check between libcbm_runner and cbmcfs3_data scenario of the static demand the remaining inconsistency of pools specifically for the DOM and soil pools

For some reason the AIDB of cbmcfs3 (latest AIDB from online) contains different values for the following turnovers:

                                       cbmcfs3	libcbm
    SoftwoodBranchTurnOverRate	0.0400000000000	0.0115000000224
    HardwoodBranchTurnOverRate	0.0400000000000	0.0115000000224

Moreover, for some reason libcbm only shows an unique value of “stem & branch to snag” for both softwoods and hardwoods.

                                   cbmcfs3	libcbm
    SoftwoodStemSnagToDOM	0.032000000000	0.032000002
    HardwoodStemSnagToDOM	0.032000000000	equal to above
    SoftwoodBranchSnagToDOM	0.100000000000	0.100000001
    HardwoodBranchSnagToDOM	0.100000000000	equal to above


# Current code improvements

## Scenarios

- Mechanism to combine various elementary scenarios into a scenario

- Comparison of scenario outputs


## Dynamic harvest allocation Task

HAT (Harvest Allocation Task)

- Add a mechanism for the dynamic harvest allocation


# Quality assurance and quality control (QA/QC)

## Pre-processing

- Method to compare input data across scenarios


## Post processing

- Harvest requested and harvested allocated


## AIDB

Scenarios changing parameters in the AIDB

- Changing soil decomposition parameters before the model run for the purpose of a given scenario.


## Harmonization of AIDB (long term)

There are many AIDB because disturbances have different meaning in different countries and because soil decomposition parameters are different.

- Differences in disturbance definition could be harmonized with a naming scheme and a single AIDB for all EU.

- But the soil decomposition parameters are not part of the input data. So if we really want only one AIDB, there needs to be a mechanism to changes those soil decomposition parameters for all countries.

























# Done

## AIDB

- Better error message in the case where the AIDB is absent (or an empty symbolic link).
  Current message is table species missing.

## Bring libcbm_runner to feature parity with cbmcfs3_runner

- Bring libcbm_runner to feature parity with cbmcfs3_runner in terms of running CBM on
  the harmonized input data for the 26 EU countries.

- As of June 2021 the model output is volatile in memory. Add a mechanism to write the
  model output to disk for different scenarios.

- Transfer the static_demand disturbances to the orig/csv/events.csv
  from
  /home/paul/rp/cbmcfs3_data/scenarios/static_demand/LU/0/input/csv/disturbance_events.csv
  to /libcbm_data/countries/LU/orig/csv/

* Add an 8th classifier for site index classifiers to all countries like is already the
  case in Bulgaria.

  8	_CLASSIFIER	Site index
  8	1 default

- Adding the 9th classifier called `growth_period` to the following input files. As has
  currently been done manually for Luxembourg. It should take values ̀`init` for the
  initialization period and `current` for the current period.

    classifiers.csv
    events.csv
    inventory.csv
    transitions.csv
    growth_curves.csv

- Creating a mechanism to define and run scenarios

- Check between libcbm_runner and cbmcfs3_data scenario of the static demand the
  consistency of pools for merchantable, Living Biomass, Soil Organic Carbon

- notebooks available
  (C:/CBM/cbmcfs3_runner/notebooks/comparison_libcbm/soil_comparison.md)
  (C:/CBM/cbmcfs3_runner/notebooks/comparison_libcbm/current_historical_libcbm.md
  For each of the relevant pools using
  numpy.testing.assert_allclose(processed, raw, rtol=1e-02)

- Since the simulation can take a long time it is useful to know when libcbm starts
  loading the data and when each simulation step starts with a short message. To
  increase the verbosity, the runner could display messages when the model is running by
  for example replacing the print statements with a mechanism that enables logging.
  Example of print statements providing information on the status of the run available
  on this old commit
  [ab62642d6bcb](https://gitlab.com/bioeconomy/libcbm/libcbm_runner/-/commit/ab62642d6bcb13e88f79973814f9a4735f7a2cbf).


## Lower case variable names

## Improve variable names

Mostly done in August 2021

- Use lower case names for classifier columns in orig/csv/classifiers.csv
  as well as in corresponding columns of all input files
  so that the input data has the same column names as the output data for example
  `runner.input_data['events']` should have the same column names as
  `runner.output.classif_df`.

     'Status' =  status
     'Forest type' =  forest_type
     'Region' =  region
     'Management type' = mgmt_type
     'Management strategy' = mgmt_strategy
     'Climatic unit' = climate
     'Conifers/Broadleaves' = con_broad
     'Site index' = site_index
     'Simulation period (for yields)' = growth_period

- All output variables in snake case

- Replace "Input" column to "area" in runner.output.load('area')

- When giving 30 years of disturbances in the input data for the afforestation scenario,
  the simulation runs only for 18 years. This could be due to a clause in the historical
  scenario that limits the length of the simulation to the current year.

AIDB to pandas done in  August 2021

- Make tables in the AIDB accessible to be loaded as pandas data frames.

