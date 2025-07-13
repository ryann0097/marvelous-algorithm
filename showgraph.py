# testando pro grafo 1 de data

import networkx as nx
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

def read_gxl_as_directed(path):
    """
    Lê um arquivo .gxl e o trata SEMPRE como um grafo direcionado (DiGraph).
    """
    # FORÇADO: Sempre cria um grafo direcionado para mostrar as setas.
    G = nx.DiGraph()
    print("O grafo será tratado como DIRECIONADO.")
    
    try:
        tree = ET.parse(path)
    except ET.ParseError as e:
        print(f"Erro de XML: O arquivo GXL parece estar malformatado. Detalhes: {e}")
        return None, None
        
    root = tree.getroot()
    node_labels = {}

    # Itera sobre os nós e arestas
    for node in root.findall('.//node'):
        node_id = node.get('id')
        node_labels[node_id] = node_id
        G.add_node(node_id)

    for edge in root.findall('.//edge'):
        source = edge.get('from')
        target = edge.get('to')
        # Adiciona a aresta direcionada de 'source' para 'target'
        if G.has_node(source) and G.has_node(target):
            G.add_edge(source, target)

    return G, node_labels

# --- Bloco Principal de Execução ---

gxl_file = 'data\CyberShake_Nodes_50_CCR_1.0.gxl' 
G, node_labels = read_gxl_as_directed(gxl_file)

if G:
    print(f"Grafo '{gxl_file}' carregado com {G.number_of_nodes()} nós e {G.number_of_edges()} arestas.")
    
    # Aumentar o tamanho da figura para melhor visualização
    plt.figure(figsize=(15, 15))
    
    # O layout 'spring' ajuda a evitar sobreposição de nós
    pos = nx.spring_layout(G, k=0.8, iterations=50, seed=42)

    # --- DESENHANDO O GRAFO COM SETAS ---
    # NetworkX desenha setas automaticamente em objetos DiGraph.
    # Podemos customizar a aparência das setas.
    nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=700)
    
    nx.draw_networkx_edges(G, pos,
                           edge_color='gray',
                           width=1.5,
                           arrowstyle='->',  # Estilo da ponta da seta
                           arrowsize=20)    # Tamanho da ponta da seta
                           
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8, font_weight='bold')

    plt.title("Visualização do Grafo Direcionado (A -> B)", fontsize=16)
    plt.axis('off') # Remove os eixos X e Y
    
    # Salva a imagem
    output_filename = "grafo_com_setas.png"
    plt.savefig(output_filename, format="PNG", dpi=300, bbox_inches='tight') 
    print(f"\nImagem salva como '{output_filename}'")
    print("Verifique o arquivo para ver o grafo com as setas indicando o sentido das dependências.")

    plt.show()
else:
    print("A imagem não foi gerada porque o grafo está vazio ou não pôde ser carregado.")