# attack_surface.py
# رسم خريطة سطح الهجوم للدومينات الفرعية

import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(domain, subdomains):
    """إنشاء خريطة بصريّة لسطح الهجوم"""
    G = nx.Graph()
    G.add_node(domain)
    for sub, ip in subdomains.items():
        G.add_edge(domain, sub)
    plt.figure(figsize=(8,6))
    nx.draw_circular(G, with_labels=True, node_color="#FF0000", node_size=1000, font_size=10)
    path = f"/tmp/{domain}_map.png"
    plt.savefig(path)
    plt.close()
    return path
