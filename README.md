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

# **Actualizar acá**

```plaintext
SustainScapesOpti/
├── config/                   # Configuration files for optimization scripts
│   ├── config_join_local_search.py
│   ├── config_solve_problem.py
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
│   ├── utils.py
│   └── README.md
├── .gitignore
├── LICENSE
└── README.md                 # Main repository README
```

### 4.1 Directories and Key files:
- **`/config`**: Configuration files for running the optimization scripts in ../src. Must be set up properly before running.
    - **`config_solve_problem`**: Configuration for `solve_problem.py`.
    - **`config_join_local_search`**: Configuration for `join_and_local_search.py`.
- **`/data`**: Input datasets, including cell IDs, municipality mappings, and adjacency relationships.
- **`/logs`**: Logs generated during optimization runs.
- **`/results`**: Output files containing the optimized solutions.
- **`/src`**: Core source code for solving the optimization problem.
    - **`solve_problem.py`**: Python file that solves a single region separately.
    - **`join_and_local_search.py`**: Python file that joins separate solutions, joins them and then performs local search on them.


## 5. Getting Started

### 5.1 Dependencies:

- Python 3.8+
- Gurobi
- Libraries:
  - `numpy`
  - `pandas`
  - `gurobipy`

### 5.2 Usage

1. Set up 

1. Correr todo junto.


# TO DO
# Terminar acá.


## 6 References

The original SustainScapes optimization repository can be found at [SustainScapesOptimization](https://github.com/Sustainscapes/OptimizationDataset).

## 7. Contributions

Repository made by students of the Pontificia Univerisdad Católica de Chile in assosiation with SustainScapes and Aarhus University.

## 8. Liscence

This project is licensed under the terms specified in the LICENSE file. Ensure compliance when using this repository.
