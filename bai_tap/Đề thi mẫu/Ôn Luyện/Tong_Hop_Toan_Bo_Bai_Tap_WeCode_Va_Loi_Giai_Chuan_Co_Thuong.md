# TỔNG HỢP TOÀN BỘ BÀI TẬP WECODE & LỜI GIẢI CHUẨN THI
## MÔN: PHÂN TÍCH VÀ THIẾT KẾ THUẬT TOÁN (CS112) - CÔ HUỲNH THỊ THANH THƯƠNG

> 🔴 **LƯU Ý ĐẶC BIỆT TỪ CÔ THƯƠNG:** Đề thi tự luận (Câu 3, 4, 5) hoặc phân tích thuật toán (Câu 2) có thể lấy **BẤT KỲ BÀI TOÁN NÀO TRONG HỆ THỐNG BÀI TẬP WECODE**.
> Mỗi bài toán dưới đây đều được biên soạn theo đúng quy chuẩn 5 phần chấm điểm của cô:
> 1. Phát biểu bài toán & Xác định Input/Output
> 2. Ý tưởng thiết kế & Chiến lược thuật toán
> 3. Ví dụ minh họa từng bước
> 4. Mã giả (Pseudocode) đánh số bước (1, 2, 3...) kèm giải thích biến
> 5. Đánh giá độ phức tạp thời gian & không gian

---

# MỤC LỤC CÁC BÀI TOÁN WECODE

