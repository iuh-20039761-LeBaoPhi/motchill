import pandas as pd

# Giả sử dữ liệu của bạn đang được đọc từ file CSV
df = pd.read_csv(r"E:\pt\duanmoi\motchill.csv")

# 1. Loại bỏ các dòng trống
cleaned_data = df.dropna()

# 2. Chuẩn hóa cột "thoiluong"
def normalize_duration(duration):
    if isinstance(duration, str):  # Kiểm tra nếu là chuỗi
        # Loại bỏ các ký tự không hợp lệ (như 'g', '+', '/ tập')
        duration = duration.replace("g", "").replace("+", "").replace(" / tập", "").strip() 
        
        # Xử lý các chuỗi dạng "1 47" thành 1 phút 47 giây
        if " " in duration:
            parts = duration.split()
            try:
                if len(parts) == 2:  # Trường hợp có 2 phần, ví dụ "1 47"
                    return int(parts[0])  # Chỉ lấy phần phút
                else:
                    return None  # Trường hợp không đúng định dạng
            except ValueError:
                return None  # Nếu không thể chuyển đổi, trả về None
        # Loại bỏ "phút" và chuyển thành số nguyên
        try:
            return int(duration.replace("phút", "").replace("Phút", "").strip())
        except ValueError:
            return None  # Nếu không thể chuyển đổi, trả về None
    return None

cleaned_data["thoiluong"] = cleaned_data["thoiluong"].apply(normalize_duration)

# 3. Chuẩn hóa cột "theloai"
cleaned_data["theloai"] = cleaned_data["theloai"].apply(
    lambda x: ", ".join([genre.strip().capitalize() for genre in x.split(",")])
)

# 4. Chuẩn hóa cột "quocgia"
cleaned_data["quocgia"] = cleaned_data["quocgia"].str.strip().str.title()

# 5. Loại bỏ các dòng trùng lặp
cleaned_data = cleaned_data.drop_duplicates()

# 6. Chuẩn hóa các cột ký tự khác
columns_to_clean = ["tenphim", "daodien", "trangthai"]
for col in columns_to_clean:
    cleaned_data[col] = cleaned_data[col].str.strip()

# 7. Lưu dữ liệu đã làm sạch ra file mới
output_path = r"E:\pt\duanmoi\motchill-Airflow.csv"
cleaned_data.to_csv(output_path, index=False)

print(f"Dữ liệu đã được lưu tại: {output_path}")
