import networkx as nx
import pathlib
import myScheduler as ms
import csv

# SAGA imports
from saga.schedulers.data.listvscluster import xml_to_digraph

# Load graphs
GRAPH_DIR = "/home/ryann0097/saga/amostragem"
graphs_path = pathlib.Path(GRAPH_DIR)

graphs_list = []
for file in graphs_path.glob("*.gxl"):
    graph = xml_to_digraph(file.read_text())
    graph.name = file.stem
    graphs_list.append(graph)

graphs_parallelism = [ms.max_parallelism(g) for g in graphs_list]

print("======================= Grafos carregados =======================")
for i, graph in enumerate(graphs_list):
    print(f"[{i}] {graph.name} | Nós: {graph.number_of_nodes()} | Arestas: {graph.number_of_edges()}")

print("\n\n ================================================================ \n\n")

# Usando makespan sem emparelhamento
graphs_and_makespans_no_matching = {}

for graph in graphs_list:
    makespan = ms.makespan_simulator_no_matching(graph, num_processors=2)
    key = (graph.name, graph.number_of_edges(), graph.number_of_nodes())
    graphs_and_makespans_no_matching[key] = makespan

with open("resultados_scheduler_no_matching.csv", mode="w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Index", "Nome", "Nós", "Arestas", "Makespan No Matching", "Paralelismo Máx"])

    for i, graph in enumerate(graphs_list):
        name = graph.name
        nodes = graph.number_of_nodes()
        edges = graph.number_of_edges()
        key = (name, edges, nodes)
        makespan = graphs_and_makespans_no_matching[key]
        parallelism = graphs_parallelism[i]
        writer.writerow([i, name, nodes, edges, makespan, parallelism])

print("\n✅ Resultados sem emparelhamento salvos em 'resultados_scheduler_no_matching.csv'")
