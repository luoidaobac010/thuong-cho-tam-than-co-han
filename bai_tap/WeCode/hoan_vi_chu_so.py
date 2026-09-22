# Đọc chuỗi số n đầu vào kèm câu nhắc
n_str = input("Nhập chuỗi số n (các chữ số tăng dần): ").strip()
L = len(n_str)

# Sắp xếp các chữ số theo thứ tự giảm dần để khi sinh hoán vị sẽ ra giảm dần
# Thêm một phần tử rỗng ở đầu để mảng A có index bắt đầu từ 1
A = [''] + sorted(list(n_str), reverse=True)

S = [0] * 15
used = [False] * 15

def xuat_loi_giai():
    # S[idx] lưu vị trí (index) của chữ số được chọn trong mảng A
    # Ta lấy A[S[idx]] để in ra chữ số tương ứng và nối lại thành 1 chuỗi
    print("".join(A[S[idx]] for idx in range(1, L + 1)))

# Cài đặt vẫn giữ đúng chuẩn 100% Mô hình 1 của Giảng viên
def Try(i):
    global L, S, used
    
    for j in range(1, L + 1):
        # Khả năng j chấp nhận được khi:
        # 1. Chưa dùng (used[j] == False)
        # 2. Xử lý trùng lặp: Nếu chữ số hiện tại giống chữ số trước đó,
        #    ta chỉ xét nó nếu chữ số trước đó đã được dùng trong nhánh này.
        if used[j] == False and (j == 1 or A[j] != A[j-1] or used[j-1] == True):
            S[i] = j
            used[j] = True
            
            if i < L:
                Try(i + 1)
            else:
                xuat_loi_giai()
                
            used[j] = False

if __name__ == '__main__':
    for j in range(1, L + 1):
        used[j] = False

    Try(1)
