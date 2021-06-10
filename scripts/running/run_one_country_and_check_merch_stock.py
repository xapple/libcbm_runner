# libcbm version 

from libcbm_runner.core.continent import continent as continent_libcbm
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

