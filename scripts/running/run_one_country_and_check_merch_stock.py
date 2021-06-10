
from libcbm_runner.core.continent import continent as continent_libcbm

#####################################
# JRC's version using libcbm_runner #
#####################################

################################################################################
scenario = continent_libcbm.scenarios['historical']
runner_libcbm   = scenario.runners['LU'][-1]
runner_libcbm.run()



#print(runner_libcbm.simulation.results)
#print(runner_libcbm.simulation.inventory)

pools_libcbm = runner_libcbm.simulation.results.pools

merch_libcbm_by_year = (pools_libcbm
  .groupby('timestep')
  .agg({'HardwoodMerch': 'sum',
        'SoftwoodMerch': 'sum'})
  .reset_index())

# pools0_libcbm=pools_libcbm.query('timestep==0')
# for c in pools0_libcbm.columns:
#     print (c, sum(pools0_libcbm[c]))

merch_libcbm_by_year

#########################################
# Canada's version using only libcbm_py #
#########################################

from libcbm.input.sit import sit_cbm_factory
from libcbm.model.cbm import cbm_simulator

def run_libcbm():
    # run the same dataset in libcbm.  the output will be appended
    # timestep-by-timestep to the dataframe results variable in this class
    libcbm_config_path = os.path.abspath(r"./data/libcbm_config.json")
    sit = sit_cbm_factory.load_sit(libcbm_config_path)
    classifiers, inventory = sit_cbm_factory.initialize_inventory(sit)
    cbm = sit_cbm_factory.initialize_cbm(sit)

    # I would encourage you to consider writing your own results
    # processing function/class if you have not already.
    # This one works, but it can cause issues in notebooks if not rebuilt each time
    # (will just keep appending results making it invalid) I suspect this having a
    # role in the doubling you observed in the results you sent.
    results, reporting_func = cbm_simulator.create_in_memory_reporting_func()

    rule_based_processor = sit_cbm_factory.create_sit_rule_based_processor(sit, cbm)
    cbm_simulator.simulate(
        cbm,
        n_steps              = 102,
        classifiers          = classifiers,
        inventory            = inventory,
        pool_codes           = sit.defaults.get_pools(),
        flux_indicator_codes = sit.defaults.get_flux_indicators(),
        pre_dynamics_func    = rule_based_processor.pre_dynamic_func,
        reporting_func       = reporting_func
    )
    return results

# run libcbm
libcbm_results = run_libcbm()

libcbm_merch_by_timestep = libcbm_results.pools[
    ["timestep", "SoftwoodMerch", "HardwoodMerch"]
].groupby("timestep").sum().rename(
    columns={
        "timestep": "TimeStep",
        "SoftwoodMerch": "swm_libcbm",
        "HardwoodMerch": "hwm_libcbm"
    })

