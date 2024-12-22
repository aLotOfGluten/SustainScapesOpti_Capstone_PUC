
# Logs Directory Documentation

The logs resulting from running the scripts are stored in this directory.

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
`localsearch` if created by `join_local_search.py` and
`problem` if created by `solve_problem.py`.
- For detailed information about the format and structure of Gurobi logs, refer to the [Gurobi Logging Documentation](https://docs.gurobi.com/projects/optimizer/en/current/concepts/logging.html).

---
## Logs Created by `solve_problem.py`
### **Summary problem solve**
**Naming Convention**
```
summary_problem_{identifier}.txt
```
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