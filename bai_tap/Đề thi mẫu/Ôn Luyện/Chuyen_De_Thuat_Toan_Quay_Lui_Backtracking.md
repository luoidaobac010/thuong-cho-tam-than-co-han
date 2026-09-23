# CHUYÊN ĐỀ ÔN TẬP: THUẬT TOÁN QUAY LUI (BACKTRACKING)
## MÔN: PHÂN TÍCH VÀ THIẾT KẾ THUẬT TOÁN (CS112) - CÔ HUỲNH THỊ THANH THƯƠNG

---

# PHẦN 1: KHUNG MẪU LÝ THUYẾT & QUY TRÌNH THIẾT KẾ CHUẨN CÔ THƯƠNG

## 1. Bản chất của Thuật toán Quay lui (Backtracking)
- **Mục đích:** Tìm tất cả các nghiệm (hoặc một nghiệm thỏa mãn) của bài toán tổ hợp, bài toán tìm kiếm hành trình, hoặc bài toán thỏa mãn ràng buộc (Constraint Satisfaction Problem - CSP).
- **Biểu diễn nghiệm:** Nghiệm của bài toán được biểu diễn dưới dạng một bộ giá trị có thứ tự:
  $$X = (x_1, x_2, \dots, x_n)$$
  trong đó $x_k \in S_k$ ($S_k$ là tập các giá trị ứng viên có thể gán cho thành phần thứ $k$).
- **Nguyên lý Thử - Sai (Trial and Error):**
  - Xây dựng nghiệm từng bước $x_1 \rightarrow x_2 \rightarrow \dots \rightarrow x_k$.
  - Tại bước thứ $k$, thử lần lượt từng giá trị $v \in S_k$. Nếu $v$ thỏa mãn các điều kiện ràng buộc (`IsValid`), ta gán $x_k = v$ và tiến hành gọi đệ quy để xây dựng $x_{k+1}$.
  - Nếu đã thử hết các giá trị ở bước $k$ hoặc phát hiện đi vào ngõ cụt, thuật toán **quay lui (backtrack)** về bước $k-1$, hoàn trả lại trạng thái trước đó (undo state) để thử tiếp ứng viên khác.

---

## 2. Khung Mã Giả Chuẩn Của Thuật Toán Quay Lui

```text
Thuật toán Backtrack(k, n, State):
Đầu vào:
  - k: Bước/thành phần hiện tại cần xác định (1 <= k <= n)
  - n: Kích thước của không gian nghiệm
  - State: Trạng thái hiện tại của nghiệm và các cấu trúc dữ liệu bổ trợ
Đầu ra: In ra hoặc lưu trữ các nghiệm hợp lệ X[1..n].

1.  Xác định tập các ứng viên có thể S_k cho thành phần thứ k
2.  Với mỗi giá trị v trong tập S_k thực hiện:
3.      Nếu IsValid(v, k, State) == True thì:
4.          Gán X[k] = v
5.          Cập nhật trạng thái State (đánh dấu phần tử đã dùng, chiếm vị trí,...)
6.          Nếu k == n (hoặc thỏa điều kiện nghiệm hoàn chỉnh) thì:
7.              Ghi nhận / In nghiệm X[1..n]
8.          Ngược lại:
9.              Backtrack(k + 1, n, State)      // Đệ quy sang thành phần kế tiếp
10.         Hoàn tác cập nhật State             // QUAY LUI: Trả lại trạng thái trước khi chọn v
```

---

# PHẦN 2: TỔNG HỢP 10 BÀI TOÁN QUAY LUI KINH ĐIỂN & WECODE

---

## DẠNG 1: BÀI TOÁN N QUÂN HẬU (N-QUEENS PROBLEM)

### 1. Mô hình hóa bài toán:
- Đặt $n$ quân hậu lên bàn cờ $n \times n$ sao cho không có 2 quân hậu nào tấn công lẫn nhau (không cùng hàng, cùng cột, hoặc cùng đường chéo).
- **Biểu diễn nghiệm:** $X = (x_1, x_2, \dots, x_n)$, trong đó $x_i = j$ nghĩa là quân hậu ở hàng $i$ được đặt tại cột $j$ ($1 \le x_i \le n$).
- **Ràng buộc:**
  - Cùng cột: $x_i \ne x_j$ với mọi $i \ne j$.
  - Cùng đường chéo chính: $x_i - i \ne x_j - j \iff |x_i - x_j| \ne |i - j|$.
  - Cùng đường chéo phụ: $x_i + i \ne x_j + j \iff |x_i - x_j| \ne |i - j|$.

