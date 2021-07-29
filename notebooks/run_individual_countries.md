---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.11.3
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

```python
from libcbm_runner.core.continent import continent
```




# Introduction

The purpose of this notebook is to illustrate how the model is run for various scenarios and for individual coutnries. Each country section gives the possibility to provide country specifics details. Additional methods are provided to explore the output. 

Each runner has an associated log file where information about the run is storred. It it located at `libcbm_data/scenarios/scenario_name/country_iso2_code/0/logs/runner.log`.



# AT


## Run example scenario afforestation

Run an afforestation scenario which is quite short. 

```python
# Create a libcbm runner object
scenario = continent.scenarios['afforestation']
r_at = scenario.runners['AT'][-1]
r_at.run(keep_in_ram=True)
```

## Explore results that were stored to disk


### Pools

```python
r_at.output['pools'].sum()
```

## Explore volatile results

libcbm results are volatile and are deleted after each simulation. Simulation results **only remain available in RAM** if the run() method was called with the `keep_in_ram=True` argument.

```python
def list_normal_methods(obj):
    """Filter out special methods from the output of dir()
    copied from https://stackoverflow.com/a/21542780/2641825"""
    return [x for x in dir(obj) if not x.startswith('__')]
list_normal_methods(r_at.simulation.results)
```

### Area

```python
r_at.simulation.results.area.iloc[[1,-1]]
```

### Classifiers

```python
r_at.simulation.results.classifiers.iloc[[1,-1]]
```

### Flux

```python
flux_at = r_at.simulation.results.flux
flux_at.iloc[[1,-1]]
```

```python
flux_at.columns
```

### Params

```python
r_at.simulation.results.params.iloc[[1,-1]]
```

### Pools

```python
r_at.simulation.results.pools.iloc[[1,-1]]
```

### State

```python
r_at.simulation.results.state.iloc[[1,-1]]
```

# LU


## Run the historical scenario

```python
scenario = continent.scenarios['historical']
r_lu = scenario.runners['LU'][-1]
#r_lu.run()
```

## Explore results

```python
r_lu.output['pools']
```

```python
r_lu.output['pools'].SoftwoodMerch.plot(figsize=(30,10))
```

```python

```
