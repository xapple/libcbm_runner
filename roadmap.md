

# Bring libcbm_runner to feature parity with cbmcfs3_runner

- Bring libcbm_runner to feature parity with cbmcfs3_runner in terms of running CBM on 
  the harmonized input data for the 26 EU countries.

- As of June 2021 the model output is volatile in memory. Add a mechanism to write the 
  model output to disk for different scenarios.


# Dynamic harvest allocation Task

- Add a mechanism for the dynamic harvest allocation 


# Code improvements

- Better error message in the case where the AIDB is absent (or an empty symbolic link). 
  Current message is table species missing.

- Fix version of autopath and plumbing dependencies

- Increase verbosity, display more messages when the model is running

