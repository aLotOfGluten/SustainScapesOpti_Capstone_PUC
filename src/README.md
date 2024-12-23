# Source Code Directory (`src`)

This directory contains the core source code for the SustainScapesOpti project. The primary purpose of these scripts is to perform optimization for land-use planning using a combination of Gurobi optimization and local search techniques.

It utilizes the parameters and conditions set up in `../config`.

---

## Files Overview

### `solve_problem.py`
- **Description**: Provides the optimal solution to the optimization problem to one .dat file utilizing the Gurobipy solver.
- **Dependencies**:
  - Variables and paths set in `config/config_solve_problem.py`

### `solve_parallelized.py`
- **Description**: Provides the optimal solution to the optimization problem to various .dat file in parallel utilizing the Gurobipy solver.
- **Dependencies**:
  - Variables and paths set in `config/config_run_all.py`

### `join_and_local_search.py`
- **Description**: Imports an initial solution (which can be one saved in one or more files) and implements a local search algorithm integrated with Gurobi to iteratively optimize land-use allocation while satisfying various constraints such as budget, spatial contiguity, and minimum allocations for specific land-use types.
    - Outputs the final solution and relevant performance metrics into the `../results/` directory.

- **Dependencies**:
  - Custom configurations from `config/config_run_all.py`
  - Utility functions from `utils.py`

### `utils.py`
- **Description**: Contains helper functions to support the optimization process. Contains:
  - `find_cluster`: Finds a connected set of municipalities (a cluster) based on size and neighbors.
