import plotly.graph_objects as go
import networkx as nx

def plot_adjacency_graph(adj_dict, color_result=None, search_query=""):
    """
    Vẽ đồ thị mạng lưới tỉnh thành phong cách Dark Mode High-Tech.
    """
    G = nx.Graph()
    for node, neighbors in adj_dict.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)

    # Tọa độ xấp xỉ địa lý để tạo dáng hình chữ S 
    pos_fixed = {
        "Hà Giang": [105, 25], "Lào Cai": [103.5, 24.5], "Cao Bằng": [106.5, 24.5],
        "Hà Nội": [105.8, 21.5], "Hải Phòng": [107, 21], "Thanh Hóa": [105.5, 19.5],
        "Đà Nẵng": [108.5, 14], "Khánh Hòa": [109.5, 9.5], "Đắk Lắk": [108.5, 10.5],
        "TP. Hồ Chí Minh": [106.5, 6.5], "Tây Ninh": [105.5, 7.5], "Cà Mau": [105, 4]
    }
    
    # Tăng tham số k để các nốt tự giãn cách đẹp hơn
    pos = nx.spring_layout(G, pos=pos_fixed, fixed=[n for n in pos_fixed if n in G], seed=42, k=0.3)

    # 1. Vẽ các đường nối (Cạnh) - Sử dụng màu xanh Neon mờ
    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1.2, color='rgba(0, 0, 0, 0.15)'), # Tăng độ dày và làm đen hơn một chút
        hoverinfo='none', mode='lines')

    # 2. Vẽ các nốt (Tỉnh thành)
    node_x, node_y, node_text, node_color, node_size, node_line_width, node_line_color = [], [], [], [], [], [], []
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)
        
        # Màu sắc: Nếu chưa tô màu thì dùng màu xám đen của Dark Mode
        color = color_result.get(node, "#2C3E50") if color_result else "#2C3E50"
        node_color.append(color)
        
        # Logic làm nổi bật khi tìm kiếm
        if search_query and search_query.lower() in node.lower():
            node_size.append(25)
            node_line_width.append(3)
            node_line_color.append("#00D2FF") # Viền xanh sáng khi tìm thấy
        else:
            node_size.append(10)
            node_line_width.append(1)
            node_line_color.append("rgba(255,255,255,0.3)")

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text' if search_query else 'markers',
        text=node_text,
        textposition="top center",
        hoverinfo='text',
        marker=dict(
            showscale=False,
            color=node_color,
            size=node_size,
        # Thêm viền đen mờ để tách biệt các nốt với nền trắng
        line=dict(width=1.5, color='rgba(0, 0, 0, 0.4)'), 
        opacity=1.0 # Đảm bảo nốt không bị trong suốt
        ))

    # 3. Cấu hình khung nhìn (Layout) 
    fig = go.Figure(data=[edge_trace, node_trace],
                 layout=go.Layout(
                    showlegend=False,
                    margin=dict(b=0, l=0, r=0, t=40),
                    height=850, 
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    
                    # Chỉnh về màu trắng để khớp với khung mới
                    plot_bgcolor='#FFFFFF',
                    paper_bgcolor='#FFFFFF',
                    
                    # Chỉnh chữ nhãn tỉnh sang màu tối (ví dụ màu đen xám)
                    font=dict(color="#2D3436") 
                ))
    
    # Chỉnh lại màu đường nối (cạnh) sang màu xám để nổi bật trên nền trắng
    edge_trace.line.color = 'rgba(0, 0, 0, 0.1)'

    return fig