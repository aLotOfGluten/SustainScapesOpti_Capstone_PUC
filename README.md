# SustainScapesOpti_Capstone_PUC

Conservation Optimization for Denmark

## 1. Introduction
This repository builds upon an optimization problem from SustainScapes to tackle land-use planning for conservation in Denmark. The project aligns with the European Biodiversity Strategy for 2030, aiming to protect 30% of natural areas and restore 20% of degraded ecosystems by 2030. The repository focuses on developing spatial analysis techniques and optimization algorithms with the aim to improve the running time of the original optimization problem.

## 2. Disclaimer
This repository contains a draft dataset currently under development and is not ready for publication. The dataset is provided strictly for educational and research purposes within the context of the associated course. Users must credit the original authors and refrain from using the dataset for publication or commercial purposes without explicit written permission. The dataset is provided "as is" without warranty, and the authors are not responsible for any issues arising from its use.

## 3. Problem Summary
The optimization model addresses Denmark's conservation goals by selecting agricultural areas to be converted into protected natural areas. The model considers biodiversity potential, spatial connectivity, and specific conservation objectives. 

### Key Objectives:
- **Maximize Biodiversity**: Leverage habitat suitability, species richness, and phylogenetic diversity.
- **Ensure Spatial Connectivity**: Prioritize contiguous areas for enhanced ecological functionality.
- **Meet Land-Use Targets**: Comply with government-mandated minimums for forests, wetlands, and other land uses.

### Problem Details:
- **Inputs**:
  - Biodiversity metrics for land uses and cells.
  - Land-use transition costs.
  - Spatial contiguity relationships.
- **Outputs**:
  - Optimized land-use assignments for agricultural cells.
  - Performance metrics, including biodiversity indices and runtime efficiency.

The problem was initially modeled in AMPL but has been adapted here using Python and Gurobi for enhanced flexibility and scalability.

## 4. Repository Structure


```plaintext
SustainScapesOpti/
├── config/                   # Configuration files for optimization scripts
│   ├── config_join_local_search.py
│   ├── config_solve_problem.py
│   ├── config_solve_parallelized.py
├── data/                     # Input datasets
│   ├── cell_ids.csv
│   ├── municip_keys.csv
│   ├── municip_neighbors.txt
│   └── RegionProblems.zip
├── logs/                     # Logs generated during optimization runs
│   ├── Logs_README.md
│   └── (log files generated during execution)
├── results/                  # Results from optimization scripts
│   └── (output files with optimized solutions)
├── src/                      # Core source code
│   ├── join_and_local_search.py
│   ├── solve_problem.py
│   ├── solve_parallelized.py
│   ├── utils.py
│   └── README.md
├── run_all.py
├── .gitignore
├── LICENSE
└── README.md                 # Main repository README
```

### 4.1 Directories and Key files:
- **`/config`**: Configuration files for running the optimization scripts in ../src. Must be set up properly before running.
    - **`config_solve_problem`**: Configuration for `solve_problem.py`.
    - **`config_solve_paralellized`**: Configuration for `solve_parallelized.py`.
    - **`config_join_local_search`**: Configuration for `join_and_local_search.py`.
- **`/data`**: Input datasets, including cell IDs, municipality mappings, and adjacency relationships.
- **`/logs`**: Logs generated during optimization runs.
- **`/results`**: Output files containing the optimized solutions.
- **`/src`**: Core source code for solving the optimization problem.
    - **`solve_problem.py`**: Python file that solves a single region separately.
    - **`solve_parallelized.py`**: Python file that solves for all regions in parallel.
    - **`join_and_local_search.py`**: Python file that joins separate solutions, joins them and then performs local search on them.
- **`run_all.py`**: Python file that runs **`solve_parallelized.py`** and **`join_and_local_search.py`**.


## 5. Getting Started

### 5.1 Dependencies:

- Python 3.8+
- Gurobi
- Libraries:
  - `numpy`
  - `pandas`
  - `gurobipy`

### 5.2 Usage

1. Set up Configuration

Before running any scripts, ensure the configuration files in the **`/config`** directory are set up properly:
- **`/config_solve_problem.py`**: Configure the correct paths to the files to solve an individual regional problem. To change datasets, change the path in the variable **`name`** and **`problem_path`**.
- **`/config_solve_parallelized.py`**: Configure parameters and path for joining solutions and performing local search optimization. To add or change datasets, just change the path in the variables **`names`**, **`problems_pathlist`** and **`problem_path`**.
- **`/config_join_local_search.py`**: Configure parameters and path for joining solutions and performing local search optimization. To add or change datasets, just change the path in the variables **`pathlist`** and **`problem_path`**.

All paths are relative to the main folder.

2. Prepare Data

Ensure the input data files in the **`/data`** directory are available.

3. Running the Scripts

To run the whole algorithm, run the file **`run_all.py`** from the main folder. It is also possible to run each step separately running the corresponding file from **`/src`** 

4. Log Monitoring

Logs for each run are saved in the **`/logs`** directory. Refer to **`/logs/README.md`** for details.

5. Output

The results of the optimization process are saved in the **`/results`** directory. Check this directory for output files with optimized solutions. To evaluate the performance of the partitions see how to do it **`/results/README.md`**.


## 6 References

The original SustainScapes optimization repository can be found at [SustainScapesOptimization](https://github.com/Sustainscapes/OptimizationDataset).

## 7. Contributions

Repository made by students of the Pontificia Univerisdad Católica de Chile in assosiation with SustainScapes and Aarhus University.

## 8. Licence

This project is licensed under the terms specified in the LICENSE file. Ensure compliance when using this repository.