# GIS Python Bench

## Overview

This repository contains a series of GIS python processing scripts that act as a benchmark for common spatial processing. Some of these are single CPU bound. Some use multiple cores and some use a bunch of memory. 

These benchmarks are based on real work applications and so are not comprehensive. They are skewed to the types of analysis that I do. The benchmark scripts are also not optimised for performance, many of which are largely generated with the assistance of LLMs. The performance therefore represents typical performance of scripts in production. Where there was performance issues with the processing I would normally perform some basic optimisation, up to the point where is added significant complexity to the solution.


## Repository Structure

### Scripts Overview

- **`01-download-input-data.py`**
    Downloads supporting datasets that are not included in this repository.

- **`02-combine-habitat-layers.py`**
    This script largely tests manipulating shapefiles, in particular clipping and dissolving to combine multiple layers into a single shapefile with no overlap between the layers. This benchmark came from the habitat mapping prepared for the Keppel Islands coral project. This task is single threaded and CPU intensive. The input data is small, only a few MB, but the processing tasks minutes. 
    
    
## Benchmark results
This section stores the results of benchmark runs on different machines.

| Machine                                                 | Script                       | Time (min) |
|---------------------------------------------------------|------------------------------|------------|
| Dell 5520 11th Gen Intel(R) Core(TM) i7-1185G7 @ 3.00GHz| 02-combine-habitat-layers.py | 12.50      |
| Dell 5520 11th Gen Intel(R) Core(TM) i7-1185G7 @ 3.00GHz| 02-combine-habitat-layers.py | 1.26       |
| Dell 5520 11th Gen Intel(R) Core(TM) i7-1185G7 @ 3.00GHz| 02-combine-habitat-layers.py | 0.86       |
| Mac Pro 16in M4 Max                                     | 02-combine-habitat-layers.py | 0.24       |
|                                                         |                              |            |

    
## Setup Instructions

1. Download the Miniconda installer for Windows from [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html).

2. Run the installer and follow the prompts. Make sure to:
   - Select "Add Miniconda to my PATH environment variable" (optional but convenient).
   - Allow the installer to initialize Miniconda.

3. Open a new Command Prompt (cmd) window.

4. Install required Python packages using the following command:
```bash
conda env create -f environment.yml
```
5. Activate the environment
```bash
conda activate gis-bench
```

## Running the benchmarks

1. Run the download script. This downloads the datasets that are manipulated by the benchmark scripts.