### 2. Cấu trúc dữ liệu & Mảng đánh dấu:
- `col[1..n]`: Đánh dấu cột đã có hậu hay chưa.
- `diag1[2..2n]`: Đánh dấu đường chéo phụ ($i + j$).
- `diag2[-(n-1)..(n-1)]`: Đánh dấu đường chéo chính ($i - j$).

### 3. Mã giả:
```text
Thuật toán N_Queens_Backtrack(i, n, X, col, d1, d2):
1.  Cho j chạy từ 1 đến n thực hiện:
2.      Nếu (col[j] == False) và (d1[i + j] == False) và (d2[i - j + n] == False) thì:
3.          X[i] = j
4.          col[j] = True; d1[i + j] = True; d2[i - j + n] = True
5.          Nếu i == n thì:
6.              In nghiệm X[1..n]
7.          Ngược lại:
8.              N_Queens_Backtrack(i + 1, n, X, col, d1, d2)
9.          col[j] = False; d1[i + j] = False; d2[i - j + n] = False  // Quay lui
```
- **Độ phức tạp:** Thời gian $O(n!)$, Không gian $O(n)$.

---

## DẠNG 2: BÀI TOÁN MÃ ĐI TUẦN (KNIGHT'S TOUR - ĐỀ THI 2025)

