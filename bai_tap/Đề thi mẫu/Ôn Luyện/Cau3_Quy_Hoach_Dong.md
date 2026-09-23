# CÂU 3: THIẾT KẾ THUẬT TOÁN QUY HOẠCH ĐỘNG (DYNAMIC PROGRAMMING)
## MÔN: PHÂN TÍCH VÀ THIẾT KẾ THUẬT TOÁN (CS112) - CÔ HUỲNH THỊ THANH THƯƠNG

---

# PHẦN 1: QUY TRÌNH 4 BƯỚC CHUẨN CÔ THƯƠNG

Khi giải bất kỳ bài toán Quy hoạch động nào trong đề thi, cần trình bày rõ ràng 4 bước sau:
1. **Bước 1: Xác định bản chất bài toán con (Subproblems) và Ý nghĩa bảng DP:**
   - Định nghĩa mảng/bảng $DP$ (1 chiều hoặc 2 chiều).
   - Nêu rõ $DP[i][j]$ đại diện cho đại lượng tối ưu gì của bài toán con từ chỉ số $i$ đến $j$.
2. **Bước 2: Thiết lập Công thức truy hồi (Recurrence Relation):**
   - Trường hợp cơ sở (Base cases) khi kích thước bài toán con nhỏ nhất.
   - Công thức chuyển trạng thái tính $DP[i][j]$ từ các bài toán con đã giải trước đó.
3. **Bước 3: Thứ tự tính toán & Điền bảng (Bottom-Up Table Filling):**
   - Nêu rõ thứ tự điền bảng (theo độ dài đoạn $L = j - i + 1$, theo đường chéo chính từ dưới lên hay từ trái sang phải).
   - Điền đầy đủ giá trị vào bảng $DP$ và bảng lưu vết $trace$ (nếu có).
4. **Bước 4: Truy vết tìm nghiệm tối ưu (Reconstruction / Traceback):**
   - Trình bày giải thuật đệ quy hoặc vòng lặp để truy xuất lại lời giải từ bảng lưu vết.

---

# PHẦN 2: BÀI TOÁN MẪU ĐỀ THI 2025 - ĐẶT DẤU NGOẶC BIỂU THỨC TỐI ƯU

## Đề bài:
Xét biểu thức gồm $n+1$ số thực $x_0, x_1, \dots, x_n$ và $n$ toán tử $o_0, o_1, \dots, o_{n-1}$, được biểu diễn dưới dạng $x_0 o_0 x_1 o_1 \dots o_{n-1} x_n$, trong đó mỗi $o_i \in \{+, \times\}$. Giả sử các số hạng $x_i \ge 0$. Hãy xác định cách đặt dấu ngoặc sao cho giá trị của biểu thức là lớn nhất.

Cho biểu thức cụ thể $A = 1 + 2 \times 3 + 4$, với:
- Các số hạng: $x_0 = 1, x_1 = 2, x_2 = 3, x_3 = 4$
- Các toán tử: $o_0 = +, o_1 = \times, o_2 = +$

---

## Lời giải chi tiết:

### a. Phương trình Quy hoạch động (Yêu cầu b)

1. **Ý nghĩa bảng DP:**
   - Gọi $DP[i][j]$ ($0 \le i \le j \le n$) là giá trị lớn nhất có thể đạt được của biểu thức con từ $x_i$ đến $x_j$, tức đoạn $x_i o_i x_{i+1} \dots o_{j-1} x_j$.
2. **Công thức truy hồi:**
   - **Trường hợp cơ sở ($i = j$):** Biểu thức chỉ gồm 1 số hạng:
     $$DP[i][i] = x_i \quad (\forall 0 \le i \le n)$$
   - **Trường hợp tổng quát ($i < j$):** Một biểu thức từ $i$ đến $j$ được chia làm 2 biểu thức con tại toán tử thứ $k$ ($i \le k < j$):
     $$\text{Đoạn trái: } (x_i \dots x_k) \quad \text{Toán tử: } o_k \quad \text{Đoạn phải: } (x_{k+1} \dots x_j)$$
     Do các số hạng không âm và chỉ gồm phép toán $\{+, \times\}$, giá trị lớn nhất đạt được khi cả hai đoạn trái và phải đều đạt giá trị lớn nhất:
     $$DP[i][j] = \max_{i \le k < j} \left\{ DP[i][k] \circ_k DP[k+1][j] \right\}$$
     *(trong đó $\circ_k$ là phép tính tương ứng của toán tử $o_k$)*

3. **Minh họa cách tính cho $DP[1][3]$:**
   - Đoạn con từ $x_1$ đến $x_3$ là $2 \times 3 + 4$ (các toán tử $o_1 = \times, o_2 = +$).
   - Vị trí chia $k$ có 2 khả năng ($k \in \{1, 2\}$):
     * Với $k = 1$ (chia tại toán tử $o_1 = \times$):
       $$\text{Giá trị} = DP[1][1] \times DP[2][3] = 2 \times 7 = 14$$
     * Với $k = 2$ (chia tại toán tử $o_2 = +$):
       $$\text{Giá trị} = DP[1][2] + DP[3][3] = 6 + 4 = 10$$
   - Do đó:
     $$DP[1][3] = \max(14, 10) = 14 \quad (\text{đạt được khi } k = 1)$$

