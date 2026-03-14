import networkx as nx
import matplotlib.pyplot as plt
import tempfile

def draw_graph(domain, subdomains):
    """
    رسم خريطة الهجوم (Attack Surface) باستخدام NetworkX
    """
    G = nx.Graph()
    G.add_node(domain)

    for sd, ip in subdomains.items():
        G.add_node(sd)
        G.add_edge(domain, sd)

    plt.figure(figsize=(8,6))
    nx.draw_circular(
        G, 
        with_labels=True, 
        node_color="#FF0000", 
        node_size=1200, 
        font_size=10,
        font_color="white",
        edge_color="#00FF00"
    )

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    plt.savefig(temp_file.name, bbox_inches='tight')
    plt.close()
    return temp_file.name