1. [Bài 1: Tính Điểm Môn Học (Grade Target / Subset Sum with Weights)](#bài-1-tính-điểm-môn-học)
2. [Bài 2: Khôi Phục Địa Chỉ IP (Restore IP Addresses)](#bài-2-khôi-phục-địa-chỉ-ip)
3. [Bài 3: Tách Chuỗi Đối Xứng (Palindrome Partitioning)](#bài-3-tách-chuỗi-đối-xứng)
4. [Bài 4: Tìm Từ Trong Ô Chữ (Word Search / Matrix DFS)](#bài-4-tìm-từ-trong-ô-chữ)
5. [Bài 5: Giải Sudoku 9x9 (Sudoku Solver)](#bài-5-giải-sudoku-9x9)
6. [Bài 6: Sinh Hoán Vị & Hoán Vị Chữ Số (Permutations)](#bài-6-sinh-hoán-vị--hoán-vị-chữ-số)
7. [Bài 7: Giải Trò Chơi Dò Mìn (Minesweeper Solver)](#bài-7-giải-trò-chơi-dò-mìn)
8. [Bài 8: Dãy Con Tăng Dài Nhất (Longest Increasing Subsequence - LIS)](#bài-8-dãy-con-tăng-dài-nhất-lis)
9. [Bài 9: Bài Toán Cái Túi 0/1 (0/1 Knapsack)](#bài-9-bài-toán-cái-túi-01)
10. [Bài 10: Nhân Chuỗi Ma Trận (Matrix Chain Multiplication - MCM)](#bài-10-nhân-chuỗi-ma-trận)

---

# CHI TIẾT LỜI GIẢI TỪNG BÀI TOÁN WECODE

---

## BÀI 1: TÍNH ĐIỂM MÔN HỌC

### 1. Phát biểu bài toán:
Cho môn học có $n$ cột điểm với trọng số tương ứng $w_1, w_2, \dots, w_n$ (tổng trọng số $\sum w_i = 100\%$). Điểm của mỗi cột nhận các giá trị từ $0.25$ đến $10.0$ với bước nhảy $0.25$ (tức $S_i \in \{0.25, 0.5, 0.75, \dots, 10.0\}$). Điểm trung bình môn được làm tròn đến $0.1$. Cho điểm trung bình mục tiêu $I_{target}$, hãy liệt kê tất cả các bộ điểm $(S_1, S_2, \dots, S_n)$ thỏa mãn.

- **Input:**
  - $n$: Số cột điểm.
  - $w_1, w_2, \dots, w_n$: Mảng trọng số (%) của $n$ cột.
  - $I_{target}$: Điểm trung bình mục tiêu (số thực).
- **Output:** Tất cả các bộ điểm $(S_1, \dots, S_n)$ có điểm trung bình sau khi làm tròn bằng $I_{target}$.

### 2. Ý tưởng giải & Chiến lược Quay lui với Nhánh Cận (Backtracking with Pruning):
- **Quy đổi số nguyên để tránh sai số dấu phẩy động:**
  - Đặt $V_i = S_i / 0.25 \implies V_i \in \{1, 2, \dots, 40\}$.
  - Điểm trung bình: $\frac{\sum V_i \cdot w_i}{400}$.
  - Điều kiện làm tròn đến $0.1$ bằng $I_{target}$:
    $$I_{target} - 0.05 \le \frac{\sum V_i \cdot w_i}{400} < I_{target} + 0.05$$
    $$\iff \text{min\_T} \le \sum_{i=1}^n V_i \cdot w_i \le \text{max\_T}$$
    với $\text{min\_T} = \text{round}(I_{target} \cdot 400) - 20$ và $\text{max\_T} = \text{round}(I_{target} \cdot 400) + 19$.
- **Cắt tỉa nhánh cận:** Tại bước chọn điểm cho cột $i$, tính tổng trọng số còn lại $rem\_w[i] = \sum_{k=i+1}^n w_k$.
  - Điểm tối đa các cột sau có thể đạt: $rem\_max = rem\_w[i] \times 40$.
  - Điểm tối thiểu các cột sau có thể đạt: $rem\_min = rem\_w[i] \times 1$.
  - Nếu tổng điểm hiện tại cộng $rem\_max < \text{min\_T}$ hoặc cộng $rem\_min > \text{max\_T} \implies$ Cắt tỉa nhánh ngay lập tức.

### 3. Mã giả chuẩn cô Thương:
```text
Thuật toán Tinh_Diem_Mon_Hoc(i, current_T, n, w, rem_w, S, min_T, max_T):
Đầu vào:
  - i: Cột điểm hiện tại cần thử (1 <= i <= n)
  - current_T: Tổng sum(V_k * w_k) từ cột 1 đến i-1
  - S[1..n]: Mảng lưu điểm quy đổi của các cột
Đầu ra: In ra tất cả các bộ điểm thỏa mãn.

1.  rem_max = rem_w[i] * 40
2.  rem_min = rem_w[i] * 1
3.  Cho j chạy từ 1 đến 40 thực hiện:                    // j đại diện cho điểm j * 0.25
4.      new_T = current_T + j * w[i]
5.      // Kiểm tra điều kiện nhánh cận (Pruning)
6.      Nếu (min_T <= new_T + rem_max) và (new_T + rem_min <= max_T) thì:
7.          S[i] = j                                    // Ghi nhận điểm cột i
8.          Nếu i == n thì:
9.              In bộ điểm [S[1]*0.25, S[2]*0.25, ..., S[n]*0.25]
10.         Ngược lại:
11.             Tinh_Diem_Mon_Hoc(i + 1, new_T, n, w, rem_w, S, min_T, max_T)
```
- **Độ phức tạp:** Thời gian $O(40^n)$ (trong thực tế chạy dưới 0.1s nhờ cắt tỉa nhánh cận cực mạnh), Không gian $O(n)$.

---

## BÀI 2: KHÔI PHỤC ĐỊA CHỈ IP (RESTORE IP ADDRESSES)

### 1. Phát biểu bài toán:
Cho một chuỗi ký tự chỉ gồm các chữ số $S$. Hãy khôi phục tất cả các địa chỉ IPv4 hợp lệ có thể tạo ra bằng cách chèn 3 dấu chấm `.` vào chuỗi $S$.
- Một địa chỉ IPv4 hợp lệ có dạng $A.B.C.D$ trong đó $0 \le A, B, C, D \le 255$ và không có số `0` ở đầu mỗi đoạn (trừ số `0` đứng một mình).
- **Ví dụ:** $S = \text{"25525511135"} \implies [\text{"255.255.11.135"}, \text{"255.255.111.35"}]$

### 2. Ý tưởng giải & Chiến lược Quay lui (Backtracking):
- Phân hoạch chuỗi $S$ thành 4 đoạn.
- Tại mỗi đoạn (từ đoạn 1 đến 4), thử lấy độ dài $len \in \{1, 2, 3\}$.
- Kiểm tra tính hợp lệ của đoạn con:
  1. $0 \le \text{giá trị số} \le 255$.
  2. Nếu $len > 1$, ký tự đầu tiên không được là `'0'`.
- Khi đã đủ 4 đoạn và duyệt hết chuỗi $S$, ghi nhận địa chỉ IP.

### 3. Mã giả chuẩn cô Thương:
```text
Thuật toán Restore_IP(start, part, current_ip, S, results):
1.  Nếu part == 4 và start == length(S) thì:
2.      Thêm current_ip (bỏ dấu '.' ở cuối) vào results
3.      Trả về
4.  Nếu part == 4 hoặc start == length(S) thì:
5.      Trả về
6.  Cho len chạy từ 1 đến 3 thực hiện:
7.      Nếu start + len <= length(S) thì:
8.          sub_str = S[start .. start + len - 1]
9.          val = StringToInteger(sub_str)
10.         Nếu (val <= 255) và (len == 1 hoặc sub_str[0] != '0') thì:
11.             Restore_IP(start + len, part + 1, current_ip + sub_str + ".", S, results)
```
- **Độ phức tạp:** Thời gian $O(3^4) = O(1)$ (hằng số), Không gian $O(1)$.

---

## BÀI 3: TÁCH CHUỖI ĐỐI XỨNG (PALINDROME PARTITIONING)

### 1. Phát biểu bài toán:
Cho một chuỗi ký tự $S$. Hãy chia chuỗi $S$ thành tất cả các danh sách chuỗi con sao cho mọi chuỗi con trong danh sách đều là chuỗi đối xứng (Palindrome).
- **Ví dụ:** $S = \text{"aab"} \implies [[\text{"a"}, \text{"a"}, \text{"b"}], [\text{"aa"}, \text{"b"}]]$

### 2. Ý tưởng giải & Chiến lược Quay lui:
- Duyệt từ chỉ số bắt đầu $start$ đến cuối chuỗi.
- Với mỗi vị trí kết thúc $end$, xét chuỗi con $S[start..end]$. Nếu chuỗi con này đối xứng (`IsPalindrome`), ta chọn chuỗi con này vào danh sách hiện tại và gọi đệ quy giải tiếp phần còn lại từ $end + 1$.
- Khi quay lui, xóa chuỗi con vừa thêm để thử các vị trí cắt khác.

### 3. Mã giả chuẩn cô Thương:
```text
Thuật toán Palindrome_Partition(start, S, current_list, results):
1.  Nếu start == length(S) thì:
2.      Thêm bản sao của current_list vào results
3.      Trả về
4.  Cho end chạy từ start đến length(S) - 1 thực hiện:
5.      sub = S[start .. end]
6.      Nếu IsPalindrome(sub) == True thì:
7.          Thêm sub vào cuối current_list
8.          Palindrome_Partition(end + 1, S, current_list, results)
9.          Xóa phần tử cuối khỏi current_list      // Quay lui (Backtrack)
```
- **Độ phức tạp:** Thời gian $O(n \cdot 2^n)$, Không gian $O(n)$.

---

## BÀI 4: TÌM TỪ TRONG Ô CHỮ (WORD SEARCH)

### 1. Phát biểu bài toán:
Cho bảng chữ cái kích thước $M \times N$ và một từ cần tìm $Word$. Xác định xem từ đó có tồn tại trên bảng hay không bằng cách di chuyển qua các ô kề cạnh (4 hướng: lên, xuống, trái, phải), mỗi ô chỉ được dùng tối đa 1 lần trong từ.

### 2. Ý tưởng giải & Chiến lược Quay lui trên Ma trận (DFS Backtracking):
- Thử bắt đầu từ mọi ô $(r, c)$ trên bảng có $Board[r][c] == Word[0]$.
- Tại mỗi bước thứ $k$ của từ, nếu khớp ký tự:
  1. Đánh dấu ô hiện tại là đã dùng (gán tạm $Board[r][c] = '\#'$).
  2. Đệ quy tìm tiếp ký tự $k+1$ ở 4 ô lân cận $(r \pm 1, c)$ và $(r, c \pm 1)$.
  3. Hoàn tác $Board[r][c]$ về lại ký tự ban đầu khi quay lui.

### 3. Mã giả chuẩn:
```text
Thuật toán Word_Search_DFS(r, c, k, Board, Word, M, N):
1.  Nếu k == length(Word) thì trả về True
2.  Nếu (r < 0 hoặc r >= M hoặc c < 0 hoặc c >= N hoặc Board[r][c] != Word[k]) thì:
3.      Trả về False
4.  temp = Board[r][c]
5.  Board[r][c] = '#'                           // Đánh dấu ô đang duyệt
6.  found = Word_Search_DFS(r+1, c, k+1, Board, Word, M, N) hoặc
            Word_Search_DFS(r-1, c, k+1, Board, Word, M, N) hoặc
            Word_Search_DFS(r, c+1, k+1, Board, Word, M, N) hoặc
            Word_Search_DFS(r, c-1, k+1, Board, Word, M, N)
7.  Board[r][c] = temp                          // Quay lui: Phục hồi lại ký tự
8.  Trả về found
```
- **Độ phức tạp:** Thời gian $O(M \cdot N \cdot 4^L)$ với $L$ là độ dài từ, Không gian $O(L)$.

---

## BÀI 5: GIẢI SUDOKU 9x9

### 1. Phát biểu bài toán:
Điền các số từ $1$ đến $9$ vào bảng Sudoku $9 \times 9$ có sẵn các ô số và ô trống (ô chứa số 0) sao cho mỗi số xuất hiện đúng 1 lần trên mỗi hàng, mỗi cột và mỗi khối $3 \times 3$.

### 2. Ý tưởng & Mã giả:
```text
Thuật toán Solve_Sudoku(Board):
1.  Tìm ô trống đầu tiên (r, c) có Board[r][c] == 0
2.  Nếu không còn ô trống nào thì trả về True
3.  Cho num chạy từ 1 đến 9 thực hiện:
4.      Nếu IsSafe(Board, r, c, num) == True thì:
5.          Board[r][c] = num
6.          Nếu Solve_Sudoku(Board) == True thì trả về True
7.          Board[r][c] = 0                     // Quay lui
8.  Trả về False
```
- **Độ phức tạp:** Thời gian $O(9^{81})$, Không gian $O(1)$.

---

## BÀI 6: SINH HOÁN VỊ & HOÁN VỊ CHỮ SỐ

- **Mô hình hóa:** Liệt kê $n!$ hoán vị của $n$ phần tử.
- **Mã giả:** (Xem chi tiết tại file [Cau4_Liet_Ke_Hoan_Vi_Va_Giam_De_Tri_Quay_Lui.md](file:///Users/thangdo/www/thuong-cho-tam-than-co-han/bai_tap/Đề%20thi%20mẫu/Ôn%20Luyện/Cau4_Liet_Ke_Hoan_Vi_Va_Giam_De_Tri_Quay_Lui.md)).
- **Độ phức tạp:** Thời gian $O(n \cdot n!)$, Bộ nhớ $O(n)$.

---

## BÀI 7: GIẢI TRÒ CHƠI DÒ MÌN (MINESWEEPER)

### 1. Phát biểu bài toán:
Cho bàn cờ $M \times N$ gồm các ô chưa mở (`'E'`), ô có mìn (`'M'`). Khi người chơi click vào ô $(r, c)$:
- Nếu trúng mìn `'M'` $\rightarrow$ đổi thành `'X'` (thua).
- Nếu xung quanh ô có mìn $\rightarrow$ hiển thị số lượng mìn lân cận (từ 1 đến 8).
- Nếu xung quanh không có mìn nào $\rightarrow$ đổi thành `'B'` và lan truyền đệ quy mở tiếp 8 ô lân cận.

### 2. Mã giả chuẩn:
```text
Thuật toán Reveal_Minesweeper(r, c, Board, M, N):
1.  Nếu Board[r][c] == 'M' thì:
2.      Board[r][c] = 'X'; Trả về
3.  count = Đếm số mìn ở 8 ô lân cận của (r, c)
4.  Nếu count > 0 thì:
5.      Board[r][c] = Character(count)
6.  Ngược lại:
7.      Board[r][c] = 'B'
8.      Với mỗi ô (nr, nc) trong 8 ô lân cận hợp lệ:
9.          Nếu Board[nr][nc] == 'E' thì:
10.             Reveal_Minesweeper(nr, nc, Board, M, N)
```
- **Độ phức tạp:** Thời gian $O(M \cdot N)$, Không gian $O(M \cdot N)$.

---

## BÀI 8: DÃY CON TĂNG DÀI NHẤT (LIS - DYNAMIC PROGRAMMING)

### 1. Phát biểu & Bảng DP:
- $M[i]$: Độ dài dãy con tăng dài nhất kết thúc tại $a_i$. Cơ sở: $M[i] = 1, S[i] = -1$.
- Công thức: $M[i] = 1 + \max_{0 \le j < i, a_j < a_i} \{ M[j] \}$.
- Kết quả: $L_{max} = \max_{0 \le i < n} M[i]$. Bảng vết $S[i] = j^*$ để in dãy con.
- **Độ phức tạp:** Thời gian $O(n^2)$, Bộ nhớ $O(n)$.

---

## BÀI 9: BÀI TOÁN CÁI TÚI 0/1 (0/1 KNAPSACK)

### 1. Công thức DP:
- $DP[i][w]$: Giá trị lớn nhất khi xét $i$ đồ vật đầu tiên với sức chứa $w$.
$$DP[i][w] = \begin{cases} DP[i-1][w] & \text{khi } w_i > w \\ \max(DP[i-1][w], DP[i-1][w - w_i] + v_i) & \text{khi } w_i \le w \end{cases}$$
- **Độ phức tạp:** Thời gian $O(n \cdot W)$, Bộ nhớ $O(n \cdot W)$.

---

## BÀI 10: NHÂN CHUỖI MA TRẬN (MATRIX CHAIN MULTIPLICATION - MCM)

### 1. Công thức DP:
- $m[i][j]$: Số phép nhân vô hướng tối thiểu nhân $A_i \dots A_j$.
$$m[i][j] = \begin{cases} 0 & \text{khi } i = j \\ \min_{i \le k < j} \{ m[i][k] + m[k+1][j] + p_{i-1} p_k p_j \} & \text{khi } i < j \end{cases}$$
- **Độ phức tạp:** Thời gian $O(n^3)$, Bộ nhớ $O(n^2)$.
