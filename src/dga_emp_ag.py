import networkx as nx # Para modelar os grafos
import pathlib # Para caminhos
import myScheduler as ms
import csv

# SAGA imports
from saga.schedulers.data.listvscluster import xml_to_digraph

# Graphs initializer

GRAPH_DIR = "/home/ryann0097/saga/data" # Insert the graph directory here
graphs_path = pathlib.Path(GRAPH_DIR) # Load the graphs .gxl files (.gxl is way similar to .xml files)

graphs_list = []
for file in graphs_path.glob("*.gxl"):
    graph = xml_to_digraph(file.read_text())
    graph.name = file.stem
    graphs_list.append(graph)

graphs_parallelism = []

for i, graph in enumerate(graphs_list):
    graphs_parallelism.append(ms.max_parallelism(graph))

print("======================= Grafos carregados =======================")
for i, graph in enumerate(graphs_list):
    name = graph.graph.get("name", f"Grafo_{i}")
    print(f"[{i}] {name} | Nós: {graph.number_of_nodes()} | Arestas: {graph.number_of_edges()}")

print("\n\n ================================================================ \n\n")
graphs_and_makespans = dict()

def naming_graphs(graph: nx.DiGraph, dict):
    dict[(graph.name, graph.number_of_edges(), graph.number_of_nodes())] = 0

for graph in graphs_list:
    naming_graphs(graph, graphs_and_makespans)

for graph in graphs_list:
    key = (graph.name, graph.number_of_edges(), graph.number_of_nodes())
    makespan = ms.execute_graph(graph)
    graphs_and_makespans[key] = makespan

with open("resultados_scheduler.csv", mode="w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Index", "Nome", "Nós", "Arestas", "Makespan", "Paralelismo Máx"])
    
    for i, graph in enumerate(graphs_list):
        name = graph.name
        nodes = graph.number_of_nodes()
        edges = graph.number_of_edges()
        key = (name, edges, nodes)
        makespan = graphs_and_makespans[key]
        parallelism = graphs_parallelism[i]
        writer.writerow([i, name, nodes, edges, makespan, parallelism])

print("\n✅ Resultados salvos em 'resultados_scheduler.csv'")