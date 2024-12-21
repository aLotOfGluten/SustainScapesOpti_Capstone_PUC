# Source Code Directory (`src`)

This directory contains the core source code for the SustainScapesOpti project. The primary purpose of these scripts is to perform optimization for land-use planning using a combination of Gurobi optimization and local search techniques.

It utilizes the parameters and conditions set up in ../config/config_join_local_search.py and ../config/config_solve_problem.py. In order for the scripts to work correctly, the .dat must be constructing using the corresponding parameters and format. This can be done through the use of the TroublemakerR **R** library, documentation at https://cran.r-project.org/web/packages/TroublemakeR/TroublemakeR.pdf.

---

## Files Overview


### `solve_problem.py`
- **Description**: Provides the optimal solution to the optimization problem to one .dat file utilizing the Gurobipy solver.
- **Dependencies**:
  - `gurobipy`
  - Custom configurations from `config/config_solve_problem.py`

### `Join_and_local_search.py`
- **Description**: Merges several solved areas into one and implements a local search algorithm integrated with Gurobi to iteratively optimize land-use allocation while satisfying various constraints such as budget, spatial contiguity, and minimum allocations for specific land-use types.
    - Outputs the final solution and relevant performance metrics into the ../results directory.

- **Dependencies**:
  - `gurobipy`
  - Custom configurations from `config/config_join_local_search.py`
  - Utility functions from `utils.py`

### `utils.py`
- **Description**: Contains helper functions to support the optimization process. Contains:
  - `find_cluster`: Finds a connected set of municipalities (a cluster) based on size and neighbors.
