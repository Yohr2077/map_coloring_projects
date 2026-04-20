import json
import os

def load_raw_data(file_path):
    """
    Đọc dữ liệu thô từ file JSON.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file dữ liệu tại {file_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Lỗi: Định dạng JSON không hợp lệ tại {file_path}")
        return {}

def save_processed_data(data, file_path):
    """
    Lưu dữ liệu đã xử lý ra file JSON để các thành viên khác sử dụng.
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Đã lưu dữ liệu thành công vào: {file_path}")
    except Exception as e:
        print(f"Lỗi khi lưu dữ liệu: {e}")

def get_adjacency_graph():
    """
    Hàm chủ chốt: Trả về Dictionary đồ thị kề.
    Ưu tiên đọc từ dữ liệu đã xử lý, nếu chưa có sẽ đọc từ dữ liệu thô.
    """
    raw_path = 'data/raw/vietnam_provinces.json'
    processed_path = 'data/processed/adjacency_matrix.json'
    
    if os.path.exists(processed_path):
        return load_raw_data(processed_path)
    elif os.path.exists(raw_path):
        # Nếu chưa có file processed, xử lý từ file raw và lưu lại
        data = load_raw_data(raw_path)
        save_processed_data(data, processed_path)
        return data
    else:
        print(f"Lỗi: Không tìm thấy file dữ liệu tại {raw_path} hoặc {processed_path}")
        return {}

if __name__ == "__main__":
    # Phần dành cho Thành viên 1 kiểm tra code của chính mình
    print("--- Vietnam Map Coloring: Kiểm tra Data Processing (Member 1) ---")
    graph = get_adjacency_graph()
    num_provinces = len(graph)
    print(f"Tổng số tỉnh thành đã tải: {num_provinces}")
    
    if num_provinces > 0:
        print("Ví dụ danh sách kề của một số tỉnh:")
        for province in list(graph.keys())[:3]:
            print(f"  - {province}: {graph[province]}")