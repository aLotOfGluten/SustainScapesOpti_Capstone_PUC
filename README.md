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
SustainScapesOpti_Capstone_PUC/
├── config/                   # Configuration files for optimization scripts
│   ├── config_run_all.py
│   ├── config_solve_problem.py
│   └── README.md
├── data/                     # Input datasets
│   ├── cell_ids.csv
│   ├── municip_keys.csv
│   ├── municip_neighbors.txt
│   ├── README.md
│   └── RegionProblems.zip
├── logs/                     # Logs generated during optimization runs
│   ├── archived/
│   └── README.md
├── results/                  # Results from optimization scripts
│   ├── archived/
│   └── README.md
├── src/                      # Core source code
│   ├── join_and_local_search.py
│   ├── README.md
│   ├── solve_parallelized.py
│   ├── solve_problem.py
│   └── utils.py
├── .gitignore
├── LICENSE
├── README.md                 # Main repository README
└── run_all.py
```

### 4.1 Directories and Key files:
- **`/config`**: Configuration files for running the optimization scripts in `../src`. Must be set up properly before running.
    - **`config_solve_problem`**: Configuration for `solve_problem.py`.
    - **`config_run_all`**: Configuration for `solve_parallelized.py` and `join_and_local_search.py`.
- **`/data`**: Input datasets, including cell IDs, municipality mappings, and adjacency relationships.
- **`/logs`**: Logs generated during optimization runs.
- **`/results`**: Output files containing the optimized solutions.
- **`/src`**: Core source code for solving the optimization problem.
    - **`solve_problem.py`**: Python file that solves a single region separately.
    - **`solve_parallelized.py`**: Python file that solves for all regions in parallel.
    - **`join_and_local_search.py`**: Python file that joins separate solutions, joins them and then performs local search on them.
- **`run_all.py`**: Python file that runs **`solve_parallelized.py`** and **`join_and_local_search.py`**.

## 5. The solving algorithm

### 5.1 General algorithm

In order to estimate the solution to the optimization problem, an algorithm was designed following the **local search** approach, with the following structure:

1. **Initial solution**: The original problem is solved by parts and merged  to form the initial solution for the **local search**.

2. **Local Search**:
    Then, the initial solution is improved iteratively by
    1. Firstly, a random municipality or district is selected.
    2. Then, through a **BFS** algorithm across the districts, a connected cluster comprised of municipalities is selected. The search only stops adding new municipalities to the cluster once it has covered a certain portion of the total land area. This total land coverage percentage can be changed in the respective `../config/..` files. In case the algorithm has added an entire connected group of districts, but hasn't yet reached the required size, a new starting point is selected and the new municipalities are added to the cluster.
    3. The cells in the incumbent solution that are not part of the cluster, are fixed by temporarily addind restrictions to the optimization problem. This allows *Gurobi* to find a better feasible solution, similar to the previous one, in a relatively short time.  
    4. After Gurobi solves for the freed cells, we obtain a new solution. We then **update** our “best-known solution” if the new one is better according to the optimization objective. 
    5. Steps 1 through 4 are repeated until a **maximum number of iterations** or a **time limit** is reached.

### 5.1.1. The ratio parameter

The `ratio` parameter is one of the main parameters of algorith. A ratio closer to 0 means selecting small portions of land to **re-optimize** in each iteration meanwhile having a `ratio` closer to 100 means solving almost the entire problem.

Consequently, a small `ratio` means faster iterations but has less potential better optimality and a big `ratio` means slower iterations but more change to optimality.

It is advised to experiment with different `ratio` values for the right balance between number of iterations and effect of each iteration.

### 5.2 Parallelization

In **step 1.** of local search, several subproblems are solved in parallel. In order to do this the algorith is instructed to:

1. Determine the number of cores in the system.
2. Assign a number of threads to each subproblem with a minimum of two threads per subproblem. In the case this is not feasable, as in for example, 8 cores with 100 subproblems, each subproblem is assignated 2 threads.
3. The maximum number of parallel jobs is determined as $max\_workers = min(subproblem\_count, num\_cores // 2)$.
4. The python object concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) is utilized to schedulle the threads.

This is done to avoid oversubscription.


## 6. Using this repository

### 6.1 Dependencies:

- Python 3.8+
- Gurobi
- Libraries:
  - `numpy`
  - `pandas`
  - `gurobipy`

### 6.2 Running the code

#### 1. Set up Configuration

Before running any scripts, ensure the configuration files in the **`/config`** directory are set up properly:
- **`/config_solve_problem.py`**: Configure the correct paths to the files to solve an individual regional problem with `src/solve_problem.py`. To change datasets, change the path in the variable **`name`** and **`problem_path`**.
- **`/config_run_all.py`**: Configure parameters and paths for `run_all.py`,
`src/solve_parallelized.py` and `src/join_and_local_search.py`.
This file is divided is divided into two parts, both must be configured to run
`run_all.py`.\
To run only one of the underlying codes:
  - First half is designed to configure `src/solve_parallelized.py`
  - Second half is designed to configure `src/join_and_local_search.py`

> :warning: **Warning**: It is very important to check the config files, as variables such as `Id`, `Names` and `Name`are used to save output files and incorrect use may lead to overwriting of output files.

All paths are relative to the main directory. For more information about the configuration files, refer to `config/README.md`.

#### 2. Prepare Data

Ensure the input data files in the **`/data`** directory are available and in the correct format.

#### 3. Running the Scripts

To run the whole algorithm, solving the problem by parts, joining them and improving the solution with local search, run the file **`run_all.py`** from the main folder.

It is also possible to run each step separately running the corresponding file from **`/src`**, although it is not recommended, except for debugging specific files.\
**`src/solve_parallelized.py`** solves the partitions of the problem in parallel and **`src/join_and_local_search.py`** starts from an initial solution and uses **local search** to improve it.\
To solve the problem or a subproblem exactly use **`src/solve_problem.py`**.

It is highly recommended to run the scripts in a computer cluster or server, specially for large problems.

> **Note**: Sometimes clusters can have trouble running files directly from the `/src` directory. If path related errors appear when running a scrpit other than `run_all.py`, consider moving the code file to be run, to the main directory.

#### 4. Log Monitoring

Logs for each run are saved in the **`/logs`** directory. Refer to **`/logs/README.md`** for details.

#### 5. Results

The results of the optimization process are saved in the **`/results`** directory. Check this directory for output files with optimized solutions.

## 7. References

The original SustainScapes optimization repository can be found at [SustainScapesOptimization](https://github.com/Sustainscapes/OptimizationDataset).
For more information about using *Gurobi*, please refer to the [Official Documentation](https://docs.gurobi.com/current/)


## 8. Contributions

Repository made by
 - Danilo Aballay
 - Catalina Alegría
 - Valentín Conejeros
 - Vittorio Salvatore
 - Cristóbal Silva

Students of Pontificia Univerisdad Católica de Chile as part of a Capstone course in association with Derek Corcoran from SustainScapes and Aarhus University.

## 9. Licence

This project is licensed under the terms specified in the LICENSE file. Ensure compliance when using this repository.