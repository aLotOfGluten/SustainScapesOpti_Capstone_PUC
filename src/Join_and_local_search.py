import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd
from time import time
import re
import sys
from warnings import warn
import config.config_join_local_search as config
from utils import find_cluster

def main():
    t0 = time()

    ratio = config.ratio
    if ratio < 0 or ratio > 100:
        sys.exit('El ratio debe estar entre 0 y 100')
    max_time = config.max_time
    max_iter = config.max_iter

    # Creación de los conjuntos
    cells = []  # Lista de celdas
    land_uses = {}  # Set de usos del suelo
    forest_land_uses = {}  # Set de usos forestales
    wet_land_uses = {}  # Set de usos de tierras húmedas
    E = {}  # Lista de pares de celdas adyacentes

    # Creación de los parámetos
    # Naturaleza existente para cada uso del suelo y celda
    existing_nature = dict()
    # Riqueza para cada uso del suelo y celda
    richness = dict()
    # Diversidad filogenética para cada uso del suelo y celda
    phylo_diversity = dict()
    # los tres últimos son del tipo diccionario de diccionario
    # {celda: {landuse: num}, ...}
    transition_cost = 1
    can_change = dict()  # Indicador de si una celda puede cambiar o no
    # este último diccionario del tipo {celda: var_bin}
    b = 0  # Presupuesto máximo
    min_for = 0  # Mínimo de tierras forestales
    min_wet = 0  # Mínimo de tierras húmedas
    min_lan = 0  # Mínimo de celdas por uso de suelo
    spatial_contiguity_bonus = 0  # Bonificación por contigüidad espacial

    default_can_change = 0
    default_existing_nature = 0
    default_richness = 0
    default_phylo_diversity = 0

    # Asignación de los datos
    with open(config.problem_path, 'r') as file:
        line_is_can_change = False
        for line in file:
            if line_is_can_change:
                can_change_list = re.findall(r'\[(\d+)\] ([\d]+)', line)
                # {celda: var_bin}
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
                # hacer dicc de dicc con {celda: {landuse: num}}
                existing_nature_list = re.findall(r'\[(\w+),(\d+)\] (\d+)',
                                                  line)
                # no puede haber más de un existing nature en una celda
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
                # hacer dicc de dicc con {celda: {landuse: num}}
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
                # hacer dicc de dicc con {celda: {landuse: num}}
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

    # Creación del modelo
    model = gp.Model("LandUseOptimization")

    # Variables
    LanduseDecision = model.addVars(land_uses, cells, vtype=GRB.BINARY,
                                    name="LanduseDecision")
    Contiguity = model.addVars(land_uses, E, vtype=GRB.BINARY,
                               name="Contiguity")

    # Función objetivo: maximizar el índice de conservación
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

    # Restricciones

    # Restricción de uso proporcional: no más de un uso de suelo por celda
    for c in cells:
        model.addConstr(
            gp.quicksum(LanduseDecision[l, c] for l in land_uses) <= 1,
            name=f"ProportionalUse_{c}"
        )

    # Restricción de mínimo de celdas por uso de suelo, excepto 'Ag'
    for l in land_uses:
        if l != 'Ag':
            model.addConstr(
                gp.quicksum(LanduseDecision[l, c] for c in cells) >= min_lan,
                name=f"MinCellPerLandUse_{l}"
            )

    # No permitir agricultura
    for c in cells:
        model.addConstr(LanduseDecision['Ag', c] == 0,
                        name=f"NoAgriculture_{c}")

    # Restricción de mínimo de tierras forestales
    model.addConstr(
        gp.quicksum(
            LanduseDecision[l, c] for l in forest_land_uses for c in cells
        ) >= min_for, name="MinimumForest"
    )

    # Restricción de mínimo de tierras húmedas
    model.addConstr(
        gp.quicksum(
            LanduseDecision[l, c] for l in wet_land_uses for c in cells
        ) >= min_wet, name="MinimumWet"
    )

    # Restricción de presupuesto
    model.addConstr(
        gp.quicksum(
            LanduseDecision[l, c] * transition_cost
            for l in land_uses for c in cells
        ) <= b, name="Budget"
    )

    # Definición de contigüidad
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

    # Importamos la solución inicial
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

    # Optimización del modelo
    model.setParam('LogToConsole', 0)
    model.setParam('LogFile', config.gurobi_log_file)
    model.setParam('Method', 3)
    model.setParam('ConcurrentMethod', 3)

    with open(config.gurobi_log_file, 'w') as file:
        pass

    if config.join_rest:
        for cell, land_use in solution.items():
            model.addConstr(LanduseDecision[land_use, cell] == 1,
                            name=f"Fixed_{cell}")

        model.optimize()

        for cell in solution.keys():
            model.remove(model.getConstrByName(f"Fixed_{cell}"))
        
        initial_objval = model.objVal

    # Importamos las comunas
    df = pd.read_csv(config.cell_ids).astype(str)
    municip_dict = df.groupby('municip_id')['cell'].apply(set).to_dict()
    municip_sizes = {k: len(v) for k, v in municip_dict.items()}
    neighbors = {}
    with open(config.municip_neighbors, 'r') as f:
        f.readline()
        for i in range(99):
            s = f.readline().strip()
            a, b = s.split(';')
            if not b:
                neighbors[a] = set()
            else:
                neighbors[a] = set(b.split(','))

    tf = time()
    t_importacion = tf - t0

    with open(config.summary_path, 'w') as file:
        file.write(f'Summary Local Search {config.Id}:\n')
        file.write(f'Ratio: {ratio}%\n')
        file.write(f'Time importing problem: {round(t_importacion)}s\n')

    # Implementamos Local Search
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
        
        # Elegimos las variables a fijar
        cluster = find_cluster(
            np.random.choice(list(municip_dict.keys())),
            cant_free_cells,
            municip_dict,
            municip_sizes,
            neighbors,
            iter + 1
        )
        fixed_cells = set()
        for cell, land_use in solution.items():
            if cell not in cluster:
                fixed_cells.add(cell)
                model.addConstr(LanduseDecision[land_use, cell] == 1,
                                name=f"Fixed_{cell}")
                
        # Resolvemos el modelo
        model.optimize()
        tf = time()

        # Guardamos y actualizamos tiempo, gap e iter
        dt = tf - t0
        times.append(dt)
        t_total += dt
        total_times.append(t_total)
        
        vals.append(model.objVal)
        iter += 1

        # Actualizamos la solución
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

        # Eliminamos las variables fijadas
        for c in fixed_cells:
            model.remove(model.getConstrByName(f"Fixed_{c}"))

        # Guardamos los resultados de la iteración
        with open(config.log_file, 'a') as file:
            file.write(f'{iter} {t_total} {dt} '
                       f'{cant_cambios} '
                       f'{vals[-1]}\n')

    abs_tf = time()
    abs_time = abs_tf - abs_t0

    # Guardamos los resultados
    with open(config.summary_path, 'a') as file:
        file.write(f'Total time in Local Search: {round(abs_time)}s\n')
        file.write(f'Number of iterations made: {iter}\n')
        if config.join_rest:
            file.write(f'Objective value initial solution: {initial_objval}\n')
        else:
            file.write(f'Objective value after first iteration: {vals[0]}\n')
        file.write(f'Final objective value achieved: {vals[-1]}\n')

    # Guardamos las variables
    with open(config.results_path, 'w') as file:
        for cell, land_use in solution.items():
            file.write(f'{cell} {land_use}\n')


if __name__ == '__main__':
    main()
