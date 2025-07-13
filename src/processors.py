import networkx as nx

"""
Generates a processor network graph for use in task scheduling simulations.

Parameters:
-----------
num_procs : int
    The number of processors to generate.
    Must be one of the following values: 2, 3, or 4.

Returns:
--------
networkx.Graph
    An undirected graph representing a processor network.
    - Each processor is a node labeled 'P1', 'P2', ..., with a 'weight' attribute representing processing speed.
    - Edges represent communication links between processors, with a 'weight' attribute representing communication cost.
    - Each processor has a self-loop (autocycle) with communication cost 1, representing local execution.

Raises:
-------
ValueError
    If `num_procs` is not 2, 3, or 4.
"""

def generate_processors(num_procs: int):
    if num_procs < 2 or num_procs > 4:
        raise ValueError("Oh, no!\n Watch out: the processors values must be 2, 3 or 4.")
    
    G = nx.Graph()

    if num_procs == 2:
        G.add_node('P1', weight=10)
        G.add_node('P2', weight=8)
        G.add_edge('P1', 'P1', weight=1)  # autociclo
        G.add_edge('P2', 'P2', weight=1)  # autociclo
        G.add_edge('P1', 'P2', weight=3)
    
    if num_procs == 3:
        G.add_node('P1', weight=10)
        G.add_node('P2', weight=8)
        G.add_node('P3', weight=6)
        G.add_edge('P1', 'P1', weight=1)
        G.add_edge('P2', 'P2', weight=1)
        G.add_edge('P3', 'P3', weight=1)
        G.add_edge('P1', 'P2', weight=3)
        G.add_edge('P2', 'P3', weight=5)
        G.add_edge('P1', 'P3', weight=7)
    
    if num_procs == 4:
        G.add_node('P1', weight=12)
        G.add_node('P2', weight=10)
        G.add_node('P3', weight=8)
        G.add_node('P4', weight=6)
        G.add_edge('P1', 'P1', weight=1)
        G.add_edge('P2', 'P2', weight=1)
        G.add_edge('P3', 'P3', weight=1)
        G.add_edge('P4', 'P4', weight=1)
        G.add_edge('P1', 'P2', weight=2)
        G.add_edge('P2', 'P3', weight=4)
        G.add_edge('P3', 'P4', weight=3)
        G.add_edge('P4', 'P1', weight=5)
        G.add_edge('P1', 'P3', weight=8)
    
    return G
