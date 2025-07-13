import networkx as nx

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
