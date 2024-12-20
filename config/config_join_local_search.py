# Description: Configuration file for the Local Search algorithm

# Id: Identifies the test from other runs of the same algorithm
Id = 0

# Problem: file path of the .dat with complete problem
problem_path = 'data/Denmark.dat'

# Logfile: file path of the Gurobi log file
logfile = f'logs/gurobi_log_localsearch_{Id}.log'

# Path_list: files to be imported as initial solution
pathlist = [
    'problem_midtjylland_vars.txt',
    'problem_nordjylland_vars.txt',
    'problem_sjaelland_vars.txt',
    'problem_syddanmark_vars.txt'
]

# Join: join restrictions and evaluate initial solution before the Local Search
# If False, the Local Search will not evaluate the initial solution,
# and will start improving it with local search immediately
join_rest = True

# Cell ids: csv file with the cells ids and the municipality they belong to
cell_ids = 'data/cell_ids.csv'

# Logs the municipalities used in each iteration of Local Search
municip_log_path = f'logs/municip_localsearch_log_{Id}.txt'