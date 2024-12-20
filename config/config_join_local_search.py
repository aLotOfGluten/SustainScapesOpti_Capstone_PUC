# Description: Configuration file for the Local Search algorithm

# Id (var): Identifies the test from other runs of the same algorithm
# It is used to name the output files,
# so it is recommended to change it to avoid overwriting
Id = 0

# Ratio (var): ratio of the number of cells freed in the local search
# as a percentage of the total number of cells in the problem
ratio = 10.0

# Time limit (var): time limit for the Local Search algorithm
max_time = 1000

# Iterations (var): maximum number of iterations for the Local Search algorithm
# The algorithm will stop if either the time limit or 
# the maximum number of iterations is reached
max_iter = 100

# Join (var): join restrictions and evaluate initial solution
# before Local Search.
# If False, the Local Search will not evaluate the initial solution
# and will start improving it with local search immediately
join_rest = True

# Problem (input): file path of the .dat with complete problem
problem_path = 'data/Denmark.dat'

# Path_list (input): files to be imported as initial solution
pathlist = [
    'problem_midtjylland_vars.txt',
    'problem_nordjylland_vars.txt',
    'problem_sjaelland_vars.txt',
    'problem_syddanmark_vars.txt'
]

# Cell ids (input): csv file with the cells ids and the municipality they belong to
cell_ids = 'data/cell_ids.csv'

# Municipalities neighbors (input): txt file with the neighbors of each municipality
# a.k.a ids of adjacent municipalities
municip_neighbors = 'data/municip_neighbors.txt'

# Results (output): file path for the file with the asignment of cells
# in found solution
results_path = f'results/vars_localsearch_{Id}.csv'

# Summary (output): file path of the summary of the results of the Local Search
summary_path = f'logs/summary_localsearch_{Id}.txt'

# Gurobi LogFile (output): file path of the Gurobi log file
gurobi_log_file = f'logs/gurobi_log_localsearch_{Id}.log'

# Log File (output): file path of the log file of the Local Search
log_file = f'logs/log_localsearch_{Id}.log'

# Municipality log (output):
# municipalities used in each iteration of Local Search
municip_log_path = f'logs/municip_localsearch_log_{Id}.txt'