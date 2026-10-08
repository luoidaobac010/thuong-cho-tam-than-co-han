# ĐỀ THI CUỐI HỌC KỲ III - THI THỬ SỐ 01
### MÔN: CS112 - PHÂN TÍCH VÀ THIẾT KẾ THUẬT TOÁN
*Thời gian: 90 phút*

---

## PHẦN 1: CÂU TRẢ LỜI NGẮN (6 điểm)

### Câu 1 (3 điểm) Ký hiệu tiệm cận
**a. (1.5 điểm)** Hãy dùng định nghĩa của các ký hiệu tiệm cận (không dùng định lý giới hạn) để chứng minh các nhận định sau:
1. (0.75 điểm) $f(n) = 3n^2 + 5n - 2$. Chứng minh $f(n) \in \Theta(n^2)$.
2. (0.75 điểm) $g(n) = n^3 + \log_2 n$. Chứng minh $g(n) \in \Omega(n^3)$.

**b. (1.5 điểm)** Sắp xếp các hàm sau theo thứ tự tăng dần của “Big-O nhỏ nhất” (bậc tăng trưởng từ thấp đến cao). Có giải thích ngắn gọn cách xác định:
$$n!, \quad 5\log_2(n^3), \quad 3^n, \quad 0.5n^4 + n^2, \quad \sqrt[3]{n}, \quad n \log_2 n$$

Thứ tự: ................................................................................

---

### Câu 2 (3 điểm) Phân tích thuật toán
**a. (1.5 điểm)** Hãy phân tích độ phức tạp của giải thuật sau:
```cpp
void solve(int n) {
    int count = 0;
    for (int i = 1; i <= n; i *= 2) {
        for (int j = 1; j <= n; j++) {
            count++;
        }
    }
    cout << count;
}
```
1. Lời gọi hàm `solve(n)` sẽ in ra thông tin gì?
2. Hãy đếm số phép toán cơ bản (phép `count++`). Trình bày cách suy ra công thức theo $n$, từ đó suy ra độ phức tạp tính toán của giải thuật.

**b. (1.5 điểm)** Thành lập phương trình đệ quy và giải để tìm độ phức tạp:
```cpp
int recurse(int n) {
    if (n <= 1) return 1;
    int sum = 0;
    for (int i = 1; i <= n; i++) {
        sum += i;
    }
    return 3 * recurse(n / 3) + sum;
}
```
1. Thành lập phương trình đệ quy $T(n)$ cho thời gian chạy.
2. Giải phương trình đệ quy bằng định lý Master (Master Theorem).

---

## PHẦN 2: TỰ LUẬN (6 điểm)

*Lưu ý: Yêu cầu viết mã giả (pseudocode) có chú thích rõ ràng.*

### Câu 3 (2 điểm) Phân tích bài toán - Trò chơi Dò mìn (Minesweeper)
Cho một ma trận $A$ kích thước $m \times n$ mô tả bản đồ dò mìn, trong đó:
- $A[i][j] = -1$ nghĩa là ô đó có mìn.
- $A[i][j] = 0$ nghĩa là ô đó an toàn.
Hãy viết thuật toán tính số lượng mìn nằm xung quanh mỗi ô an toàn (tính cả 8 ô xung quanh: trên, dưới, trái, phải và 4 góc chéo) và lưu kết quả lại vào chính ô đó trong ma trận $A$.
- Thiết kế thuật toán (Mã giả) và tính độ phức tạp.

### Câu 4 (2 điểm) Thiết kế thuật toán - Khôi phục địa chỉ IP
Cho một chuỗi $S$ chỉ gồm các chữ số (ví dụ: `25525511135`). Hãy tìm tất cả các cách có thể để chèn các dấu chấm `.` vào chuỗi $S$ để tạo thành một địa chỉ IPv4 hợp lệ.
Một địa chỉ IP hợp lệ gồm 4 phần, mỗi phần là số từ 0 đến 255 và không được có số 0 ở đầu (ngoại trừ chính số 0).
- Thiết kế thuật toán bằng phương pháp **Quay lui (Backtracking)**. Đánh giá độ phức tạp.

### Câu 5 (2 điểm) Quy hoạch động - Dãy con tăng dài nhất (Longest Increasing Subsequence)
Cho một mảng $A$ gồm $n$ số nguyên ($a_1, a_2, ..., a_n$). Hãy tìm độ dài của dãy con tăng ngặt dài nhất của $A$. (Dãy con không nhất thiết phải liên tiếp).
Ví dụ: $A = [10, 9, 2, 5, 3, 7, 101, 18]$ -> Dãy con dài nhất là $[2, 3, 7, 101]$ có độ dài là 4.
1. Xác định cấu trúc con tối ưu và xây dựng hệ thức truy hồi.
2. Viết mã giả thuật toán Quy hoạch động (Dynamic Programming). Đánh giá độ phức tạp Thời gian và Không gian.
