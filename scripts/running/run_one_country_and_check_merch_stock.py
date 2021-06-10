
################################################################################
##################### JRC's version using libcbm_runner ########################
################################################################################

# Import
from libcbm_runner.core.continent import continent

# Init
scenario = continent.scenarios['historical']
runner_libcbm = scenario.runners['LU'][-1]
runner_libcbm.run()

# Show results
#print(runner_libcbm.simulation.results)
#print(runner_libcbm.simulation.inventory)

# Retrieve pools
pools_libcbm = runner_libcbm.simulation.results.pools

# Make dataframe
merch_libcbm_by_year = (pools_libcbm
  .groupby('timestep')
  .agg({'HardwoodMerch': 'sum',
        'SoftwoodMerch': 'sum'})
  .reset_index())

# Show
print(merch_libcbm_by_year)

###############################################################################
################ Canada's version using only libcbm_py ########################
###############################################################################

# Imports
from libcbm.input.sit import sit_cbm_factory
from libcbm.model.cbm import cbm_simulator
import os

# Constant
json_config_path = "xxxxxxxxxxxxxxxx"

# Function
def run_libcbm():
    libcbm_config_path = os.path.abspath(json_config_path)
    sit = sit_cbm_factory.load_sit(libcbm_config_path)
    classifiers, inventory = sit_cbm_factory.initialize_inventory(sit)
    cbm = sit_cbm_factory.initialize_cbm(sit)
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

# Run libcbm
libcbm_results = run_libcbm()

# Make dataframe
libcbm_merch_by_timestep = libcbm_results.pools[
    ["timestep", "SoftwoodMerch", "HardwoodMerch"]
].groupby("timestep").sum().rename(
    columns={
        "timestep": "TimeStep",
        "SoftwoodMerch": "swm_libcbm",
        "HardwoodMerch": "hwm_libcbm"
    })

# Show
print(libcbm_merch_by_timestep)


