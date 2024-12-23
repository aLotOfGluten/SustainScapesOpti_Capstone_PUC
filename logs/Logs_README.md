
# Logs Directory Documentation

The logs resulting from running the scripts are stored in this directory.

---

### **Summary Logs**
**Naming Convention**:  

---

### **Gurobi Logs**
**Naming Convention**:  
```
gurobi_log_{script}_{identifier}.log
```

These logs capture the output from Gurobi's optimization processes.  
- If the algorithm invokes Gurobi multiple times, the logs are appended sequentially.  
- For detailed information about the format and structure of Gurobi logs, refer to the [Gurobi Logging Documentation](https://docs.gurobi.com/projects/optimizer/en/current/concepts/logging.html).

---

### **Local Search Logs**
**Naming Convention**:  
```
log_localsearch_{identifier}.log
```

These logs track the progress of the local search algorithm.  
For each iteration, the following information is recorded:  
- **Iteration Number**: The current iteration of the local search.  
- **Total Elapsed Time**: Time elapsed since the beginning of the local search (in seconds).  
- **Iteration Duration**: Time taken for the current iteration (in seconds).  
- **Cells Changed**: Number of cells modified from the previous solution.  
- **Objective Value**: The solution's objective value.

---

### **Municipality Logs**
**Naming Convention**:  
```
municip_log_{identifier}.log
```

These logs document the selection of municipalities during the local search algorithm.  
For each iteration, the logs store the **IDs of municipalities** added to the _cluster_.

---

### **Notes**
- Use consistent and descriptive identifiers for `{script}` and `{identifier}` to ensure logs are easy to track and manage.
- If additional log types are introduced in the future, follow the naming conventions to maintain consistency.

