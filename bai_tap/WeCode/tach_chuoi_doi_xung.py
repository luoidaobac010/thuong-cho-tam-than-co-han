def is_palindrome(s, left, right):
    """Hàm phụ trợ kiểm tra chuỗi con s[left...right] có phải là palindrome không"""
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True

def solve(s):
    n = len(s)
    current_partition = [] # Mảng lưu trữ các chuỗi con của cách chia hiện tại
    
    # Hàm Quay lui theo đúng Mô hình 1 (bản sạch, dễ đọc)
    def try_backtrack(start_index):
        # for (j = 1 --> k) // Số khả năng mà Si có thể chọn là các điểm cắt j
        for j in range(start_index, n):
            
            # if (khả năng j chấp nhận được)
            if is_palindrome(s, start_index, j):
                
                # Xác định Si theo j
                chuoi_con = s[start_index : j+1]
                
                # Ghi nhận trạng thái mới của bài toán
                current_partition.append(chuoi_con)
                
                # if (i < n) // Trong bài này: nếu điểm cắt tiếp theo chưa vượt quá chiều dài chuỗi
                if j + 1 < n:
                    # try(i+1) // Tiến hành bước i+1 để xác định tiếp Si+1
                    try_backtrack(j + 1)
                else:
                    # else Xuất lời giải S = (S1, S2, ..., Sn)
                    print(" ".join(current_partition))
                
                # Trả lại trạng thái cũ của bài toán
                current_partition.pop()

    # Bắt đầu quay lui từ ký tự đầu tiên của chuỗi (index = 0)
    if n > 0:
        try_backtrack(0)

if __name__ == "__main__":
    # Test case ví dụ
    print("Test với chuỗi: aab")
    solve("aab")
    
    # Bạn có thể tự mở comment dòng dưới để nhập từ bàn phím
    # s = input("Nhập chuỗi s: ").strip()
    # solve(s)
