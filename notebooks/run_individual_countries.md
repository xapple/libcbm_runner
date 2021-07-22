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

The purpose of this notebook is to illustrate how the model is run for various scenarios and for individual coutnries. Each country section gives the possibility to provide country specifics details.


# Introduction

Each runner has an associated log file where information about the run is storred. It it located at `libcbm_data/scenarios/scenario_name/country_iso2_code/0/logs/runner.log`.



# AT

```python
# Create a libcbm runner object
scenario = continent.scenarios['historical']
r_at = scenario.runners['AT'][-1]
r_at.run()
```

# LU

```python
scenario = continent.scenarios['historical']
r_lu = scenario.runners['LU'][-1]
r_lu.run()
```
