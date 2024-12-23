
# Logs Directory Documentation (`logs`)

The logs and the summaries resulting from running the scripts are stored in this directory.

It's important to note that the file `run_all.py` runs both `solve_parallelized.py` and `join_and_local_search.py` and therefore, produces both types of *logs*.

## Files description

#### **`Summary Logs (.txt)`**

Sumary logs provide a summary of the algorithm's run. They include: 

<<<<<<< HEAD
=======
---
## Logs Created by `solve_problem.py` or `solve_parallelized.py`
### **Summary problem solve**
**Naming Convention**
```
summary_problem_{identifier}.txt
```
These logs provide a summary of the algorithm's run. These include
>>>>>>> origin/main
- Problem identifier
- Time importing problem variables and restrictions
- Time solving the problem with Gurobi
- Objective value found
- Parameters and data from **local search**.

#### **`Gurobi Logs (.log)`**


Gurobi logs capture the output from Gurobi's optimization processes. These include:
- Problem identifier
- Ratio of size of cluster used for local search to the size of the main problem (%)
- Time importing problem variables and restrictions
- Total time in local search algorithm
- Number of iterations of the local search algorithm
- Objective value found after local search


More information about them can be found at the[Gurobi Logging Documentation](https://docs.gurobi.com/projects/optimizer/en/current/concepts/logging.html).
- If the algorithm invokes Gurobi multiple times, the logs are appended sequentially.  


## **Naming convention**

**Sumary logs**
```
summary_{script}_{identifier}.txt
```
**Gurobi logs**

```
gurobi_log_{script}_{identifier}.log
```

Where:

- `{script}`: Identifies the source script.
    - `script` = `parallelelized` if it originates from `solve_parallelized` or `run_all.py`.
    - `script` = `problem` if it originates from `solve problem.py`
    - `script` = `localsearch` if it originates from `localsearch.py` or `run_all.py`.
- `{identifier}`: Identifier for the test.