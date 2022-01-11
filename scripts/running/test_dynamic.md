---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.12.0
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

# Imports 

```python
import pandas
from libcbm_runner.core.continent import continent
```

# Get combo

```python
combo   = continent.combos['harvest_test']
runner  = combo.runners['ZZ'][-1]
country = runner.country
```

# Display orig data


## Classifier names

```python
classif_names = list(country.orig_data.classif_names.values())
display(classif_names)
```

## Events (mgmt, orig_data)

```python
events_mgmt = country.orig_data.load(['mgmt', 'events'], to_long=True)
display(events_mgmt)
```

## Inventory  (mgmt, orig_data)

* Measurement Type: “A” for area, “P” for proportion of area of all eligible records, or “M” for merchantable carbon.

* The amount of the stand to be disturbed, according to the measurement type indicated in the “Measurement Type” column (hectares for area, proportion [1 for 100%, 0.5 for 50%, etc.] for proportion of area of all eligible records, and tonnes of carbon for merchantable carbon).

**Sort Type**

* 0* Undefined sort
* 1 No sort; a proportion of each record to disturb is calculated; only applicable to disturbance events with proportion (P) targets
* 2 Sort by merchantable biomass carbon (highest first); only applicable to disturbance events with merchantable carbon (M) targets
* 3 Sort by oldest first
* 4* Sort by time since softwood component was last harvested
* 5 Sort by SVO (State Variable Object) ID; used for spatially explicit projects and instructs the model to disturb 100% of a single eligible record
* 6 Sort randomly; only applicable to fire and insect disturbance events
* 7* Sort by total stem snag carbon (highest first)
* 8* Sort by softwood stem snag carbon (highest first)
* 9* Sort by hardwood stem snag carbon (highest first)
* 10* Sort by softwood merchantable carbon (highest first)
* 11* Sort by hardwood merchantable carbon (highest first)
* 12* Sort by oldest first
* 13* Sort by time since hardwood component was last harvested

`*` Not valid for use in the “Disturbance Events” import file, but can be used after import in the table tblDisturbanceEvents in a project database file.

```python
inv_mgmt = country.orig_data.load(['mgmt', 'inventory'])
display(inv_mgmt)
```

## Number of timesteps

```python
print("Number of timesteps:", events_mgmt['step'].max())
```

**Set the number of time steps**

```python
runner.num_timesteps = 30
```

# Run

```python
output = runner.run(keep_in_ram=True, verbose=True, interrupt_on_error=True)
```

# Display input data


## Disturbances

```python
events = runner.input_data.load('events')

with pandas.option_context('display.max_rows', 5):
    display(events)
```

# Display results


## Classifiers

```python
classif_df = runner.internal.classif_df

with pandas.option_context('display.max_rows', 5): display(classif_df)
```

## Area (internal)

```python
area = runner.internal.load('area')

with pandas.option_context('display.max_rows', 5): display(area)
```

## State (internal)

```python
state = runner.internal.load('state')

with pandas.option_context('display.max_rows', 5): display(state)
```

## Area with age (internal)

```python
# Join the age information #
index = ['identifier', 'year']
age = state[index + ['age', 'time_since_last_disturbance']]
area_age = area.merge(age, 'left', on=index)

with pandas.option_context('display.max_rows', None): display(area_age)
```

# Graph results

```python
area_by_step = area.groupby("year").sum().drop(columns='identifier')
display(area_by_step)
area_by_step[['area']].plot(figsize=(15,10))
```