- **Mục tiêu:** Quân mã đi qua toàn bộ $n^2$ ô của bàn cờ $n \times n$, mỗi ô đúng 1 lần.
- **Biểu diễn:** Ma trận $Board[1..n][1..n]$ lưu thứ tự các bước từ $1$ đến $n^2$.
- **Mảng hướng:** $dx = [2, 1, -1, -2, -2, -1, 1, 2]$, $dy = [1, 2, 2, 1, -1, -2, -2, -1]$.
- **Mã giả:** (Xem chi tiết tại file [Cau5_Ma_Di_Tuan_Va_Quay_Lui.md](file:///Users/thangdo/www/thuong-cho-tam-than-co-han/bai_tap/Đề%20thi%20mẫu/Ôn%20Luyện/Cau5_Ma_Di_Tuan_Va_Quay_Lui.md)).
- **Độ phức tạp:** Thời gian $O(8^{n^2})$, Không gian $O(n^2)$.

---

## DẠNG 3: BÀI TOÁN SINH HOÁN VỊ / HOÁN VỊ CHỮ SỐ (WECODE)

- **Mục tiêu:** Liệt kê tất cả $n!$ hoán vị của tập $n$ phần tử.
- **Cấu trúc dữ liệu:** Mảng $X[1..n]$ và mảng đánh dấu `used[1..n]`.
- **Mã giả:** (Xem chi tiết tại file [Cau4_Liet_Ke_Hoan_Vi_Va_Giam_De_Tri_Quay_Lui.md](file:///Users/thangdo/www/thuong-cho-tam-than-co-han/bai_tap/Đề%20thi%20mẫu/Ôn%20Luyện/Cau4_Liet_Ke_Hoan_Vi_Va_Giam_De_Tri_Quay_Lui.md)).
- **Độ phức tạp:** Thời gian $O(n \cdot n!)$, Không gian $O(n)$.

---

## DẠNG 4: BÀI TOÁN GIẢI SUDOKU 9x9 (WECODE)

### 1. Mô hình hóa bài toán:
- Điền các chữ số từ $1$ đến $9$ vào các ô trống $(r, c)$ của bảng $9 \times 9$ sao cho mỗi chữ số xuất hiện đúng 1 lần trên mỗi hàng, mỗi cột, và mỗi khối con $3 \times 3$.

### 2. Mã giả:
```text
Thuật toán Solve_Sudoku(board):
1.  Tìm ô trống (r, c) đầu tiên có board[r][c] == 0
2.  Nếu không còn ô trống nào thì:
3.      Trả về True                           // Đã giải xong toàn bộ bảng Sudoku
4.  Cho num chạy từ 1 đến 9 thực hiện:
5.      Nếu IsValidSudoku(board, r, c, num) == True thì:
6.          board[r][c] = num                 // Thử điền chữ số num
7.          Nếu Solve_Sudoku(board) == True thì:
8.              Trả về True
9.          board[r][c] = 0                   // Quay lui: xóa số vừa điền
10. Trả về False                              // Không có số nào hợp lệ -> backtrack
```
- **Độ phức tạp:** Thời gian $O(9^{81})$ (trong thực tế rất nhanh nhờ cắt tỉa ràng buộc), Không gian $O(1)$.

---

## DẠNG 5: BÀI TOÁN KHÔI PHỤC ĐỊA CHỈ IP (RESTORE IP ADDRESSES - WECODE)

### 1. Mô hình hóa bài toán:
- Cho chuỗi ký tự số $S$. Cần chèn 3 dấu chấm `.` để tách $S$ thành 4 đoạn hợp lệ của địa chỉ IPv4 ($A.B.C.D$):
  - Mỗi đoạn có độ dài từ 1 đến 3 ký tự.
  - Giá trị nguyên của mỗi đoạn nằm trong đoạn $[0, 255]$.
  - Không có số 0 ở đầu (ngoại trừ chính số `0`).

### 2. Mã giả:
```text
Thuật toán Restore_IP_Backtrack(start_idx, part_count, current_ip, S, results):
1.  Nếu part_count == 4 và start_idx == length(S) thì:
2.      Thêm current_ip (bỏ dấu chấm cuối) vào results
3.      Trả về
4.  Nếu part_count == 4 hoặc start_idx == length(S) thì:
5.      Trả về
6.  Cho len chạy từ 1 đến 3 thực hiện:
7.      Nếu start_idx + len <= length(S) thì:
8.          sub = S[start_idx .. start_idx + len - 1]
9.          val = Integer(sub)
10.         Nếu (val <= 255) và (length(sub) == 1 hoặc sub[0] != '0') thì:
11.             Restore_IP_Backtrack(start_idx + len, part_count + 1, current_ip + sub + ".", S, results)
```
- **Độ phức tạp:** Thời gian $O(3^4) = O(1)$ (hằng số), Không gian $O(1)$.

---

## DẠNG 6: TÁCH CHUỖI ĐỐI XỨNG (PALINDROME PARTITIONING - WECODE)

### 1. Mô hình hóa bài toán:
- Phân hoạch chuỗi $S$ thành tất cả các danh sách chuỗi con sao cho mọi chuỗi con đều là chuỗi đối xứng (Palindrome).

### 2. Mã giả:
```text
Thuật toán Palindrome_Partition(start_idx, S, current_list, results):
1.  Nếu start_idx == length(S) thì:
2.      Thêm bản sao của current_list vào results
3.      Trả về
4.  Cho end_idx chạy từ start_idx đến length(S) - 1 thực hiện:
5.      sub = S[start_idx .. end_idx]
6.      Nếu IsPalindrome(sub) == True thì:
7.          Thêm sub vào current_list
8.          Palindrome_Partition(end_idx + 1, S, current_list, results)
9.          Xóa phần tử cuối khỏi current_list    // Quay lui
```
- **Độ phức tạp:** Thời gian $O(n \cdot 2^n)$, Không gian $O(n)$.

---

## DẠNG 7: TÌM TỪ TRONG Ô CHỮ (WORD SEARCH - WECODE)

### 1. Mô hình hóa:
- Cho bảng chữ cái kích thước $M \times N$ và một từ cần tìm $Word$. Xác định xem từ đó có tồn tại trên bảng hay không bằng cách di chuyển qua các ô kề cạnh (4 hướng), mỗi ô chỉ được dùng 1 lần trong từ.

### 2. Mã giả:
```text
Thuật toán Word_Search_DFS(r, c, k, board, Word, M, N):
1.  Nếu k == length(Word) thì:
2.      Trả về True
3.  Nếu (r < 0 hoặc r >= M hoặc c < 0 hoặc c >= N hoặc board[r][c] != Word[k]) thì:
4.      Trả về False
5.  temp = board[r][c]
6.  board[r][c] = '#'                         // Đánh dấu ô đang được sử dụng
7.  res = Word_Search_DFS(r+1, c, k+1) hoặc
          Word_Search_DFS(r-1, c, k+1) hoặc
          Word_Search_DFS(r, c+1, k+1) hoặc
          Word_Search_DFS(r, c-1, k+1)
8.  board[r][c] = temp                        // QUAY LUI: Phục hồi lại ký tự ô
9.  Trả về res
```
- **Độ phức tạp:** Thời gian $O(M \cdot N \cdot 4^L)$ với $L$ là độ dài từ, Không gian $O(L)$.

---

## DẠNG 8: TÍNH ĐIỂM MÔN HỌC / TỔNG TẬP CON (SUBSET SUM - WECODE)

### 1. Mô hình hóa:
- Cho tập hợp các trọng số/điểm thành phần $A = \{a_1, a_2, \dots, a_n\}$ và giá trị mục tiêu $Target$. Tìm tất cả các tập con có tổng bằng đúng $Target$.

### 2. Mã giả với kỹ thuật Cắt tỉa (Pruning / Bounding):
```text
Thuật toán Subset_Sum_Backtrack(idx, current_sum, Target, A, n, current_subset, results):
1.  Nếu current_sum == Target thì:
2.      Thêm current_subset vào results
3.      Trả về
4.  Cho i chạy từ idx đến n thực hiện:
5.      Nếu current_sum + A[i] <= Target thì: // Nhánh cận: Cắt tỉa nhánh vượt quá Target
6.          Thêm A[i] vào current_subset
7.          Subset_Sum_Backtrack(i + 1, current_sum + A[i], Target, A, n, current_subset, results)
8.          Xóa A[i] khỏi current_subset      // Quay lui
```
- **Độ phức tạp:** Thời gian $O(2^n)$ (nhưng giảm đáng kể nhờ cắt tỉa), Không gian $O(n)$.

---

## DẠNG 9: BÀI TOÁN TÔ MÀU ĐỒ THỊ (M-COLORING PROBLEM)

### 1. Mô hình hóa:
- Cho đồ thị vô hướng $G = (V, E)$ gồm $n$ đỉnh và $M$ màu. Tô mỗi đỉnh bằng 1 trong $M$ màu sao cho không có 2 đỉnh kề nhau có cùng màu.

### 2. Mã giả:
```text
Thuật toán Graph_Coloring_Backtrack(u, n, M, color, adj_matrix):
1.  Nếu u > n thì:
2.      In phương án tô màu color[1..n]
3.      Trả về
4.  Cho c chạy từ 1 đến M thực hiện:
5.      Nếu IsSafeColor(u, c, color, adj_matrix) == True thì:
6.          color[u] = c
7.          Graph_Coloring_Backtrack(u + 1, n, M, color, adj_matrix)
8.          color[u] = 0                      // Quay lui
```
- **Độ phức tạp:** Thời gian $O(M^n)$, Không gian $O(n)$.

---

## DẠNG 10: BÀI TOÁN DÒ MÌN (MINESWEEPER - WECODE)

- **Mục tiêu:** Mở các ô trên bảng cờ $M \times N$ theo tọa độ click, cập nhật trạng thái đệ quy lan truyền nếu ô là rỗng (`'B'`) hoặc gán số lượng mìn xung quanh.
- **Mã giả:** Dùng Backtracking / DFS lan truyền 8 hướng xung quanh ô được click.
- **Độ phức tạp:** Thời gian $O(M \times N)$, Không gian $O(M \times N)$.

---

# PHẦN 3: BẢNG TỔNG HỢP SO SÁNH ĐỘ PHỨC TẠP CÁC BÀI TOÁN QUAY LUI

| STT | Bài toán | Kích thước không gian | Độ phức tạp thời gian | Bộ nhớ Stack & State | Kỹ thuật cắt tỉa chủ đạo |
| :---: | :--- | :---: | :---: | :---: | :--- |
| 1 | **N-Queens** | $n^n$ | $O(n!)$ | $O(n)$ | 3 mảng đánh dấu Cột & Đường chéo |
| 2 | **Mã đi tuần** | $8^{n^2}$ | $O(8^{n^2})$ | $O(n^2)$ | Heuristic Warnsdorff (bậc nhỏ nhất) |
| 3 | **Hoán vị** | $n!$ | $O(n \cdot n!)$ | $O(n)$ | Mảng boolean `used[]` |
| 4 | **Sudoku 9x9** | $9^{81}$ | $O(9^{81})$ | $O(1)$ | Kiểm tra Hàng, Cột, Khối $3 \times 3$ |
| 5 | **Khôi phục IP** | $3^4$ | $O(1)$ | $O(1)$ | Ràng buộc $[0..255]$ và số `0` đầu |
| 6 | **Tách Palindrome**| $2^n$ | $O(n \cdot 2^n)$ | $O(n)$ | Kiểm tra tính đối xứng của chuỗi con |
| 7 | **Word Search** | $4^L$ | $O(M \cdot N \cdot 4^L)$ | $O(L)$ | Đánh dấu ô đang duyệt bằng ký tự tạm |
| 8 | **Subset Sum** | $2^n$ | $O(2^n)$ | $O(n)$ | Cắt nhánh khi `sum + A[i] > Target` |
| 9 | **Tô màu đồ thị** | $M^n$ | $O(M^n)$ | $O(n)$ | Kiểm tra màu các đỉnh kề |
| 10 | **Dò mìn** | $8^{MN}$ | $O(M \cdot N)$ | $O(M \cdot N)$ | Dừng khi gặp ô có số lân cận $> 0$ |
