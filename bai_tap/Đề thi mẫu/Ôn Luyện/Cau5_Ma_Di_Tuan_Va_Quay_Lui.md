# CÂU 5: BÀI TOÁN MÃ ĐI TUẦN (KNIGHT'S TOUR) & PHƯƠNG PHÁP QUAY LUI
## MÔN: PHÂN TÍCH VÀ THIẾT KẾ THUẬT TOÁN (CS112) - CÔ HUỲNH THỊ THANH THƯƠNG

---

# PHẦN 1: MÔ HÌNH HÓA BÀI TOÁN VÀ ĐẶT VẤN ĐỀ

## 1. Mô hình hóa bài toán
- **Không gian bài toán:** Bàn cờ vuông kích thước $n \times n$ ô, được biểu diễn bằng hệ tọa độ Descartes rời rạc $(x, y)$ với $1 \le x \le n$ và $1 \le y \le n$.
- **Quy tắc di chuyển của quân mã (Knight's Move):**
  - Từ vị trí hiện tại $(x, y)$, quân mã có thể di chuyển theo hình chữ L (2 ô một hướng và 1 ô vuông góc), tương ứng tối đa **8 nước đi hợp lệ**:
    $$(x \pm 1, y \pm 2) \quad \text{hoặc} \quad (x \pm 2, y \pm 1)$$
  - Điều kiện hợp lệ của nước đi $(u, v)$:
    1. **Nằm trong bàn cờ:** $1 \le u \le n$ và $1 \le v \le n$.
    2. **Chưa từng đi qua:** Ô $(u, v)$ chưa được quân mã ghé thăm ở các bước trước đó.
- **Mục tiêu bài toán:** Tìm một chuỗi $n^2$ nước đi bắt đầu từ $(x_0, y_0)$ sao cho quân mã đi qua toàn bộ $n^2$ ô của bàn cờ, mỗi ô đúng 1 lần (Hành trình Hamilton trên đồ thị các nước đi của quân mã).

---

# PHẦN 2: THIẾT KẾ CẤU TRÚC DỮ LIỆU

1. **Ma trận bàn cờ $Board[1..n][1..n]$:**
   - Dùng để ghi nhận thứ tự bước đi mà quân mã đặt chân tới từng ô.
   - Ban đầu, khởi tạo $Board[x][y] = 0$ với mọi $1 \le x, y \le n$ (ô chưa được đi qua).
   - Ô xuất phát: $Board[x_0][y_0] = 1$.
   - Nếu ô $(x, y)$ được đi ở bước thứ $k$, ta gán $Board[x][y] = k$ ($1 \le k \le n^2$).

2. **Mảng dịch chuyển tọa độ 8 hướng:**
   - Dùng hai mảng hằng số $dx[1..8]$ và $dy[1..8]$:
     $$dx = [2, 1, -1, -2, -2, -1, 1, 2]$$
     $$dy = [1, 2, 2, 1, -1, -2, -2, -1]$$
   - Tọa độ ô kế tiếp từ $(x, y)$ theo hướng thứ $i$ ($1 \le i \le 8$) là:
     $$u = x + dx[i], \quad v = y + dy[i]$$

3. **Hàm kiểm tra tính hợp lệ `IsValid(u, v, n, Board)`:**
   - Trả về `True` nếu $1 \le u \le n \land 1 \le v \le n \land Board[u][v] == 0$.
   - Trả về `False` trong các trường hợp còn lại.

---

# PHẦN 3: THIẾT KẾ THUẬT TOÁN QUAY LUI (BACKTRACKING)

## 1. Mã giả chi tiết thuật toán

```text
Thuật toán IsValid(u, v, n, Board):
1.  Nếu (1 <= u <= n) và (1 <= v <= n) và (Board[u][v] == 0) thì:
2.      Trả về True
3.  Trả về False

Thuật toán KnightTour_Backtracking(x, y, step, n, Board):
Đầu vào:
  - x, y: Tọa độ hiện tại của quân mã
  - step: Thứ tự bước đi hiện tại (ban đầu step = 1)
  - n: Kích thước bàn cờ
  - Board[1..n][1..n]: Bảng trạng thái bước đi
Đầu ra: In ra tất cả các hành trình hoàn chỉnh của quân mã.

1.  Nếu step == n * n thì:
2.      In ma trận Board[1..n][1..n]     // Đã đi qua tất cả n^2 ô -> In kết quả
3.      Trả về
4.  Cho i chạy từ 1 đến 8 thực hiện:     // Thử 8 hướng đi có thể của quân mã
5.      next_x = x + dx[i]
6.      next_y = y + dy[i]
7.      Nếu IsValid(next_x, next_y, n, Board) == True thì:
8.          Board[next_x][next_y] = step + 1   // Thử đi đến ô mới ở bước (step + 1)
9.          KnightTour_Backtracking(next_x, next_y, step + 1, n, Board) // Đệ quy bước kế tiếp
10.         Board[next_x][next_y] = 0          // Quay lui (Backtrack): trả ô về trạng thái trống

Thuật toán Giai_Ma_Di_Tuan(x0, y0, n):
1.  Khởi tạo ma trận Board[1..n][1..n] với tất cả các phần tử bằng 0
2.  Board[x0][y0] = 1                      // Đặt quân mã tại ô xuất phát
3.  Gọi KnightTour_Backtracking(x0, y0, 1, n, Board)
```

---

# PHẦN 4: ĐÁNH GIÁ ĐỘ PHỨC TẠP & KỸ THUẬT NÂNG CAO

## 1. Phân tích độ phức tạp
- **Thời gian (Time Complexity):**
  - Tại mỗi ô, quân mã có tối đa 8 hướng đi có thể.
  - Chiều sâu của cây đệ quy là $n^2$ bước.
  - Trường hợp xấu nhất (xét toàn bộ không gian trạng thái): $T(n) = O(8^{n^2})$.
  - Đối với $n \ge 8$, không gian trạng thái cực kỳ lớn ($8^{64} \approx 6.27 \times 10^{57}$).
- **Không gian (Space Complexity):**
  - Ma trận $Board$: $O(n^2)$.
  - Ngăn xếp đệ quy: Chiều sâu tối đa là $n^2 \implies O(n^2)$.
  - Tổng độ phức tạp không gian: $O(n^2)$.

## 2. Kỹ thuật tối ưu hóa Heuristic (Thuật toán Warnsdorff)
- **Ý tưởng Heuristic Warnsdorff:** Khi từ ô hiện tại có nhiều ô kế tiếp hợp lệ, ta **ưu tiên chọn ô kế tiếp có số nước đi tiếp theo ít nhất (bậc nhỏ nhất)**.
- **Lý do:** Đi vào các ô góc và ô rìa trước sẽ giúp tránh bị kẹt (ngõ cụt) ở giai đoạn cuối của hành trình.
- **Hiệu quả:** Cho phép tìm được 1 nghiệm hành trình của bàn cờ $n = 8 \times 8$ trong thời gian thực $O(n^2)$ gần như tuyến tính mà không cần quay lui nhiều lần.
