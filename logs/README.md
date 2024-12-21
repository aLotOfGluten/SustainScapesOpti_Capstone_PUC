The logs resulting from running the scripts are stored here.\
There are several types of logs:

### Summary
Names follow the naming convention\
summary_{script}_{identifier}.txt\
Summary of the run of the algorithm.
Includes run times of different steps of the algorithm,
as well as main results like objective value of the optimization problem.

### Gurobi logs
Names follow the naming convention\
gurobi_log_{script}_{identifier}.log\
When the algorithm runs gurobi optimization multiple times,
they are written one after the other.\
More information about the format of gurobi logs can be found at
https://docs.gurobi.com/projects/optimizer/en/current/concepts/logging.html

### Local Search logs
Names follow the naming convention\
log_localsearch_{identifier}.log\
Logs for the local search algorithm.
They save the following information for each iteration of the algorthm:\
- Number of iteration
- Total time elapsed since the beginning of the local search (seconds)
- Duration of the current iteration (seconds)
- Amount of cells changed from the previous solution
- Objective value of the solution found

### Municipality logs
Names follow the naming convention\
municip_log_{identifier}.log\
Logs for the selection of municipalities in the local searh algorithm.
For each iteration, it stores the ids of the municipalities added to the
_cluster_.
