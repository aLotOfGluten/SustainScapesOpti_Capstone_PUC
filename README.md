# SustainScapesOpti_Capstone_PUC

Conservation and Biodiversity Optimization for Denmark.

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


```
plaintext
SustainScapesOpti/
├── config/                   # Configuration files for optimization scripts
│   ├── config_all.py
│   ├── config_join_local_search.py
│   ├── config_solve_parallelized.py
│   ├── config_solve_problem.py
│   └── README.md
├── data/                     # Input datasets
│   ├── cell_ids.csv
│   ├── municip_keys.csv
│   ├── municip_neighbors.txt
│   ├── RegionProblems.zip
│   └── README.md
├── logs/                     # Log files generated during execution
│   └── README.md
├── results/                  # Results from optimization scripts
│   └── README.md
├── src/                      # Core source code
│   ├── join_and_local_search.py
│   ├── solve_parallelized.py
│   ├── solve_problem.py
│   ├── utils.py
│   └── README.md
├── run_all.py
├── .gitignore
├── LICENSE
└── README.md                 # Main repository README
```

### 4.1 Directories and Key files:
- **`/config`**: Configuration files for running the optimization scripts in `../src`. Must be set up properly before running.
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

All paths are relative to the main directory.

2. Prepare Data

Ensure the input data files in the **`/data`** directory are available.

3. Running the Scripts

To run the whole algorithm, run the file **`run_all.py`** from the main folder. It is also possible to run each step separately running the corresponding file from **`/src`** 

4. Log Monitoring

Logs for each run are saved in the **`/logs`** directory. Refer to **`/logs/README.md`** for details.

5. Output

The results of the optimization process are saved in the **`/results`** directory. Check this directory for output files with optimized solutions. To evaluate the performance of the partitions see how to do it **`/logs/README.md`**.

## 6. The solving algorithm

### 6.1 Local Search

In order to estimate the solution to the optimization problem, a novel algorithm was designed following the structure of **local search**. The algorithm has the following structure:

1. **Initial solution**: The original .dat file is divided into smaller, significantly faster to solve .dat's. This .dat's are then solved in paralel utilizing *Gurobi* and merged in order to form the initial solution for the **local search**.

2. **Local Search**:  
    1. Firstly, a random Denmark comune is selected.
    2. Then, through a **BFS** algorithm across the comunes, a cluster comprissed of neighbor comunes is created. **BFS** only stops adding new comunes to the cluster once it has covered a certain rate of the total land area. This total land coverage percentage can be changed via the `rate` parameter in the respective `../config/..` files. In the case the **BFS** finds itself without any neighbors, a new strating point is selected and used in conjuntion.
    3. The cells inside the cluster are then **re-optimized** using *Gurobi*, while the rest of the cells stay locked in their current assignment.  
    4. After Gurobi solves for the freed cells, we obtain a new solution. We then **update** our “best-known solution” if the new one is better according to the optimization objective. 
    5. The process repeats itself until either a **maximum number of iterations** or a **time limit** is reached.

### 6.1.1. The Rate parameter

The `rate` parameter is one of the main parameters of algorith. A rate closer to 0 means selecting low portions of land to **re-optimize** in each iteration meanwhile having a `rate` closer to 100 means solving the entire problem altoghether.

Consecuently, having a small `rate` means faster iterations but less change to optimality and a big `rate` means slower iterations but more change to optimallity.

It is advised to experiment with different `rate`'s, altough values between 0.1 and 0.6 are advised.

### 6.2 Parallelizing

In **step 1.** of local search, several subproblems (.dat's) were solved in parallel. In order to do this the algorith is instructed to:

1. Determine the number of cores in the system.
2. Assign a number of threads to each subproblem with a minimum of two threads per subproblem. In the case this is not feasable, as in for example, 8 cores with 100 subproblems, each subproblem is assignated 2 threads.
3. The maximum number of parallel jobs is determined as max_workers = min(subproblem_count, num_cores // 2).
4. The python object concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) is utilized to schedulle the threads.

Given the process, there is no oversubscription.


## 7. References

The original SustainScapes optimization repository can be found at [SustainScapesOptimization](https://github.com/Sustainscapes/OptimizationDataset).

## 8. Contributions

Repository made by students of the Pontificia Univerisdad Católica de Chile in assosiation with SustainScapes and Aarhus University.

## 9. Licence

This project is licensed under the terms specified in the LICENSE file. Ensure compliance when using this repository.