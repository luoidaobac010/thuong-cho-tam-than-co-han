# Khởi tạo kích thước tối đa (n <= 9 theo đề bài, lấy dư tới 15 cho an toàn)
S = [0] * 15
used = [False] * 15
n = 0

def xuat_loi_giai():
    # Xuất lời giải S = (S1, S2, ..., Sn), các số cách nhau bằng khoảng trắng
    print(" ".join(str(S[idx]) for idx in range(1, n + 1)))

# Cài đặt chính xác theo Mô hình 1 của Giảng vi
def Try(i):
    global n, S, used
    
    for j in range(1, n + 1):             # j = 1 --> k (với k = n, số khả năng có thể chọn)
        if used[j] == False:              # Nếu khả năng j chấp nhận được
            
            S[i] = j                      # Xác định S_i theo j
            used[j] = True                # Ghi nhận trạng thái mới của bài toán
            
            if i < n:
                Try(i + 1)                # Tiến hành bước i+1
            else:
                xuat_loi_giai()           # Xuất lời giải
                
            used[j] = False               # Trả lại trạng thái cũ của bài toán

if __name__ == '__main__':
    # Đọc số n từ input có kèm câu nhắc
    n = int(input("Nhập số tự nhiên từ 1 đến 9: ").strip())

    # Khởi tạo trạng thái ban đầu (thực tế mảng đã khởi tạo False ở trên)
    for j in range(1, n + 1):
        used[j] = False

    # Bắt đầu chọn phần tử đầu tiên
    Try(1)
