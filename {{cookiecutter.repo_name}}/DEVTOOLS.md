# Dev tools

# Overview

* [vprof](https://github.com/nvdv/vprof) - Profiling. It offers flame graphs, memory graphs and code heatmaps of python scripts.
* [MonkeyType](https://github.com/Instagram/MonkeyType) - Automatic typing. It automatically generates type annotations for your python scripts.

## TLDR

Minimal and typical usage of these packages.

### vprof

```bash
# Install python package
pip install vprof

# Prepare for all graphs
vprof -c cmhp /path/to/script.py --output-file profile.json

# Prepare for flame graph
vprof -c c /path/to/script.py --output-file profile.json

# Visualize
vprof --input-file profile.json
```

### monkeytype

```bash
# Install from PyPI
pip install MonkeyType

# Infer the type annotation
monkeytype run myscript.py

# Outputs a output a stub file
monkeytype stub some.module

# Modifies some/module.py
monkeytype apply some.module
```

