def is_valid_part(s, start, end):
    """
    Kiểm tra xem chuỗi con từ vị trí start đến end có phải là một phần hợp lệ của địa chỉ IP không.
    - Chiều dài từ 1 đến 3 ký tự.
    - Không được bắt đầu bằng '0' nếu chiều dài lớn hơn 1 (VD: "01" là sai).
    - Giá trị số phải nằm trong khoảng 0 đến 255.
    """
    length = end - start + 1
    if length <= 0 or length > 3:
        return False
        
    if length > 1 and s[start] == '0':
        return False
        
    val = int(s[start:end+1])
    return 0 <= val <= 255

def solve(s):
    """
    Hàm chính giải quyết bài toán khôi phục địa chỉ IP.
    Bản code này dùng các biến local, viết theo style Pythonic hiện đại, 
    chú thích cực kì rõ ràng để dễ đọc, hiểu bản chất đệ quy.
    """
    n = len(s)
    current_ip_parts = [] # Mảng lưu các phần của IP đang được xây dựng (đóng vai trò như mảng S)
    
    # Một địa chỉ IP hợp lệ có tổng chiều dài từ 4 đến 12 ký tự (4 phần, mỗi phần 1-3 ký tự)
    if n < 4 or n > 12:
        return

    # Hàm đệ quy nội bộ
    def try_backtrack(start_index):
        # ĐIỀU KIỆN DỪNG: Đã có đủ 4 phần
        if len(current_ip_parts) == 4:
            # Và nếu đã xài hết toàn bộ chuỗi ban đầu -> Đây là 1 IP hợp lệ trọn vẹn
            if start_index == n:
                print(".".join(current_ip_parts))
            return
            
        # CẮT TỈA (Pruning) để thuật toán chạy tối ưu:
        # Nếu số lượng ký tự còn dư nhiều hơn khả năng chứa của các phần còn lại (tối đa 3 char/phần)
        # Hoặc ít hơn mức tối thiểu (1 char/phần) -> Nhánh này vô vọng, kết thúc sớm.
        parts_left = 4 - len(current_ip_parts)
        chars_left = n - start_index
        if chars_left > parts_left * 3 or chars_left < parts_left:
            return

        # VÒNG LẶP THỬ CÁC KHẢ NĂNG (Mô hình 1)
        # Một phần IP dài tối đa 3 ký tự, nên j chạy từ start_index tới start_index + 2
        for j in range(start_index, min(start_index + 3, n)):
            if is_valid_part(s, start_index, j):
                
                # Ghi nhận trạng thái: Thêm phần vừa cắt vào mảng tạm
                part = s[start_index : j+1]
                current_ip_parts.append(part)
                
                # Gọi đệ quy để xác định phần tử tiếp theo, bắt đầu từ j+1
                try_backtrack(j + 1)
                
                # Trả lại trạng thái cũ: Xóa phần vừa đưa vào để thử độ dài (khả năng j) khác
                current_ip_parts.pop()

    # Bắt đầu gọi đệ quy từ ký tự đầu tiên
    try_backtrack(0)

if __name__ == "__main__":
    # Test case ví dụ
    print("Kết quả cho chuỗi '25525511135':")
    solve("25525511135")
    
    # Bạn có thể tự mở comment các dòng dưới để nhập từ bàn phím
    # s = input("\nNhập chuỗi IP bị mất dấu chấm: ").strip()
    # solve(s)
