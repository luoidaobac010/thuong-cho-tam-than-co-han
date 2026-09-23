# BÀI GIẢI CHI TIẾT ĐỀ THI CUỐI HỌC KỲ I (2025-2026)
## MÔN: CS112 - PHÂN TÍCH VÀ THIẾT KẾ THUẬT TOÁN
### GIẢNG VIÊN: CÔ HUỲNH THỊ THANH THƯƠNG - TRƯỜNG ĐH CÔNG NGHỆ THÔNG TIN (UIT)

---

# PHẦN 1: BẮT BUỘC (7.5 điểm)

---

## CÂU 1 (2.5 điểm)

### a. (0.75 điểm) Dùng định nghĩa của các ký hiệu tiệm cận để chứng minh:
$$\text{Nếu } g(n) \in O(f(n)) \text{ và } f(n) \in O(g(n)) \text{ thì } O(f(n)) = O(g(n))$$

#### Lời giải chi tiết:
Để chứng minh $O(f(n)) = O(g(n))$, ta bắt buộc phải chứng minh 2 vế bao hàm:

1. **Vế 1: Chứng minh $O(f(n)) \subseteq O(g(n))$:**
   - Theo giả thiết $f(n) \in O(g(n))$, theo định nghĩa Big-O ta có:
     $$\exists c_1 \in \mathbb{R}^+, \exists n_1 \in \mathbb{N}, \forall n \ge n_1: 0 \le f(n) \le c_1 \cdot g(n)$$
   - Xét một hàm **bất kỳ** $h(n) \in O(f(n))$, theo định nghĩa Big-O ta có:
     $$\exists c_2 \in \mathbb{R}^+, \exists n_2 \in \mathbb{N}, \forall n \ge n_2: 0 \le h(n) \le c_2 \cdot f(n)$$
   - Với mọi $n \ge n_0 = \max(n_1, n_2)$, ta có:
     $$0 \le h(n) \le c_2 \cdot f(n) \le c_2 \cdot (c_1 \cdot g(n)) = (c_2 \cdot c_1) \cdot g(n)$$
   - Chọn hằng số $c = c_2 \cdot c_1 \in \mathbb{R}^+$ và $n_0 = \max(n_1, n_2) \in \mathbb{N}$.
   - Với mọi $n \ge n_0$, ta có $0 \le h(n) \le c \cdot g(n)$.
   - Theo định nghĩa của Big-O, suy ra $h(n) \in O(g(n))$.
   - Vì điều này đúng với mọi hàm $h(n)$ bất kỳ thuộc $O(f(n))$, ta có:
     $$O(f(n)) \subseteq O(g(n)) \quad (1)$$

2. **Vế 2: Chứng minh $O(g(n)) \subseteq O(f(n))$:**
   - Theo giả thiết $g(n) \in O(f(n))$, theo định nghĩa Big-O ta có:
     $$\exists c_3 \in \mathbb{R}^+, \exists n_3 \in \mathbb{N}, \forall n \ge n_3: 0 \le g(n) \le c_3 \cdot f(n)$$
   - Xét một hàm **bất kỳ** $k(n) \in O(g(n))$, theo định nghĩa Big-O ta có:
     $$\exists c_4 \in \mathbb{R}^+, \exists n_4 \in \mathbb{N}, \forall n \ge n_4: 0 \le k(n) \le c_4 \cdot g(n)$$
   - Với mọi $n \ge n_0' = \max(n_3, n_4)$, ta có:
     $$0 \le k(n) \le c_4 \cdot g(n) \le c_4 \cdot (c_3 \cdot f(n)) = (c_4 \cdot c_3) \cdot f(n)$$
   - Chọn hằng số $c' = c_4 \cdot c_3 \in \mathbb{R}^+$ và $n_0' = \max(n_3, n_4) \in \mathbb{N}$.
   - Với mọi $n \ge n_0'$, ta có $0 \le k(n) \le c' \cdot f(n)$.
   - Theo định nghĩa của Big-O, suy ra $k(n) \in O(f(n))$.
   - Vì điều này đúng với mọi hàm $k(n)$ bất kỳ thuộc $O(g(n))$, ta có:
     $$O(g(n)) \subseteq O(f(n)) \quad (2)$$

**Kết luận:** Từ $(1)$ và $(2)$ suy ra $O(f(n)) = O(g(n))$ ($\text{ĐPCM}$).

---

### b. (1.75 điểm) Phân lớp 07 hàm vào các “Big-O nhỏ nhất” và sắp xếp tăng dần:

| Hàm ban đầu | Biến đổi đưa về dạng chuẩn | Big-O nhỏ nhất | Giải thích ngắn gọn |
| :--- | :--- | :---: | :--- |
| $f_1(n) = 4^{\log n} + \log \log n$ | $4^{\log_2 n} = n^{\log_2 4} = n^2 \implies n^2 + \log \log n$ | $O(n^2)$ | Áp dụng công thức $a^{\log_b n} = n^{\log_b a}$, bậc cao nhất là $n^2$. |
| $f_2(n) = n \cdot \sqrt[3]{n}$ | $n \cdot n^{1/3} = n^{4/3} = n^{1.333}$ | $O(n^{4/3})$ | Tích hai lũy thừa cùng cơ số $n^{1 + 1/3} = n^{4/3}$. |
| $f_3(n) = \sum_{i=1}^n \sum_{j=1}^n (i \cdot j)$ | $\left(\sum_{i=1}^n i\right)\left(\sum_{j=1}^n j\right) = \left[\frac{n(n+1)}{2}\right]^2 = \frac{n^4 + 2n^3 + n^2}{4}$ | $O(n^4)$ | Tách thành tích 2 cấp số cộng, số hạng cao nhất là $\frac{n^4}{4}$. |
| $f_4(n) = n \cdot (\log n)^4$ | $n \cdot (\log n)^4$ | $O(n \log^4 n)$ | Đa thức bậc 1 nhân logarit bậc 4 (nhỏ hơn mọi $n^{1+\epsilon}$). |
| $f_5(n) = n^5 (\log n)^2$ | $n^5 (\log n)^2$ | $O(n^5 \log^2 n)$ | Đa thức bậc 5 nhân logarit bậc 2. |
| $f_6(n) = \sqrt{3^{\sqrt{n}}}$ | $(3^{\sqrt{n}})^{1/2} = 3^{\frac{\sqrt{n}}{2}} = (\sqrt{3})^{\sqrt{n}}$ | $O(3^{\sqrt{n}/2})$ | Hàm mũ của căn bậc hai $\sqrt{n}$ (lớn hơn mọi $n^k$, nhỏ hơn $a^n$). |
| $f_7(n) = \sqrt{n} \cdot 3^{n/2}$ | $\sqrt{n} \cdot (\sqrt{3})^n$ | $O(\sqrt{n} \cdot 3^{n/2})$ | Hàm mũ thực sự theo số mũ bậc nhất $n$, tăng nhanh nhất. |

**Kết luận Thứ tự các hàm tăng dần:**
$$f_4(n) < f_2(n) < f_1(n) < f_3(n) < f_5(n) < f_6(n) < f_7(n)$$

---

## CÂU 2 (2.5 điểm) - THÁP HÀ NỘI

### a. (1.0 điểm) Thành lập phương trình đệ quy đếm số thao tác transfer:
- Gọi $T(n)$ là số thao tác chuyển đĩa (`transfer`) cần thực hiện để chuyển $n$ đĩa từ cột $A$ sang $C$.
- **Trường hợp $n = 1$:** Thuật toán thực hiện 1 lần gọi `transfer(A, C)` $\implies T(1) = 1$.
- **Trường hợp $n > 1$:** Thuật toán thực hiện 3 bước:
  1. `hanoi(n-1, A, C, B)`: Cần $T(n-1)$ lần chuyển.
  2. `transfer(A, C)`: Đúng $1$ lần chuyển.
  3. `hanoi(n-1, B, A, C)`: Cần $T(n-1)$ lần chuyển.
  $\implies T(n) = T(n-1) + 1 + T(n-1) = 2T(n-1) + 1$.

**Hệ thức đệ quy:**
$$\begin{cases} T(1) = 1 \\ T(n) = 2T(n-1) + 1 & (n > 1) \end{cases}$$

---

### b. (1.5 điểm) Giải phương trình đệ quy bằng 2 phương pháp:

#### Phương pháp 1: Truy hồi thế ngược (Backward Substitution)
$$T(n) = 2T(n-1) + 1$$
$$= 2(2T(n-2) + 1) + 1 = 2^2 T(n-2) + 2 + 1$$
$$= 2^2(2T(n-3) + 1) + 2 + 1 = 2^3 T(n-3) + 2^2 + 2 + 1$$
$$\dots$$
$$= 2^{n-1} T(1) + \sum_{i=0}^{n-2} 2^i = 2^{n-1} \cdot 1 + (2^{n-1} - 1) = 2^n - 1$$
$\implies$ Độ phức tạp thời gian: **$O(2^n)$** (hoặc $\Theta(2^n)$).