---

### b. Bảng tính Quy hoạch động $DP[i][j]$ và Lời giải tối ưu (Yêu cầu a)

Thứ tự tính toán theo độ dài đoạn con $L = j - i + 1$ từ $1$ đến $4$:

1. **Độ dài $L = 1$ (Đường chéo chính $i = j$):**
   - $DP[0][0] = x_0 = 1$
   - $DP[1][1] = x_1 = 2$
   - $DP[2][2] = x_2 = 3$
   - $DP[3][3] = x_3 = 4$

2. **Độ dài $L = 2$ ($j = i + 1$):**
   - $DP[0][1] = DP[0][0] + DP[1][1] = 1 + 2 = 3$ ($k=0$)
   - $DP[1][2] = DP[1][1] \times DP[2][2] = 2 \times 3 = 6$ ($k=1$)
   - $DP[2][3] = DP[2][2] + DP[3][3] = 3 + 4 = 7$ ($k=2$)

3. **Độ dài $L = 3$ ($j = i + 2$):**
   - $DP[0][2]$ ($k \in \{0, 1\}$):
     * $k = 0: DP[0][0] + DP[1][2] = 1 + 6 = 7$
     * $k = 1: DP[0][1] \times DP[2][2] = 3 \times 3 = 9$
     $\implies DP[0][2] = \max(7, 9) = 9$ ($k=1$).
   - $DP[1][3]$ ($k \in \{1, 2\}$):
     * $k = 1: DP[1][1] \times DP[2][3] = 2 \times 7 = 14$
     * $k = 2: DP[1][2] + DP[3][3] = 6 + 4 = 10$
     $\implies DP[1][3] = \max(14, 10) = 14$ ($k=1$).

4. **Độ dài $L = 4$ ($j = i + 3$, tức $DP[0][3]$):**
   - $k = 0: DP[0][0] + DP[1][3] = 1 + 14 = 15$
   - $k = 1: DP[0][1] \times DP[2][3] = 3 \times 7 = 21$
   - $k = 2: DP[0][2] + DP[3][3] = 9 + 4 = 13$
   $\implies DP[0][3] = \max(15, 21, 13) = 21$ ($k=1$).

---

### BẢNG ĐIỀN KẾT QUẢ $DP[i][j]$:

| | $j = 0$ | $j = 1$ | $j = 2$ | $j = 3$ |
| :---: | :---: | :---: | :---: | :---: |
| **$i = 0$** | **1** | **3** | **9** | **21** |
| **$i = 1$** | - | **2** | **6** | **14** |
| **$i = 2$** | - | - | **3** | **7** |
| **$i = 3$** | - | - | - | **4** |

### BẢNG LƯU VẾT $trace[i][j]$ (Vị trí $k$ tối ưu):

| | $j = 0$ | $j = 1$ | $j = 2$ | $j = 3$ |
| :---: | :---: | :---: | :---: | :---: |
| **$i = 0$** | - | 0 | 1 | **1** |
| **$i = 1$** | - | - | 1 | 1 |
| **$i = 2$** | - | - | - | 2 |
| **$i = 3$** | - | - | - | - |

**Kết luận:**
- **Giá trị lớn nhất có thể đạt được:** $DP[0][3] = 21$.
- **Cách đặt dấu ngoặc tương ứng:**
  - Tại $(0, 3)$, vết cắt tối ưu là $k = 1 \implies (A_{0..1}) \times (A_{2..3})$.
  - Đoạn trái $(0, 1)$ cắt tại $k = 0 \implies (x_0 + x_1) = (1 + 2)$.
  - Đoạn phải $(2, 3)$ cắt tại $k = 2 \implies (x_2 + x_3) = (3 + 4)$.
  - Biểu thức tối ưu là: **$((1 + 2) \times (3 + 4)) = 3 \times 7 = 21$**.

---

### c. Ý tưởng truy xuất lời giải tối ưu (Yêu cầu c)

1. **Xác định giá trị lớn nhất:**
   - Tra trực tiếp ô góc trên bên phải của bảng: $\text{Max\_Value} = DP[0][n]$.
2. **Thuật toán truy vết đặt dấu ngoặc:**
   - Sử dụng bảng $trace[i][j]$ để ghi nhớ chỉ số $k$ mang lại giá trị lớn nhất khi tính $DP[i][j]$.
   - Xây dựng hàm đệ quy `Print_Optimal_Parens(trace, i, j)`:
     ```text
     Thuật toán Print_Optimal_Parens(trace, i, j):
     1. Nếu i == j thì:
     2.    In ra "x" + i
     3. Ngược lại:
     4.    In ra "("
     5.    Print_Optimal_Parens(trace, i, trace[i][j])
     6.    In ra toán tử o_{trace[i][j]}
     7.    Print_Optimal_Parens(trace, trace[i][j] + 1, j)
     8.    In ra ")"
     ```
   - Gọi hàm ban đầu: `Print_Optimal_Parens(trace, 0, n)` sẽ in ra đúng cấu trúc đặt dấu ngoặc tối ưu.

