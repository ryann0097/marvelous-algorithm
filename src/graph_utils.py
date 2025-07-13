import networkx as nx
import pathlib 

from saga.schedulers.data.listvscluster import xml_to_digraph

# Loading functions
def load_graph_data(path_to_data):
    data_path = pathlib.Path(path_to_data)
    graphs = []

    for file in data_path.glob("*.gxl"):
        graph = xml_to_digraph(file.read_text())
        graph.name = file.stem
        graphs.append(graph)

    return graphs


# Maybe photos?