#### Phương pháp 2: Hàm sinh (Generating Function)
- Đặt hàm sinh $G(x) = \sum_{n=1}^\infty T_n x^n$.
- Nhân 2 vế của $T_n - 2T_{n-1} = 1$ với $x^n$ và lấy tổng từ $n=2$ đến $\infty$:
  $$\sum_{n=2}^\infty T_n x^n - 2 \sum_{n=2}^\infty T_{n-1} x^n = \sum_{n=2}^\infty x^n$$
  $$(G(x) - T_1 x) - 2x G(x) = \frac{x^2}{1-x}$$
  Vì $T_1 = 1$:
  $$G(x)(1 - 2x) = x + \frac{x^2}{1-x} = \frac{x}{1-x} \implies G(x) = \frac{x}{(1-x)(1-2x)}$$
- Phân tích phân thức hữu tỉ:
  $$G(x) = \frac{1}{1-2x} - \frac{1}{1-x} = \sum_{n=0}^\infty (2^n - 1) x^n$$
- Hệ số của $x^n$ là: $T_n = 2^n - 1 \quad (\forall n \ge 1)$.
$\implies$ Độ phức tạp thời gian: **$O(2^n)$**.

---

## CÂU 3 (2.5 điểm) - ĐẶT DẤU NGOẶC BIỂU THỨC QUY HOẠCH ĐỘNG

Biểu thức: $A = 1 + 2 \times 3 + 4$ với $x_0=1, x_1=2, x_2=3, x_3=4$ và $o_0=+, o_1=\times, o_2=+$.

### a. Bảng tính Quy hoạch động $DP[i][j]$:

| | $j = 0$ | $j = 1$ | $j = 2$ | $j = 3$ |
| :---: | :---: | :---: | :---: | :---: |
| **$i = 0$** | **1** | **3** | **9** | **21** |
| **$i = 1$** | - | **2** | **6** | **14** |
| **$i = 2$** | - | - | **3** | **7** |
| **$i = 3$** | - | - | - | **4** |

- **Giá trị lớn nhất có thể đạt được:** $DP[0][3] = \mathbf{21}$.
- **Cách đặt dấu ngoặc tương ứng:** $((1 + 2) \times (3 + 4)) = 3 \times 7 = 21$.

### b. Xây dựng phương trình quy hoạch động & Minh họa cho $DP[1][3]$:
- Phương trình DP:
  $$DP[i][j] = \begin{cases} x_i & \text{khi } i = j \\ \max_{i \le k < j} \left\{ DP[i][k] \circ_k DP[k+1][j] \right\} & \text{khi } i < j \end{cases}$$
- Minh họa tính $DP[1][3]$ (đoạn $2 \times 3 + 4$):
  - $k = 1$: $DP[1][1] \times DP[2][3] = 2 \times 7 = 14$
  - $k = 2$: $DP[1][2] + DP[3][3] = 6 + 4 = 10$
  $\implies DP[1][3] = \max(14, 10) = 14$ (với $k = 1$).

### c. Ý tưởng truy xuất lời giải tối ưu:
- **Xác định giá trị lớn nhất:** Tra ô $DP[0][n]$.
- **Truy vết dấu ngoặc:** Lưu vết $trace[i][j] = k$ tại điểm chia tối ưu. Dùng hàm đệ quy `Print_Parens(trace, i, j)` in dấu mở ngoặc `(`, gọi đệ quy nửa trái `(i, k)`, in toán tử $o_k$, gọi đệ quy nửa phải `(k+1, j)`, và in dấu đóng ngoặc `)`.

---

# PHẦN 2: TỰ CHỌN (2.5 điểm)

---

## CÂU 4 (2.5 điểm) - LIỆT KÊ HOÁN VỊ

### 1. Phương pháp Quay lui (Backtracking):
- Mã giả sử dụng mảng $X[1..n]$ và mảng đánh dấu $used[1..n]$:
  ```text
  Thuật toán Backtrack_Perm(k, n, a, X, used):
  1. Cho i từ 1 đến n:
  2.    Nếu used[i] == False thì:
  3.        X[k] = a[i]; used[i] = True
  4.        Nếu k == n thì: In X[1..n]
  5.        Ngược lại: Backtrack_Perm(k + 1, n, a, X, used)
  6.        used[i] = False
  ```
- Độ phức tạp thời gian: $O(n \cdot n!)$. Độ phức tạp không gian: $O(n)$.

