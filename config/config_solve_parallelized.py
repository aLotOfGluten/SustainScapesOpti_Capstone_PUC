# Description: Configuration file for ../scr/solve_parallelized.py

# Id (var): Identifies the test from other runs of the same algorithm
# It is used to name the output files,
# so it is recommended to change it to avoid overwriting
Id = 0

# Problem (input): file path of the .dat with complete problem
problem_path = 'data/Denmark.dat'

# Name of problems:

name = [
    'midtjylland',
    'nordjylland',
    'sjaelland',
    'syddanmark'
]

# Path_list (input): files to be imported as initial problems.
problems_pathlist = [
    'data/midtjylland.dat',
    'data/nordjylland.dat',
    'data/sjaelland.dat',
    'data/syddanmark.dat'
]

# Number of subproblems/regions
subproblem_count = len(problems_pathlist)

# Results (output): file path for the file with the asignment of cells
# in found solution

results_path = [
    f'results/vars_parallelized_{Id}_midtjylland.txt',
    f'results/vars_parallelized_{Id}_nordjylland.txt',
    f'results/vars_parallelized_{Id}_sjaelland.txt',
    f'results/vars_parallelized_{Id}_syddanmark.txt'
]

# Summary (output): file path of the summary of the results.
summary_path = [
    f'logs/summary_parallelized_{Id}_midtjylland.txt',
    f'logs/summary_parallelized_{Id}_nordjylland.txt',
    f'logs/summary_parallelized_{Id}_sjaelland.txt',
    f'logs/summary_parallelized_{Id}_syddanmark.txt'
]

# Gurobi LogFile (output): file path of the Gurobi log file
gurobi_log_file = [
    f'logs/parallelized_gurobi_log_{Id}_midtjylland.log',
    f'logs/parallelized_gurobi_log_{Id}_nordjylland.log',
    f'logs/parallelized_gurobi_log_{Id}_sjaelland.log',
    f'logs/parallelized_gurobi_log_{Id}_syddanmark.log',
]
