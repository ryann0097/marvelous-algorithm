import networkx as nx
import csv
from saga.schedulers import heft, cpop, minmin, maxmin
import marvelous_scheduler as ms
import graph_utils as gu
import processors as proc


schedulers = [
    ("HEFT", heft.HeftScheduler),
    ("CPOP", cpop.CpopScheduler),
    ("MinMin", minmin.MinMinScheduler),
    ("MaxMin", maxmin.MaxMinScheduler)
]

# Define the path to your data directory here:
DATA_DIR = "/home/ryann0097/saga/src/data"

# Path to graph data
graphs = gu.load_graph_data(DATA_DIR)

print("\n======================= Loaded Graphs =======================\n")

for i, graph in enumerate(graphs):
    name = graph.graph.get("name", f"Graph_{i}")
    print(f"[{i}] {name} | Nodes: {graph.number_of_nodes()} | Edges: {graph.number_of_edges()}")

print("\n=============================================================\n")

# Have to test something now.
# Now, we're gonna to see how the graphs are gonna be seen.


results = []

for graph in graphs:
    network = proc.generate_processors(3)
    
    row = {
        "GraphName": graph.graph.get("name", "Unknown"),
        "Nodes": graph.number_of_nodes(),
        "Edges": graph.number_of_edges()
    }

    heft_scheduler = heft.HeftScheduler()
    heft_schedule = heft_scheduler.schedule(network, graph)
    heft_makespan = max(task.end for tasks in heft_schedule.values() for task in tasks)
    row["HEFT_Makespan"] = heft_makespan

    cpop_scheduler = cpop.CpopScheduler()
    cpop_schedule = cpop_scheduler.schedule(network, graph)
    cpop_makespan = max(task.end for tasks in cpop_schedule.values() for task in tasks)
    row["CPOP_Makespan"] = cpop_makespan

    minmin_scheduler = minmin.MinMinScheduler()
    minmin_schedule = minmin_scheduler.schedule(network, graph)
    minmin_makespan = max(task.end for tasks in minmin_schedule.values() for task in tasks)
    row["MinMin_Makespan"] = minmin_makespan

    maxmin_scheduler = maxmin.MaxMinScheduler()
    maxmin_schedule = maxmin_scheduler.schedule(network, graph)
    maxmin_makespan = max(task.end for tasks in maxmin_schedule.values() for task in tasks)
    row["MaxMin_Makespan"] = maxmin_makespan

    marvelous_scheduler = ms.MarvelousScheduler()
    marvelous_schedule = marvelous_scheduler.schedule(network, graph)
    marvelous_makespan = max(task.end for tasks in marvelous_schedule.values() for task in tasks)
    row["Marvelous_Makespan"] = marvelous_makespan

    results.append(row)


# Agora salvar no CSV
with open("./results/scheduler_results.csv", "w", newline="") as csvfile:
    fieldnames = ["GraphName", "Nodes", "Edges", "HEFT_Makespan", "CPOP_Makespan", "MinMin_Makespan", "MaxMin_Makespan", "Marvelous_Makespan"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)

print("CSV salvo como 'scheduler_results.csv'")