### 2. Phương pháp Giảm để trị (Decrease-and-Conquer):
- Mã giả chèn phần tử $a_n$ vào mọi vị trí có thể của các hoán vị kích thước $n-1$:
  ```text
  Thuật toán Gen_Perm_Decrease(a, n):
  1. Nếu n == 1 thì trả về [[a[1]]]
  2. L_prev = Gen_Perm_Decrease(a, n - 1)
  3. Khởi tạo L_res = []
  4. Với mỗi P trong L_prev:
  5.    Với mỗi vị trí pos từ 0 đến length(P):
  6.        new_P = chèn a[n] vào vị trí pos của P
  7.        Thêm new_P vào L_res
  8. Trả về L_res
  ```
- Độ phức tạp thời gian: $O(n \cdot n!)$. Độ phức tạp không gian: $O(n \cdot n!)$.

### 3. So sánh độ phức tạp:
- Cả hai đều có độ phức tạp thời gian là $\Theta(n \cdot n!)$.
- Phương pháp Quay lui tối ưu không gian hơn vượt trội ($O(n)$ so với $O(n \cdot n!)$ của Giảm để trị).

---

## CÂU 5 (2.5 điểm) - BÀI TOÁN MÃ ĐI TUẦN (KNIGHT'S TOUR)

1. **Mô hình hóa:** Bàn cờ $n \times n$. Quân mã tại $(x, y)$ có tối đa 8 nước đi hợp lệ: $(x \pm 1, y \pm 2)$ và $(x \pm 2, y \pm 1)$ với điều kiện $1 \le u, v \le n$ và ô $(u, v)$ chưa được ghé thăm.
2. **Cấu trúc dữ liệu:** Ma trận $Board[1..n][1..n]$ khởi tạo bằng 0; $Board[x_0][y_0] = 1$; 2 mảng hướng $dx = [2, 1, -1, -2, -2, -1, 1, 2]$ và $dy = [1, 2, 2, 1, -1, -2, -2, -1]$.
3. **Thuật toán Quay lui:**
   ```text
   Thuật toán KnightTour(x, y, step, n, Board):
   1. Nếu step == n * n thì: In Board[1..n][1..n]; Trả về
   2. Cho i từ 1 đến 8:
   3.    u = x + dx[i]; v = y + dy[i]
   4.    Nếu IsValid(u, v, n, Board) thì:
   5.        Board[u][v] = step + 1
   6.        KnightTour(u, v, step + 1, n, Board)
   7.        Board[u][v] = 0   // Quay lui
   ```
4. **Độ phức tạp:** Thời gian $O(8^{n^2})$, không gian $O(n^2)$.

---

## CÂU 6 (2.5 điểm) - BA LÔ PHÂN SỐ (FRACTIONAL KNAPSACK)

### a. Mô hình hóa & Thiết kế thuật toán Tham lam:
- **Mô hình hóa:** $\max \sum_{i=1}^n p_i x_i$ thỏa $\sum_{i=1}^n w_i x_i \le M$ và $0 \le x_i \le 1$.
- **Chiến lược Tham lam:** Tính đơn giá $v_i = \frac{p_i}{w_i}$, sắp xếp giảm dần theo $v_i$, ưu tiên chọn đầy đủ các món đồ vật có $v_i$ cao nhất cho đến khi ba lô đầy.

### b. Áp dụng cho dữ liệu: $n = 3, M = 20\text{ kg}$, $w = (18, 15, 10), p = (25, 24, 15)$
1. **Tính đơn giá $v_i$:**
   - $v_1 = \frac{25}{18} \approx 1.389$
   - $v_2 = \frac{24}{15} = 1.600$
   - $v_3 = \frac{15}{10} = 1.500$
2. **Sắp xếp theo đơn giá giảm dần:** Đồ vật 2 ($1.60$) $\rightarrow$ Đồ vật 3 ($1.50$) $\rightarrow$ Đồ vật 1 ($1.39$).
3. **Các bước chọn:**
   - Chọn Đồ vật 2: Lấy $x_2 = 1.0 \implies$ Trọng lượng $= 15\text{ kg}$, Giá trị $= 24$, Sức chứa còn $= 20 - 15 = 5\text{ kg}$.
   - Chọn Đồ vật 3: Do $w_3 = 10 > 5$, lấy $x_3 = \frac{5}{10} = 0.5 \implies$ Trọng lượng lấy thêm $= 5\text{ kg}$, Giá trị thêm $= 15 \times 0.5 = 7.5$, Sức chứa còn $= 0$.
   - Đồ vật 1: $x_1 = 0$.
4. **Kết quả:**
   - Vectơ nghiệm: $X = (x_1, x_2, x_3) = (0, 1, 0.5)$.
   - Tổng trọng lượng: $15 + 5 = 20\text{ kg}$.
   - Tổng giá trị lớn nhất: $P_{max} = 24 + 7.5 = \mathbf{31.5}$.
