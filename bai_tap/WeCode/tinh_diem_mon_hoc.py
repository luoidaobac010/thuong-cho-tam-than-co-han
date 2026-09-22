n = int(input("Nhập số cột điểm n: ").strip())
w = [0] * (n + 1)
for i in range(1, n + 1):
    w[i] = int(input(f"Nhập hệ số cho cột {i} (%): ").strip())
I_target = float(input("Nhập điểm trung bình môn mục tiêu: ").strip())

# MẸO XỬ LÝ SỐ THẬP PHÂN:
# Để tránh sai số của số thập phân (float), ta nhân mọi thứ với 400 để tính toán trên số nguyên.
# Điểm S_i = V_i * 0.25 (với V_i chạy từ 1 đến 40).
# Trung bình = sum(V_i * 0.25 * w_i / 100) = sum(V_i * w_i) / 400.
# Làm tròn đến 0.1 nghĩa là: I - 0.05 <= Trung bình < I + 0.05
# => 400*I - 20 <= sum(V_i * w_i) <= 400*I + 19
min_T = round(I_target * 400) - 20
max_T = round(I_target * 400) + 19

# rem_w[i] lưu tổng trọng số của các cột từ i+1 đến n
rem_w = [0] * (n + 1)
for i in range(1, n + 1):
    rem_w[i] = sum(w[k] for k in range(i + 1, n + 1))

S = [0] * (n + 1)
current_T = 0 # Biến lưu trữ tổng sum(V_i * w_i) hiện tại

def format_score(v):
    s = v * 0.25
    if s.is_integer():
        return str(int(s))
    return str(s)

def xuat_loi_giai():
    print(" ".join(format_score(S[idx]) for idx in range(1, n + 1)))

# Vẫn là Mô hình 1 của Cô Thương, nhưng bổ sung "Cắt tỉa" (Pruning) để chạy cực nhanh
def Try(i):
    global current_T
    
    # Tính trước: Nếu tất cả các cột còn lại đều lấy 10 (tức V_i = 40) hoặc 0.25 (tức V_i = 1)
    rem_max = rem_w[i] * 40
    rem_min = rem_w[i] * 1
    
    for j in range(1, 41): # Điểm từ 0.25 đến 10.0 => 40 khả năng
        new_T = current_T + j * w[i]
        
        # ĐIỀU KIỆN CHẤP NHẬN: Nhánh này CÓ CƠ HỘI lọt vào khoảng [min_T, max_T] sau khi cộng các cột còn lại
        if min_T <= new_T + rem_max and new_T + rem_min <= max_T:
            S[i] = j
            current_T = new_T # Ghi nhận trạng thái mới
            
            if i < n:
                Try(i + 1)
            else:
                xuat_loi_giai()
                
            current_T -= j * w[i] # Trả lại trạng thái cũ

if __name__ == '__main__':
    Try(1)
