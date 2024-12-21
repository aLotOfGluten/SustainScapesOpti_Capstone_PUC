# Configuration Files Directory (`config`)

This directory contains the configuration files required for running the optimization scripts in the project found in ../scr. Each configuration file specifies the input files, output paths, and algorithm parameters necessary for their corresponding optimization processes.

---

### `config_join_local_search.py`
- **Description**: Configuration file for the Join and Local Search algorithm.
- **Key Configurations**:
  - **Id**: Identifies the test to avoid overwriting output files. 
  - **ratio**: Percentage of cells freed during local search.
  - **max_time**: Maximum runtime for the Local Search algorithm (in seconds).
  - **max_iter**: Maximum number of iterations for Local Search.
  - **join_rest**: If `True`, evaluates the initial solution before starting Local Search.
  - **Input Files**:
    - `problem_path`: Path to the `.dat` file with the problem definition.
    - `pathlist`: List of paths to initial solution files for the join and local search.
    - `cell_ids`: CSV file mapping cell IDs to municipalities.
    - `municip_neighbors`: Text file containing municipality adjacency information.
  - **Output Files**:
    - `results_path`: File to save the optimized cell assignments.
    - `summary_path`: Summary of results for the Local Search process.
    - `gurobi_log_file`: Log file for Gurobi operations.
    - `log_file`: Log file tracking the Local Search iterations.
    - `municip_log_path`: Log file tracking municipalities used in each iteration.

### `config_solve_problem.py`
- **Description**: Configuration file for solving the problem directly without Local Search.
- **Key Configurations**:
  - **name**: Name of test. Identifies the test to avoid overwriting output files.
  - **Input File**:
    - `problem_path`: Path to the `.dat` file with the problem definition.
  - **Output Files**:
    - `results_path`: File to save the optimized cell assignments.
    - `summary_path`: Summary of results for the problem-solving process.
    - `gurobi_log_file`: Log file for Gurobi operations.
