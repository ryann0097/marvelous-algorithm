import networkx as nx
import pathlib 

from saga.schedulers.data.listvscluster import xml_to_digraph

def load_graph_data(path_to_data):
    """
    Returns a list of networkx graph objects.

    Params:
    path_to_data: Directory path to graphs data.

    Return:
    list: The loaded graphs in a list.
    """
    data_path = pathlib.Path(path_to_data)
    graphs = []

    for file in data_path.glob("*.gxl"):
        graph = xml_to_digraph(file.read_text())
        graph.name = file.stem
        graphs.append(graph)

    return graphs
