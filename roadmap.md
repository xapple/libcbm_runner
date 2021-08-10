# Bring libcbm_runner to feature parity with cbmcfs3_runner

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

- Check between libcbm_runner and cbmcfs3_data scenario of the static demand the
  consistency of pools for merchantable, Living Biomass, Soil Organic Carbon

- notebooks available
  (C:/CBM/cbmcfs3_runner/notebooks/comparison_libcbm/soil_comparison.md)
  (C:/CBM/cbmcfs3_runner/notebooks/comparison_libcbm/current_historical_libcbm.md
  For each of the relevant pools using
  numpy.testing.assert_allclose(processed, raw, rtol=1e-02)

- Creating a mechanism to define and run scenarios

- Use lower case names for classifier columns

     'Status' =  status
     'Forest type' =  forest_type
     'Region' =  region
     'Management type' = mgmt_type
     'Management strategy' = mgmt_strategy
     'Climatic unit' = climate
     'Conifers/Broadleaves' = con_broad
     'Site index' = site_index
     'Simulation period (for yields)'] = growth_period


# Dynamic harvest allocation Task

- Add a mechanism for the dynamic harvest allocation


# Future code improvements

- Better error message in the case where the AIDB is absent (or an empty symbolic link).
  Current message is table species missing.

- Fix version of autopaths and plumbing dependencies

- Since the simulation can take a long time it is useful to know when libcbm starts
  loading the data and when each simulation step starts with a short message. To
  increase the verbosity, the runner could display messages when the model is running by
  for example replacing the print statements with a mechanism that enables logging.
  Example of print statements providing information on the status of the run available
  on this old commit
  [ab62642d6bcb](https://gitlab.com/bioeconomy/libcbm/libcbm_runner/-/commit/ab62642d6bcb13e88f79973814f9a4735f7a2cbf).

- Would it make sense to make sit available before the simulation run?  i.e. Create a
  SIT object before the run method? Maybe it doesn't make sense. An alternative would be
  to decompose the run in 2 one that prepares the run and one that actually calls the
  simulator? That's mostly useful for debugging anyway.

        self.sit = sit_cbm_factory.load_sit(str(self.paths.json_config), db_path=str(db_path))

## AIDB

There are many AIDB because disturbances have different meaning in different countries
and because soil decomposition parameters are different.

- Differences in disturbance definition could be harmonized with a naming scheme and a
  single AIDB for all EU.
- But the soil decomposition parameters are not part of the input data. So if we really
  want only one AIDB, there needs to be a mechanism to changes those soil decomposition
  parameters for all countries.