---

# PHẦN 3: DẠNG BÀI DÃY CON TĂNG DÀI NHẤT (LIS - TRỌNG TÂM BUỔI 8)

## 1. Phát biểu bài toán:
Cho mảng $A = (a_0, a_1, \dots, a_{n-1})$ gồm $n$ phần tử. Hãy tìm độ dài và chỉ ra một dãy con tăng dài nhất trên mảng $A$ (các phần tử trong dãy con không nhất thiết phải liên tiếp nhau).

## 2. Thiết kế thuật toán Quy hoạch động 4 bước:

### Bước 1: Xác định bài toán con & Ý nghĩa bảng DP
- Sử dụng mảng một chiều $M[0..n-1]$:
  - $M[i]$ là **độ dài của dãy con tăng dài nhất có phần tử kết thúc là $a_i$**.
- Mảng truy vết $S[0..n-1]$:
  - $S[i]$ lưu **chỉ số (index) của phần tử đứng ngay trước $a_i$** trong dãy con tăng tối ưu kết thúc tại $a_i$ (nếu $a_i$ là phần tử đầu tiên thì $S[i] = -1$).

### Bước 2: Phương trình Quy hoạch động
- **Cơ sở:** Với dãy con chỉ gồm đúng 1 phần tử $a_i$, độ dài là $1$:
  $$M[i] = 1 \quad \text{và} \quad S[i] = -1 \quad (\forall 0 \le i < n)$$
- **Công thức chuyển trạng thái:** Xét các phần tử $a_j$ đứng trước $a_i$ ($0 \le j < i$) thỏa mãn điều kiện tăng $a_j < a_i$:
  $$M[i] = 1 + \max_{\substack{0 \le j < i \\ a_j < a_i}} \{ M[j] \}$$
  *(Nếu không có $j$ nào thỏa $a_j < a_i$ thì $M[i] = 1$)*
- Cập nhật vết: $S[i] = j^*$ (với $j^*$ là chỉ số đạt giá trị $M[j]$ lớn nhất).

### Bước 3: Điền bảng Bottom-Up & Lấy kết quả bài toán gốc
- **Thứ tự điền bảng:** Duyệt $i$ từ $0$ đến $n-1$. Tại mỗi $i$, duyệt $j$ từ $0$ đến $i-1$ để tìm $\max M[j]$.
- **Kết quả bài toán gốc:** Độ dài dãy con tăng dài nhất toàn mảng $A$ là:
  $$L_{max} = \max_{0 \le i < n} M[i]$$
  *(Lưu ý: Không phải ô cuối cùng $M[n-1]$ mà là ô có giá trị lớn nhất trên toàn mảng $M$)*.

### Bước 4: Thuật toán truy vết tìm dãy con
- Tìm chỉ số $pos$ sao cho $M[pos] = L_{max}$.
- Lần ngược theo mảng $S$: $pos \rightarrow S[pos] \rightarrow S[S[pos]] \dots$ cho đến khi gặp $-1$. Đảo ngược danh sách thu được để có dãy con tăng dài nhất.

---

# PHẦN 4: DẠNG BÀI NHÂN CHUỖI MA TRẬN (MATRIX CHAIN MULTIPLICATION - MCM)

## 1. Bài toán:
Cho chuỗi $n$ ma trận $A_1, A_2, \dots, A_n$, trong đó ma trận $A_i$ có kích thước $p_{i-1} \times p_i$. Cần tính tích $A_1 A_2 \dots A_n$ sao cho tổng số phép nhân vô hướng là ít nhất.

## 2. Công thức DP chuẩn:
- Gọi $m[i][j]$ là số phép nhân vô hướng tối thiểu để tính tích $A_i \dots A_j$ ($1 \le i \le j \le n$).
$$m[i][j] = \begin{cases} 0 & \text{khi } i = j \\ \min_{i \le k < j} \{ m[i][k] + m[k+1][j] + p_{i-1} p_k p_j \} & \text{khi } i < j \end{cases}$$
- Bảng lưu vết $s[i][j] = k$ ghi lại điểm phân hoạch tối ưu.
- Thứ tự tính toán: Theo độ dài chuỗi ma trận $L = 2, 3, \dots, n$.

## 3. Độ phức tạp:
- Thời gian: $O(n^3)$ (do có 3 vòng lặp: độ dài $L$, chỉ số bắt đầu $i$, và điểm cắt $k$).
- Không gian: $O(n^2)$ để lưu 2 bảng $m$ và $s$.
