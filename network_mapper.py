import matplotlib.pyplot as plt
import networkx as nx
import io

def map_network(target, subdomains=None):
    """
    رسم خريطة شبكة حقيقية للعلاقات بين الدومين والنطاقات الفرعية المكتشفة.
    """
    if not subdomains:
        return "⚠️ لا توجد نطاقات فرعية لرسم الخريطة. يرجى إجراء تحليل الدومين أولاً."

    try:
        G = nx.Graph()
        G.add_node(target, color='red', size=1000)
        
        # إضافة النطاقات الفرعية كعقد مرتبطة بالدومين الأساسي
        if isinstance(subdomains, dict):
            for sub, ip in subdomains.items():
                G.add_node(sub, color='green', size=500)
                G.add_edge(target, sub)
                if ip and ip != "N/A":
                    G.add_node(ip, color='blue', size=300)
                    G.add_edge(sub, ip)
        elif isinstance(subdomains, list):
            for sub in subdomains:
                G.add_node(sub, color='green', size=500)
                G.add_edge(target, sub)

        # إعدادات الرسم
        plt.figure(figsize=(12, 8), facecolor='black')
        pos = nx.spring_layout(G)
        
        # رسم العقد
        colors = [G.nodes[node].get('color', 'gray') for node in G.nodes()]
        sizes = [G.nodes[node].get('size', 300) for node in G.nodes()]
        
        nx.draw(G, pos, with_labels=True, node_color=colors, node_size=sizes, 
                font_color='white', font_size=8, edge_color='gray', width=0.5)
        
        plt.title(f"Network Map for {target}", color='green', fontsize=15)
        
        # حفظ الرسم في الذاكرة
        buf = io.BytesIO()
        plt.savefig(buf, format='png', facecolor='black')
        buf.seek(0)
        plt.close()
        return buf
    except Exception as e:
        return f"⚠️ خطأ أثناء رسم الشبكة: {str(e)}"
