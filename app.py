import streamlit as st
import time
from src.data_processing import get_adjacency_graph
from src.csp_core import solve_csp
from src.visualization import plot_adjacency_graph

# 1. Cấu hình trang
st.set_page_config(page_title="Tô màu Bản đồ - Việt Nam", layout="wide", page_icon="🇻🇳")

# 2. CSS TÙY CHỈNH: GIAO DIỆN TỐI (DARK MODE)
st.markdown("""
    <style>
    /* Nền trang */
    .stApp { background-color: #0E1117; }
    .main { background-color: #0E1117; color: #FAFAFA; }
    
    /* Các khối Card màu đen */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #1A1C24 !important;
        border: 1px solid #30333D !important;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }

    /* RIÊNG BIỆT: Khung trực quan hóa đồ thị màu trắng (Theo yêu cầu trước của bạn) */
    [data-testid="column"]:nth-child(1) [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E9ECEF !important;
    }
    [data-testid="column"]:nth-child(1) h3, [data-testid="column"]:nth-child(1) span {
        color: #2D3436 !important;
    }

    /* FIX SELECTBOX & INPUT SANG MÀU ĐEN */
    /* Ô nhập liệu và ô chọn chính */
    div[data-baseweb="select"] > div, 
    div[data-baseweb="input"] > div,
    input {
        background-color: #262730 !important;
        color: white !important;
        border: 1px solid #4B4D58 !important;
    }

    /* MENU SỔ XUỐNG (Dropdown Menu) */
    div[data-baseweb="popover"] > div,
    div[data-baseweb="menu"] {
        background-color: #1A1C24 !important;
        border: 1px solid #4B4D58 !important;
    }

    /* Các mục bên trong danh sách sổ xuống */
    div[data-baseweb="menu"] li {
        color: white !important;
        background-color: transparent !important;
    }
    
    /* Khi di chuột qua các mục trong danh sách */
    div[data-baseweb="menu"] li:hover {
        background-color: #3a7bd5 !important;
        color: white !important;
    }

    /* Chữ tiêu đề và nhãn (Trừ cột 1 màu trắng đã chỉnh ở trên) */
    [data-testid="column"]:nth-child(2) h3, 
    [data-testid="column"]:nth-child(2) span,
    label { color: #FAFAFA !important; }

    /* Nút bấm Neon Blue */
    div.stButton > button {
        background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%);
        color: white; border-radius: 10px; border: none;
        height: 50px; font-weight: bold; width: 100%; transition: 0.3s;
    }
    div.stButton > button:hover {
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.5);
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Tiêu đề chính
st.markdown("# Giải toán Tô màu Bản đồ Việt Nam ")

# 4. THANH ĐIỀU KHIỂN
with st.container(border=True):
    c1, c2, c3, c4, c5 = st.columns([1.5, 1.2, 1.2, 2, 1])
    with c1:
        algo_choice = st.selectbox("Thuật toán AI", ["Giải thuật AC-3", "Forward Checking", "Backtracking cơ bản"])
    with c2:
        num_colors = st.select_slider("Số màu tối đa (k)", options=[3, 4, 5, 6], value=4)
    with c3:
        speed_opt = st.selectbox("Tốc độ mô phỏng", ["Nhanh", "Trung bình", "Chậm"])
    with c4:
        search_query = st.text_input("Tìm kiếm tỉnh thành", placeholder="Nhập tên tỉnh (VD: Hà Nội, Cần Thơ...)")
    with c5:
        st.write("") 
        st.write("")
        run_btn = st.button("▶ CHẠY ")

# 5. Khởi tạo dữ liệu
graph_data = get_adjacency_graph()
palette = ["#FF5733", "#2ECC71", "#3498DB", "#F1C40F", "#9B59B6", "#1ABC9C"]
colors = palette[:num_colors]

# 6. KHU VỰC HIỂN THỊ CHÍNH
col_map, col_status = st.columns([2.5, 1])

with col_map:
    with st.container(border=True):
        st.subheader("Trực quan hóa Đồ thị")
        if run_btn:
            with st.spinner("Đang tính toán..."):
                start_time = time.time()
                result = solve_csp(graph_data, colors)
                end_time = time.time()
                if result:
                    fig = plot_adjacency_graph(graph_data, result, search_query=search_query)
                    st.plotly_chart(fig, use_container_width=True, height=800)
                else:
                    st.error("Không tìm thấy lời giải!")
        else:
            fig = plot_adjacency_graph(graph_data, search_query=search_query)
            st.plotly_chart(fig, use_container_width=True, height=800)

with col_status:
    with st.container(border=True):
        st.subheader("Chú thích màu")
        sc1, sc2 = st.columns(2)
        for i in range(num_colors):
            target_col = sc1 if i % 2 == 0 else sc2
            target_col.markdown(f'''
                <div style="display:flex; align-items:center; margin-bottom:12px;">
                    <div style="background-color:{colors[i]}; width:20px; height:20px; border-radius:5px; margin-right:10px; border:1px solid #444;"></div>
                    <span style="font-size:14px; color:white;">Màu {i+1}</span>
                </div>
            ''', unsafe_allow_html=True)

    st.write("")
    with st.container(border=True):
        st.subheader("Chi tiết tìm kiếm")
        if search_query:
            found = [p for p in graph_data.keys() if search_query.lower() in p.lower()]
            if found:
                target = found[0]
                st.success(f"Đã xác định: {target}")
                st.write(f"Giáp ranh: {', '.join(graph_data[target])}")
            else: st.warning("Không tìm thấy tỉnh.")
        else: st.info("Nhập tên tỉnh để xem ràng buộc.")

    st.write("")
    with st.container(border=True):
        st.subheader("Thông số hệ thống")
        if run_btn and 'result' in locals() and result:
            st.markdown(f"""
                <div style="margin-bottom: 15px;">
                    <p style="margin:0; font-size:14px; color: #BBB;">Thời gian thực thi</p>
                    <p style="margin:0; font-size:24px; font-weight: bold; color: #00d2ff;">{end_time - start_time:.4f} giây</p>
                </div>
                <div style="margin-bottom: 15px;">
                    <p style="margin:0; font-size:14px; color: #BBB;">Tổng số biến (Tỉnh)</p>
                    <p style="margin:0; font-size:24px; font-weight: bold; color: #00d2ff;">{len(graph_data)}</p>
                </div>
            """, unsafe_allow_html=True)
            st.success("Đã tìm thấy lời giải")