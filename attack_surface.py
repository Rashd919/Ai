import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(domain, subs):
    """رسم شبكة النطاقات الفرعية والسطح الهجومي"""
    G = nx.Graph()
    G.add_node(domain)
    for sub, ip in subs.items():
        G.add_node(sub)
        G.add_edge(domain, sub)
    plt.figure(figsize=(10,6))
    nx.draw(G, with_labels=True, node_color='skyblue', node_size=2000, font_size=10, font_weight='bold')
    file = f"{domain}_attack_surface.png"
    plt.savefig(file)
    plt.close()
    return file
