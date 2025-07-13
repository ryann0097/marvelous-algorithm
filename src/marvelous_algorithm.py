import networkx as nx

"""

    Deciclify Complexity: O(V + E)
        - Cycle finding: O(V + E) (uses DFS internally)
        - Custom DFS (colorful_dfs): O(V + E)
        - Edges visiting: O(E)
        - Nodes visiting: O(V)

"""

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
            if colors[v] == 'WHITE':
                colorful_dfs(v)

        return acyclic_graph

"""

    Matching Ready Tasks: O(n² x (V + E) + n³)
        - First of all, we run by edges and nodes, resulting in n² pairs, so O(n²).
        - We take this to all the others operations, like the DFS to verify the paths from u to v, and from v to u.
        - Two calls by pair: O(n² x (V + E))
        - Matching implemented by networkx: O(n³)


"""

def matching_ready_tasks(task_graph: nx.DiGraph, ready_tasks: list[str]):
    """
    Recebe um subconjunto de tarefas disponíveis e retorna pares independentes
    para execução paralela.
    """
    cc_graph = nx.Graph()

    for i in range(len(ready_tasks)):
        for j in range(i + 1, len(ready_tasks)):
            u, v = ready_tasks[i], ready_tasks[j]
            if not nx.has_path(task_graph, u, v) and not nx.has_path(task_graph, v, u):
                cc_graph.add_edge(u, v)

    # matching = nx.max_weight_matching(cc_graph, maxcardinality=True)
    # return list(matching)

    matching = edmonds_matching(cc_graph)
    
    pairs = []
    used = set()
    for u in matching:
        v = matching[u]
        if u not in used and v not in used:
            pairs.append((u, v))
            used.add(u)
            used.add(v)
    return pairs

def edmonds_matching(G: nx.Graph):
    """
    Versão simplificada do algoritmo de Edmonds (sem contraction de blossoms).
    Funciona para grafos pequenos com pares independentes.
    """
    matching = {}
    for node in G.nodes():
        if node in matching:
            continue

        queue = [node]
        base = {v: v for v in G.nodes()}
        parent = {}
        used = {v: False for v in G.nodes()}
        used[node] = True
        blossom = {}

        found = False

        while queue and not found:
            v = queue.pop(0)
            for u in G.neighbors(v):
                if base[v] == base[u] or matching.get(v) == u:
                    continue
                if u in matching and not used[u]:
                    used[u] = True
                    parent[u] = v
                    queue.append(matching[u])
                    used[matching[u]] = True
                    parent[matching[u]] = u
                elif u not in parent:
                    path = []
                    curr_v, curr_u = v, u
                    while curr_v is not None:
                        path.append(curr_v)
                        curr_v = parent.get(curr_v)
                        if curr_v is not None and curr_v in matching:
                            path.append(matching[curr_v])
                            curr_v = parent.get(matching[curr_v])
                        else:
                            break

                    while curr_u is not None:
                        path.append(curr_u)
                        curr_u = parent.get(curr_u)
                        if curr_u is not None and curr_u in matching:
                            path.append(matching[curr_u])
                            curr_u = parent.get(matching[curr_u])
                        else:
                            break

                    for i in range(0, len(path) - 1, 2):
                        matching[path[i]] = path[i + 1]
                        matching[path[i + 1]] = path[i]

                    found = True
                    break
    return matching