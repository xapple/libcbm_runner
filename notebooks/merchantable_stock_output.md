---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.3.3
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

# Run

```python
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

```

# Input data


## Classifiers

```python
# Classifiers as defined in the input data
runner_libcbm.input_data['classifiers']
```

```python
# Classifiers as used by libcbm
with pandas.option_context('display.max_rows', None, 'display.max_columns', None):
    display(runner_libcbm.simulation.classifiers)
```

## Inventory


```python
inv = runner_libcbm.input_data['inventory']
inv
```

```python
inv.sum
```

# Output

## Merchantable pools

```python
import pandas
with pandas.option_context('display.max_rows', None, 'display.max_columns', None):
    display(pools_libcbm.query('timestep == 0'))
```

```python
pools0 = pools_libcbm.query('timestep == 0')
# Compare the input inventory area to the area available in the output pools table
print(pools0['Input'].sum())
print(inv['area'].sum())
# They are exactly the same

#merch_libcbm_by_year = (pools_libcbm
#  .agg({'area': 'sum', 
#        'HardwoodMerch': 'sum',
#        'SoftwoodMerch': 'sum'}))
#
#
```

```python

```
