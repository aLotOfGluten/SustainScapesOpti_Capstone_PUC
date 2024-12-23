import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd
from time import time
import re
import sys
from warnings import warn
import config.config_all as config
from src.utils import find_cluster


def main():
    t0 = time()

    # Setting Local Search parameters
    ratio = config.ratio
    if ratio < 0 or ratio > 100:
        sys.exit('Ratio must be between 0 and 100')
    max_time = config.max_time
    max_iter = config.max_iter

    # Importing problem
    # Creating sets and dictionaries
    cells = []  # List of cells
    land_uses = {}  # Set of land uses
    forest_land_uses = {}  # Set of forest land uses
    wet_land_uses = {}  # Set of wet land uses
    E = {}  # List of edges between cells

    # Parameters
    # Format for the next 3 dictionaries is
    # {cell: {land_use: num}, ...}
    # Existing nature for each land use and cell
    existing_nature = dict()
    # Richness for each land use and cell
    richness = dict()
    # Phylogenetic diversity for each land use and cell
    phylo_diversity = dict()

    transition_cost = 1
    can_change = dict()  # Indicates if a cell can change or not
    # Dictionary {celda: var_bin}

    b = 0  # Maximum budget
    min_for = 0  # Minimum of forest land uses
    min_wet = 0  # Minimum of wet land uses
    min_lan = 0  # Minimum of land uses
    spatial_contiguity_bonus = 0  # Spatial contiguity bonus

    default_can_change = 0
    default_existing_nature = 0
    default_richness = 0
    default_phylo_diversity = 0

    # Asigning values to the sets and dictionaries
    with open(config.problem_path, 'r') as file:
        line_is_can_change = False
        for line in file:
            if line_is_can_change:
                can_change_list = re.findall(r'\[(\d+)\] ([\d]+)', line)
                # {cell: var_bin}
                for cell_id, value in can_change_list:
                    can_change[cell_id] = int(value)
                for cell_id in cells:
                    if cell_id not in can_change.keys():
                        can_change[cell_id] = default_can_change

            elif line.startswith('set Cells'):
                cells = re.findall(r'\d+', line)

            elif line.startswith('set Landuses'):
                land_uses = set(re.findall(r'\w+', line.split(":=")[1]))

            elif line.startswith('set ForestLanduses'):
                forest_land_uses = set(re.findall(r'\w+', line.split(":=")[1]))

            elif line.startswith('set WetLanduses'):
                wet_land_uses = set(re.findall(r'\w+', line.split(":=")[1]))

            elif line.startswith('set E'):
                E = re.findall(r'\((\d+),(\d+)\)', line.split(":=")[1])

            elif line.startswith('param Existingnature'):
                # Dict of dict {cell: {landuse: num}}
                existing_nature_list = re.findall(r'\[(\w+),(\d+)\] (\d+)',
                                                  line)
                # There can be no more than one existing nature in a cell
                for land_use, cell_id, value in existing_nature_list:
                    existing_nature[cell_id] = {land_use: int(value)}
                for cell_id in cells:
                    if cell_id in existing_nature.keys():
                        for land_use in land_uses:
                            if land_use not in existing_nature[cell_id].keys():
                                existing_nature[cell_id][land_use] = \
                                    default_existing_nature
                    else:
                        existing_nature[cell_id] = {
                            land_use:
                            default_existing_nature for land_use in land_uses
                        }

            elif line.startswith('param PhyloDiversity'):
                # Dict of dict {cell: {landuse: num}}
                phylo_diversity_list = re.findall(r'\[(\w+),(\d+)\] ([\d.]+)',
                                                  line)
                for land_use, cell_id, value in phylo_diversity_list:
                    if cell_id in phylo_diversity.keys():
                        phylo_diversity[cell_id][land_use] = float(value)
                    else:
                        phylo_diversity[cell_id] = {land_use: float(value)}
                for cell_id in cells:
                    if cell_id in phylo_diversity.keys():
                        for land_use in land_uses:
                            if land_use not in phylo_diversity[cell_id].keys():
                                phylo_diversity[cell_id][land_use] = \
                                    default_phylo_diversity
                    else:
                        phylo_diversity[cell_id] = {
                            land_use:
                            default_phylo_diversity for land_use in land_uses
                        }

            elif line.startswith('param Richness'):
                # Dict of dict {cell: {landuse: num}}
                richness_list = re.findall(r'\[(\w+),(\d+)\] ([\d.]+)', line)
                for land_use, cell_id, value in richness_list:
                    if cell_id in richness.keys():
                        richness[cell_id][land_use] = float(value)
                    else:
                        richness[cell_id] = {land_use: float(value)}
                for cell_id in cells:
                    if cell_id in richness.keys():
                        for land_use in land_uses:
                            if land_use not in richness[cell_id].keys():
                                richness[cell_id][land_use] = default_richness
                    else:
                        richness[cell_id] = {
                            land_use: default_richness
                            for land_use in land_uses
                        }

            elif line.startswith('param b'):
                b = float((re.findall(r'\d+', line))[0])

            elif line.startswith('param MinFor'):
                min_for = float((re.findall(r'\d+', line))[0])

            elif line.startswith('param MinWet'):
                min_wet = float((re.findall(r'\d+', line))[0])

            elif line.startswith('param MinLan'):
                min_lan = float((re.findall(r'\d+', line))[0])

            elif line.startswith('param TransitionCost'):
                transition_cost = float((re.findall(r'\d+', line))[0])

            elif line.startswith('param SpatialContiguityBonus'):
                spatial_contiguity_bonus = float(
                    (re.findall(r'([\d.]+)', line))[0]
                )

            elif line.startswith('param CanChange'):
                line_is_can_change = True

    # Creation of the model
    model = gp.Model("LandUseOptimization")

    # Variables
    LanduseDecision = model.addVars(land_uses, cells, vtype=GRB.BINARY,
                                    name="LanduseDecision")
    Contiguity = model.addVars(land_uses, E, vtype=GRB.BINARY,
                               name="Contiguity")

    # Objective function: maximize the conservation index
    model.setObjective(
        gp.quicksum(
            LanduseDecision[l, c] * richness[c][l] *
            phylo_diversity[c][l] * can_change[c]
            for l in land_uses for c in cells
        ) +
        spatial_contiguity_bonus * gp.quicksum(
            Contiguity[l, i, j] * can_change[i] * can_change[j] +
            existing_nature[i][l] * LanduseDecision[l, j] * can_change[j]
            for (i, j) in E for l in land_uses
        ),
        GRB.MAXIMIZE
    )

    # Constraints

    # Proportional use constraint: no more than one land use per cell
    for c in cells:
        model.addConstr(
            gp.quicksum(LanduseDecision[l, c] for l in land_uses) <= 1,
            name=f"ProportionalUse_{c}"
        )

    # Minimum cells per land use (except 'Ag') constraint
    for l in land_uses:
        if l != 'Ag':
            model.addConstr(
                gp.quicksum(LanduseDecision[l, c] for c in cells) >= min_lan,
                name=f"MinCellPerLandUse_{l}"
            )

    # Can't change land use to agriculture
    for c in cells:
        model.addConstr(LanduseDecision['Ag', c] == 0,
                        name=f"NoAgriculture_{c}")

    # Minumum forest land uses constraint
    model.addConstr(
        gp.quicksum(
            LanduseDecision[l, c] for l in forest_land_uses for c in cells
        ) >= min_for, name="MinimumForest"
    )

    # Minimum wet land uses constraint
    model.addConstr(
        gp.quicksum(
            LanduseDecision[l, c] for l in wet_land_uses for c in cells
        ) >= min_wet, name="MinimumWet"
    )

    # Budget constraint
    model.addConstr(
        gp.quicksum(
            LanduseDecision[l, c] * transition_cost
            for l in land_uses for c in cells
        ) <= b, name="Budget"
    )

    # Contiguity definition constraint
    for l in land_uses:
        for (i, j) in E:
            model.addConstr(Contiguity[l, i, j] <=
                            LanduseDecision[l, i],
                            name=f"DefineContiguity1_{l}_{i}_{j}")
            model.addConstr(Contiguity[l, i, j] <=
                            LanduseDecision[l, j],
                            name=f"DefineContiguity2_{l}_{i}_{j}")
            model.addConstr(Contiguity[l, i, j] >=
                            LanduseDecision[l, i] + LanduseDecision[l, j] - 1,
                            name=f"DefineContiguity3_{l}_{i}_{j}")

    # Importing initial solution
    solution = {}
    cells_solution = set()
    for path in config.pathlist:
        with open(path, 'r') as file:
            for line in file:
                cell, land_use = line.strip().split()
                if cell in cells_solution:
                    if solution[cell] != land_use:
                        warn(
                            f'Two different land uses for cell {cell}, '
                            f'used the one in {path}'
                        )
                solution[cell] = land_use

    # Gurobi configuration
    model.setParam('LogToConsole', 0)
    model.setParam('LogFile', config.gurobi_log_file)
    model.setParam('Method', 3)
    model.setParam('ConcurrentMethod', 3)

    # Clearing the log file
    with open(config.gurobi_log_file, 'w') as file:
        pass

    # Evaluating initial solution
    if config.eval:
        for cell, land_use in solution.items():
            model.addConstr(LanduseDecision[land_use, cell] == 1,
                            name=f"Fixed_{cell}")

        model.optimize()

        for cell in solution.keys():
            model.remove(model.getConstrByName(f"Fixed_{cell}"))
        
        initial_objval = model.objVal

    # Importing municipalities and neighbors
    df = pd.read_csv(config.cell_ids).astype(str)
    municip_dict = df.groupby('municip_id')['cell'].apply(set).to_dict()
    municip_sizes = {k: len(v) for k, v in municip_dict.items()}
    neighbors = {}
    with open(config.municip_neighbors, 'r') as f:
        f.readline()
        for i in range(len(municip_dict.keys())):
            s = f.readline().strip()
            a, b = s.split(';')
            if not b:
                neighbors[a] = set()
            else:
                neighbors[a] = set(b.split(','))

    tf = time()
    t_import = tf - t0

    with open(config.summary_path, 'w') as file:
        file.write(f'Summary Local Search {config.Id}:\n')
        file.write(f'Ratio: {ratio}%\n')
        file.write(f'Time importing problem: {round(t_import)}s\n')

    # We run Local Search
    iter = 0
    t_total = 0
    total_times = []
    times = []
    vals = []
    total_cells = len(cells)
    cant_free_cells = round(total_cells * ratio / 100)

    with open(config.log_file, 'w') as file:
        file.write('Iter total_time iter_time cells_changed objval\n')
    
    with open(config.municip_log_path, 'w') as file:
        file.write('iter: municipalities used\n')

    abs_t0 = time()
    while t_total < max_time and iter < max_iter:
        t0 = time()
        
        # Choose the cells to free
        cluster = find_cluster(
            np.random.choice(list(municip_dict.keys())),
            cant_free_cells,
            municip_dict,
            municip_sizes,
            neighbors,
            iter + 1
        )
        
        # Fix the cells
        fixed_cells = set()
        for cell, land_use in solution.items():
            if cell not in cluster:
                fixed_cells.add(cell)
                model.addConstr(LanduseDecision[land_use, cell] == 1,
                                name=f"Fixed_{cell}")
                
        # Solve the model
        model.optimize()
        tf = time()

        # Save and update time, gap and iter
        dt = tf - t0
        times.append(dt)
        t_total += dt
        total_times.append(t_total)
        
        vals.append(model.objVal)
        iter += 1

        # Update the solution
        new_sol = {}
        cant_cambios = 0
        old_cells = set(solution.keys())
        for c in cells:
            for l in land_uses:
                if LanduseDecision[l, c].x > 0.5:
                    new_sol[c] = l
        new_cells = set(new_sol.keys())
        cant_cambios = len(old_cells.symmetric_difference(new_cells))
        for c in old_cells.intersection(new_cells):
            if new_sol[c] != solution[c]:
                cant_cambios += 1
        solution = new_sol

        # Remove the fixed variables
        for c in fixed_cells:
            model.remove(model.getConstrByName(f"Fixed_{c}"))

        # Save the results of the iteration
        with open(config.log_file, 'a') as file:
            file.write(f'{iter} {t_total} {dt} '
                       f'{cant_cambios} '
                       f'{vals[-1]}\n')

        # Save the solution found
        with open(config.results_path, 'w') as file:
            for cell, land_use in solution.items():
                file.write(f'{cell} {land_use}\n')

    abs_tf = time()
    abs_time = abs_tf - abs_t0

    # Save the results in summary
    with open(config.summary_path, 'a') as file:
        file.write(f'Total time in Local Search: {round(abs_time)}s\n')
        file.write(f'Number of iterations made: {iter}\n')
        if config.eval:
            file.write(f'Objective value initial solution: {initial_objval}\n')
        else:
            file.write(f'Objective value after first iteration: {vals[0]}\n')
        file.write(f'Final objective value achieved: {vals[-1]}\n')



if __name__ == '__main__':
    main()
