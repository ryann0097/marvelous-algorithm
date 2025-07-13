import networkx as nx
import csv
from saga.schedulers import heft, cpop, minmin, maxmin
import simulation as smt
import graph_utils as gu

schedulers = [
    ("HEFT", heft.HeftScheduler),
    ("CPOP", cpop.CpopScheduler),
    ("MinMin", minmin.MinMinScheduler),
    ("MaxMin", maxmin.MaxMinScheduler)
]

# Define the path to your data directory here:
DATA_DIR = "/home/ryann0097/saga/data"

# Path to graph data
graphs = gu.load_graph_data(DATA_DIR)

print("\n======================= Loaded Graphs =======================\n")

for i, graph in enumerate(graphs):
    name = graph.graph.get("name", f"Graph_{i}")
    print(f"[{i}] {name} | Nodes: {graph.number_of_nodes()} | Edges: {graph.number_of_edges()}")

print("\n=============================================================\n")

# Have to test something now.
# Now, we're gonna to see how the graphs are gonna be seen.

""" results = []

for i, graph in enumerate(graphs):
    row = {
        "GraphName": graph.graph.get("name", f"Graph_{i}"),
        "Nodes": graph.number_of_nodes(),
        "Edges": graph.number_of_edges()
    }

    for sched_name, scheduler_class in schedulers:
        scheduler = scheduler_class()
        scheduler.schedule(graph)
        runtime = scheduler.get_runtimes()
        row[f"{sched_name}_Makespan"] = runtime
    
    marvelous_runtime = smt.execute_graph(graph)
    row["Marvelous_Makespan"] = marvelous_runtime

    results.append(row)

with open("scheduler_results.csv", "w", newline="") as csvfile:
    fieldnames = ["GraphName", "Nodes", "Edges"] + [f"{name}_Makespan" for name, _ in schedulers] + ["Marvelous_Makespan"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)

print("CSV salvo como 'scheduler_results.csv'") """


results = []

for graph in graphs:
    row = {
        "GraphName": graph.graph.get("name", "Unknown"),
        "Nodes": graph.number_of_nodes(),
        "Edges": graph.number_of_edges()
    }
    
    # HEFT
    heft_scheduler = heft.HeftScheduler()
    heft_scheduler.schedule(graph)  # Ajuste para o método correto!
    heft_runtime = heft_scheduler.get_runtimes()
    row["HEFT_Makespan"] = heft_runtime
    
    # CPOP
    cpop_scheduler = cpop.CpopScheduler()
    cpop_scheduler.schedule(graph)
    cpop_runtime = cpop_scheduler.get_runtimes()
    row["CPOP_Makespan"] = cpop_runtime
    
    # MinMin
    minmin_scheduler = minmin.MinMinScheduler()
    minmin_scheduler.schedule(graph)
    minmin_runtime = minmin_scheduler.get_runtimes()
    row["MinMin_Makespan"] = minmin_runtime
    
    # MaxMin
    maxmin_scheduler = maxmin.MaxMinScheduler()
    maxmin_scheduler.schedule(graph)
    maxmin_runtime = maxmin_scheduler.get_runtimes()
    row["MaxMin_Makespan"] = maxmin_runtime
    
    # Marvelous (simulation)
    marvelous_runtime = smt.execute_graph(graph)
    row["Marvelous_Makespan"] = marvelous_runtime
    
    results.append(row)

# Agora salvar no CSV
with open("scheduler_results.csv", "w", newline="") as csvfile:
    fieldnames = ["GraphName", "Nodes", "Edges", "HEFT_Makespan", "CPOP_Makespan", "MinMin_Makespan", "MaxMin_Makespan", "Marvelous_Makespan"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)

print("CSV salvo como 'scheduler_results.csv'")
