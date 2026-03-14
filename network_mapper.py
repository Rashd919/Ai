import networkx as nx
import matplotlib.pyplot as plt

def map_network(target):
    """رسم خريطة الشبكة"""
    G = nx.Graph()
    G.add_node(target)
    for i in range(1,4):
        sub = f"{target}-node{i}"
        G.add_node(sub)
        G.add_edge(target, sub)
    file = f"{target}_network.png"
    plt.figure(figsize=(6,4))
    nx.draw(G, with_labels=True, node_color="lightgreen", node_size=1500, font_size=10)
    plt.savefig(file)
    plt.close()
    return file
