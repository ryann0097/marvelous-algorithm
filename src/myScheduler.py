import networkx as nx
import pathlib

# SAGA Library imports
from saga.schedulers.data.listvscluster import xml_to_digraph

def makespan_simulator(task_graph: nx.DiGraph, matching, execution_time, num_procs = 2):

    def min_processor(processors):
        return processors.index(min(processors))
    
    def min_2_processors(processors):
        sorted_procs = sorted((t, i) for i, t in enumerate(processors))
        return sorted_procs[0][1], sorted_procs[1][1]
    
    global_time = 0
    processors = [0] * num_procs
    processed = set()
    queue = []

    start = {}
    end = {}
    alloc = {}

    pendent_tasks = set()
    for node in task_graph.nodes:
        if task_graph.in_degree(node) == 0: # In this excerpt, we're looking for initial nodes (independent nodes)
            pendent_tasks.add(node)

    while len(processed) < len(task_graph.nodes):
        queue.sort()
        while queue and queue[0][0] <= global_time:
            end_task, task, p = queue.pop(0)
            processed.add(task)
            processors[p] = end_task

            for successor in task_graph.successors(task):
                if all(predecessors in processed for predecessors in task_graph.predecessors(successor)):
                    pendent_tasks.add(successor)

        tasks_to_execute = list(pendent_tasks)
        used_tasks = set()

        for u,v in matching:
            if u in tasks_to_execute and v in tasks_to_execute:
                p1, p2 = min_2_processors(processors)
                start[u] = global_time
                start[v] = global_time
                end[u] = global_time + execution_time[u]
                end[v] = global_time + execution_time[v]
                alloc[u] = p1
                alloc[v] = p2
                queue.append((end[u], u, p1))
                queue.append((end[v], v, p2))
                used_tasks.update({u,v})

        for tasks in pendent_tasks:
            if tasks in used_tasks:
                continue
            p = min_processor(processors)
            start[tasks] = global_time
            end[tasks] = global_time + execution_time[tasks]
            alloc[tasks] = p
            queue.append((end[tasks], tasks, p))
            used_tasks.add(tasks)
        
        pendent_tasks -= used_tasks

        if queue:
            global_time = min(evt[0] for evt in queue)
        else:
            break

    makespan = max(end.values())
    return makespan

def deciclify(cyclic_graph: nx.DiGraph, start_node):
        try:
            nx.find_cycle(cyclic_graph)
        except nx.NetworkXNoCycle:
            return cyclic_graph
    
        acyclic_graph = cyclic_graph.copy()
        colors = {v: 'WHITE' for v in cyclic_graph.nodes} # White nodes are the not visited nodes.
        
        def colorful_dfs(u):
            colors[u] = 'GRAY' # Gray nodes are the nodes that are being visited.
            
            for v in cyclic_graph.successors(u):
                if colors[v] == 'WHITE':
                    colorful_dfs(v)
                elif colors[v] == 'GRAY':
                    acyclic_graph.remove_edge(u,v)
            
            colors[u] = 'BLACK' # Black nodes are the nodes that were visited.
        
        colorful_dfs(start_node) 

        for (u, v) in list(cyclic_graph.edges):
            if colors[u] == 'WHITE' and colors[v] == 'BLACK':
                acyclic_graph.remove_edge(u, v)

        for v in cyclic_graph.nodes:
            if colors[u] == 'WHITE':
                colorful_dfs(v)

        return acyclic_graph

def matching_maker(acyclic_graph: nx.DiGraph):
        cc_graph = nx.Graph()
        tasks = list(acyclic_graph.nodes())

        for i in range(len(tasks)):
            for j in range(i+1, len(tasks)):
                u,v = tasks[i], tasks[j]
                if not nx.has_path(acyclic_graph, u, v) and not nx.has_path(acyclic_graph, v ,u):
                    cc_graph.add_edge(u,v)

        matching = nx.max_weight_matching(cc_graph, maxcardinality=True)        
        return matching    

def execute_graph(task_graph: nx.DiGraph):
    task_graph = deciclify(task_graph, list(task_graph.nodes)[0])
    topo_order = list(nx.topological_sort(task_graph))
    m = matching_maker(task_graph)
    execution_time = {
        node: task_graph.nodes[node].get("weight", 1)  # usa 1 se não houver peso definido
        for node in task_graph.nodes
    }

    return makespan_simulator(task_graph, m, execution_time, 2)
    # Preparando para a parte do cálculo do makespan:

def max_parallelism(task_graph: nx.DiGraph):
    levels = {}
    for node in nx.topological_sort(task_graph):
        if task_graph.in_degree(node) == 0:
            levels[node] = 0
        else:
            levels[node] = 1 + max(levels[pred] for pred in task_graph.predecessors(node))
    
    # Conta quantos nós estão em cada "nível"
    level_counts = {}
    for lvl in levels.values():
        level_counts[lvl] = level_counts.get(lvl, 0) + 1
    
    return max(level_counts.values())

def makespan_simulator_no_matching(graph, num_processors):
    time = 0  # current time
    completed_tasks = set()
    running_tasks = dict()  # task -> finish time

    while len(completed_tasks) < graph.number_of_nodes():
        # Remove tasks that have finished by current time
        for task, finish_time in list(running_tasks.items()):
            if finish_time <= time:
                completed_tasks.add(task)
                del running_tasks[task]

        # Identify ready tasks (all predecessors completed)
        ready_tasks = [
            node for node in graph.nodes()
            if node not in completed_tasks
            and node not in running_tasks
            and all(pred in completed_tasks for pred in graph.predecessors(node))
        ]

        # Assign processors up to available slots
        free_slots = num_processors - len(running_tasks)
        tasks_to_start = ready_tasks[:free_slots]

        # Start execution of assigned tasks
        for task in tasks_to_start:
            duration = graph.nodes[task].get("weight", 1)  # default duration = 1
            running_tasks[task] = time + duration

        # Advance time to the next finishing task
        if running_tasks:
            time = min(running_tasks.values())
        else:
            break

    makespan = time
    return makespan

