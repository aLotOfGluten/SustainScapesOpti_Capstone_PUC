
# Logs Directory Documentation

The logs resulting from running the scripts are stored in this directory. Running `run_all.py` generates log files through `src/solve_parallelized` for each of the problems given and logfiles for the local search afterwards through `src/join_and_local_search.py`.

Additionaly, the directory contains example files in `archived/`.

---
## Shared Log types
### **Gurobi Logs**
**Naming Convention**:  
```
gurobi_log_{script}_{identifier}.log
```

These logs capture the output from Gurobi's optimization processes.  
- If the algorithm invokes Gurobi multiple times, the logs are appended sequentially.  
- The `{script}` part of the filename identifies the source script.
`localsearch` if created by `join_local_search.py`,
`problem` if created by `solve_problem.py` and `parallelized` if created by `solve_parallelized.py`.
- For detailed information about the format and structure of Gurobi logs, refer to the [Gurobi Logging Documentation](https://docs.gurobi.com/projects/optimizer/en/current/concepts/logging.html).

---
## Logs Created by `solve_problem.py` or `solve_parallelized.py`
### **Summary Problem Solve**
**Naming Convention**
```
summary_{script}_{identifier}.txt
```
Where `{script}` clarifies whether it was created by `solve_problem.py` or `solve_parallelized.py`.\
These logs provide a summary of the algorithm's run. These include
- Problem identifier
- Time importing problem variables and restrictions
- Time solving the problem with Gurobi
- Objective value found

**Example**:
```
Summary solve problem midtjylland:
Time importing problem: 310s
Time solving problem: 3008s
Objective value: 6310.386787551
```

---
## Logs Created by `join_local_search.py`
### **Summary Local Search**
**Naming Convention**
```
summary_localsearch_{identifier}.txt
```
These logs provide a summary of the algorithm's run. These include
- Problem identifier
- Ratio of size of cluster used for local search to the size of the
main problem (%)
- Time importing problem variables and restrictions
- Total time in local search algorithm
- Number of iterations of the local search algorithm
- Initial objective value:
    - If set to evaluate the initial solution, its objective value
    - Otherwise, objective value after first iteration of local search
- Objective value found after local search

**Examples**:\
If initial solution is evaluated
```
Summary Local Search 2:
Ratio: 3.0%
Time importing problem: 1089s
Total time in Local Search: 11413s
Number of iterations made: 8
Objective value initial solution: 14672.781699998592
Final objective value achieved: 14687.3518
```
If initial solution is not evaluated
```
Summary Local Search 3:
Ratio: 7.0%
Time importing problem: 1129s
Total time in Local Search: 10766s
Number of iterations made: 6
Objective value after first iteration: 14673.1325
Final objective value achieved: 14681.7874
```
---
### **Local Search Log Files**
**Naming Convention**
```
log_localsearch_{identifier}.txt
```
This file contains information about the changes to the solutions for each iteration of the local search. These include:
 - Number of the iteration
 - Time elapsed since the beginning of the local search (in seconds).
 - Time taken for the current iteration (in seconds).
 - Number of cells modified from the previous solution.
 - The objective value achieved with the current solution.

**Example**:
```
Iter total_time iter_time cells_changed objval
1 1494.5488781929016 1494.5488781929016 6473 14121.48989999852
```

---
### **Municipality Selection Log**
**Naming Convention**
```
municip_log_{identifier}.txt
```
These logs document the selection of municipalities used for each iteration of the local search algorithm. It stores the municipalities by their IDs given in `data/municip_keys.csv`. For more information on these IDs, please refer to `data/README.md`.

**Example**:
```
Iter: municipalities used
1: 18, 73, 23, 12, 3, 22, 36, 33, 43
2: 46, 74, 50, 88, 11, 87
3: 79, 64, 81
```