# Description: Configuration file for the Local Search algorithm

# Name (var): Identifies the test from other runs of the same script
# It is used to name the output files,
# so it is recommended to change it to avoid overwriting
name = 'midtjylland'

# Problem (input): file path of the .dat with complete problem
problem_path = 'data/midtjylland.dat'

# Results (output): file path for the file with the asignment of cells
# in found solution
results_path = f'results/vars_problem_{name}.csv'

# Summary (output): file path of the summary of the results of the Local Search
summary_path = f'logs/summary_problem_{name}.txt'

# Gurobi LogFile (output): file path of the Gurobi log file
gurobi_log_file = f'logs/gurobi_log_problem_{name}.log'
