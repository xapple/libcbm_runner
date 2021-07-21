

# Bring libcbm_runner to feature parity with cbmcfs3_runner

- Bring libcbm_runner to feature parity with cbmcfs3_runner in terms of running CBM on 
  the harmonized input data for the 26 EU countries.

- As of June 2021 the model output is volatile in memory. Add a mechanism to write the 
  model output to disk for different scenarios.

- Transfer the static_demand disturbances to the orig/csv/events.csv
  from
  /home/paul/rp/cbmcfs3_data/scenarios/static_demand/LU/0/input/csv/disturbance_events.csv
  to /libcbm_data/countries/LU/orig/csv/

- Adding the 9th classifier called `period` to the following input files. As 
  has currently been done manually for Luxemburg.

    classifiers.csv
    events.csv
    inventory.csv
    transitions.csv
    growth_curves.csv

- Check between libcbm-runner and cbmcfs3_data scenraio of the static demand the
  consistency of pools for merchantable, Living Biomass, Soil Organic Carbon 

- notebooks available 
  (C:/CBM/cbmcfs3_runner/notebooks/comparison_libcbm/Soil_comparison.md)
  (C:/CBM/cbmcfs3_runner/notebooks/comparison_libcbm/current_historical_libcbm.md
  For each of the relevant pools using
  numpy.testing.assert_allclose(processed, raw, rtol=1e-02)

- Creating a mechanism to define and run scenarios


# Dynamic harvest allocation Task

- Add a mechanism for the dynamic harvest allocation 


# Code improvements

- Better error message in the case where the AIDB is absent (or an empty symbolic link). 
  Current message is table species missing.

- Fix version of autopath and plumbing dependencies

- Increase verbosity, display more messages when the model is running. Replace the print 
  statements with a mechanism that enables logging.

- Would it make sense to make sit available before the simulation run?  i.e. Create a 
  SIT object before the run method? Maybe it doesn't make sense. An alternative would be 
  to decompose the run in 2 one that prepares the run and one that actually calls the 
  simulator? That's mostly useful for debugging anyway.

        self.sit = sit_cbm_factory.load_sit(str(self.paths.json_config), db_path=str(db_path))


