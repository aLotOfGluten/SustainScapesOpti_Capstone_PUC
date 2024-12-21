
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
- The `{script}` part of the filneame identifies the source script.
`localsearch` if created by `join_local_search.py` and
`problem` if created by `solve_problem.py`.
- For detailed information about the format and structure of Gurobi logs, refer to the [Gurobi Logging Documentation](https://docs.gurobi.com/projects/optimizer/en/current/concepts/logging.html).

---
## Logs Created by `solve_problem.py`
### **Summary problem solve**
**Naming Convention
