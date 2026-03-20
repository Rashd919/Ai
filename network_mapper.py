import networkx as nx
import matplotlib.pyplot as plt
import io

def map_network(target):
    """
    رسم خريطة للشبكة باستخدام NetworkX و Matplotlib.
    يعيد كائن BytesIO يحتوي على الصورة بدلاً من حفظها في ملف لتجنب مشاكل الصلاحيات.
    """
    try:
        G = nx.Graph()
        G.add_node(target)
        for i in range(1, 5):
            sub = f"{target}-node{i}"
            G.add_node(sub)
            G.add_edge(target, sub)

        plt.figure(figsize=(8, 6))
        nx.draw(G, with_labels=True, node_color="lightgreen", node_size=1500, font_size=10, font_weight='bold')
        
        # استخدام BytesIO لحفظ الصورة في الذاكرة
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close()
        buf.seek(0)
        
        return buf
    except Exception as e:
        return f"❌ خطأ في رسم الشبكة: {str(e)}"
