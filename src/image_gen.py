import os
import networkx as nx
import matplotlib.pyplot as plt

import graph_utils as gu
import marvelous_algorithm as ma

"""
This script processes a set of graphs by applying the following operations to each one:
1. Visualizes and saves the original graph structure.
2. Applies a decyclification algorithm to convert it into a DAG (Directed Acyclic Graph).
3. Constructs the co-comparability graph from the DAG by identifying pairs of nodes that are not reachable from each other.
4. Computes a maximum matching from the co-comparability graph.
5. Saves visual representations of each stage (original, decyclified, co-comparability, and matching) into subdirectories under the 'image' folder.

Steps:
- Loads graphs from a specified data directory (`DATA_DIR`) using a custom utility (`graph_utils.load_graph_data`).
- Each graph is stored in its own subfolder under the `IMAGE_DIR` path.
- Uses `matplotlib` and `networkx` for visualization and graph processing.
- Calls a custom `deciclify()` function from `marvelous_algorithm` to remove cycles from graphs.
- Computes co-comparability graphs by connecting node pairs that have no path between them in either direction.
- Computes maximum matchings on the co-comparability graphs using NetworkX's `max_weight_matching()`.

Generated files:
- `original.png`: Original input graph.
- `deciclified.png`: DAG after removing cycles.
- `cocomparability.png`: Co-comparability graph.
- `matching.png`: Matching from the co-comparability graph.

Required modules:
- os
- pathlib
- networkx
- matplotlib.pyplot
- graph_utils (custom)
- marvelous_algorithm (custom)
- saga.utils.draw (optional, not used unless enabled)

Ensure the `DATA_DIR` path points to a valid folder containing input graphs.
"""

DATA_DIR = "/home/ryann0097/saga/src/data"
IMAGE_DIR = "./image"

graphs = gu.load_graph_data(DATA_DIR)

acyclic_graphs = []
cc_graphs = []
matchings = []

for i, graph in enumerate(graphs):
    name = graph.graph.get("name", f"Graph_{i}")
    subdir = os.path.join(IMAGE_DIR, name)
    os.makedirs(subdir, exist_ok=True)

    # ORIGINAL GRAPH
    plt.figure(figsize=(8,6))
    nx.draw(graph, with_labels=True, node_color="skyblue", edge_color="gray")
    plt.title(f"Original - {name}")
    plt.savefig(os.path.join(subdir, "original.png"))
    plt.close()

    # DIRECTED ACYCLIC GRAPH
    dag = ma.deciclify(graph, list(graph.nodes)[0])
    acyclic_graphs.append(dag)

    plt.figure(figsize=(8,6))
    nx.draw(dag, with_labels=True, node_color="lightgreen", edge_color="black")
    plt.title(f"Deciclified - {name}")
    plt.savefig(os.path.join(subdir, "deciclified.png"))
    plt.close()

    # CO-COMPARABILITY GRAPH
    cc_graph = nx.Graph()
    nodes = list(dag.nodes())
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            u, v = nodes[i], nodes[j]
            if not nx.has_path(dag, u, v) and not nx.has_path(dag, v, u):
                cc_graph.add_edge(u, v)
    cc_graphs.append(cc_graph)

    plt.figure(figsize=(8,6))
    nx.draw(cc_graph, with_labels=True, node_color="orange", edge_color="purple")
    plt.title(f"Co-comparability - {name}")
    plt.savefig(os.path.join(subdir, "cocomparability.png"))
    plt.close()

    # MATCHING RESULT
    matching = nx.max_weight_matching(cc_graph, maxcardinality=True)
    match_graph = nx.Graph()
    match_graph.add_edges_from(matching)
    matchings.append(matching)

    plt.figure(figsize=(8,6))
    nx.draw(match_graph, with_labels=True, node_color="pink", edge_color="red")
    plt.title(f"Matching - {name}")
    plt.savefig(os.path.join(subdir, "matching.png"))
    plt.close()
