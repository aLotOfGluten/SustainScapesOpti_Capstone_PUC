from random import shuffle
import numpy as np
import config.config_join_local_search as config

def find_cluster(
        municip_id, size, municip_dict, municip_sizes, neighbors, iter = None
):
    """
    Finds a connected set, or small cluster of municipalities

    Args:
        municip_id (int): id of the municipality to start the search
        size (int): minimum size of the cluster, in number of cells
        municip_dict (dict): dictionary of the municipalities and their cells
        municip_sizes (dict): dictionary of the municipalities and their sizes
                              (number of cells)
        neighbors (dict): dictionary of the neighbors of each municipality
        iter (int): current iteration of the Local Search, for logging purposes

    Returns:
        cluster (set): set of the ids of cells in the cluster
    
    """
    if iter is None:
        iter = '--'

    cluster = set().union(municip_dict[municip_id])
    temp_size = municip_sizes[municip_id]
    queue = list(neighbors[municip_id])
    municips_added = set([municip_id])
    while temp_size < size:
        if queue:
            municip = queue.pop(0)
        else:
            left = [i for i in municip_dict.keys() if i not in municips_added]
            if left:
                municip = np.random.choice(left)
            else:
                break
        cluster = cluster.union(municip_dict[municip])
        temp_size += municip_sizes[municip]
        new_neighbors = [i for i in neighbors[municip]
                         if i not in municips_added]
        if new_neighbors:
            shuffle(new_neighbors)
            queue += new_neighbors
        municips_added.add(municip)
    
    with open(config.municip_log_path, 'a') as file:
        file.write(
            f'{iter}: '+', '.join([str(i) for i in municips_added])+'\n'
        )

    return cluster