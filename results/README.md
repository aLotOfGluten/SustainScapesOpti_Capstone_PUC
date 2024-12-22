# Configuration Files Directory (`results`)

This directory contains the results of the optimization process, either resulting from solve_problem.py or from join_and_local_search.

---

### Types of files found:


- **`vars_problem_{test_name}.csv`**: .csv file that contains the information of the optimized land use for each cell in the problem. The format for each row is {cell id} | {land use}.

- **`summary_problem_{test_name}.txt`**: .txt file that contains a summary of optimization solving process. It includes the time importing the optimization problem, the time solving the optimization problem and the maximum value of the optimization function.