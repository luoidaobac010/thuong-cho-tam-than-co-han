# ĐÁP ÁN & LỜI GIẢI CHI TIẾT - ĐỀ THI MẪU SỐ 02
## MÔN: CS112 - PHÂN TÍCH VÀ THIẾT KẾ THUẬT TOÁN (CS112)
### THANG ĐIỂM: 12.0 ĐIỂM (CHUẨN CÔ HUỲNH THỊ THANH THƯƠNG)

---

# PHẦN 1: CÂU TRẢ LỜI NGẮN (6.0 ĐIỂM)

## CÂU 1 (3.0 ĐIỂM) - KÝ HIỆU TIỆM CẬN

### a. Chứng minh theo định nghĩa (1.75 điểm):

- **Chứng minh 1 (0.75 điểm): $f(n) \in O(g(n)) \iff g(n) \in \Omega(f(n))$.**
  - **Chiều thuận ($\implies$):** Giả sử $f(n) \in O(g(n))$. Theo định nghĩa Big-O:
    $$\exists c \in \mathbb{R}^+, \exists n_0 \in \mathbb{N}, \forall n \ge n_0: 0 \le f(n) \le c \cdot g(n)$$
    Vì $c > 0$, nhân hai vế với $\frac{1}{c} > 0$:
    $$0 \le \frac{1}{c} \cdot f(n) \le g(n) \quad (\forall n \ge n_0)$$
    Chọn hằng số $c' = \frac{1}{c} \in \mathbb{R}^+$ và giữ nguyên $n_0 \in \mathbb{N}$. Theo định nghĩa Big-Omega, suy ra $g(n) \in \Omega(f(n))$.
  - **Chiều đảo ($\impliedby$):** Giả sử $g(n) \in \Omega(f(n))$. Theo định nghĩa Big-Omega:
    $$\exists c_1 \in \mathbb{R}^+, \exists n_1 \in \mathbb{N}, \forall n \ge n_1: 0 \le c_1 \cdot f(n) \le g(n)$$
    Vì $c_1 > 0$, suy ra $0 \le f(n) \le \frac{1}{c_1} \cdot g(n)$ ($\forall n \ge n_1$).
    Chọn $c_2 = \frac{1}{c_1} \in \mathbb{R}^+$ và $n_1 \in \mathbb{N}$. Theo định nghĩa Big-O, suy ra $f(n) \in O(g(n))$.
  - **Kết luận:** Hai mệnh đề tương đương (ĐPCM). *(0.75đ)*

- **Chứng minh 2 (1.00 điểm): $\log_2(n!) \in \Theta(n \log_2 n)$.**
  - Ta có $n! = 1 \cdot 2 \cdots n \le n^n$. Lấy logarit hai vế:
    $$\log_2(n!) \le \log_2(n^n) = n \log_2 n \quad (\forall n \ge 1)$$
  - Mặt khác: $n! \ge \lceil n/2 \rceil^{\lceil n/2 \rceil} \ge (n/2)^{n/2}$. Với mọi $n \ge 4$:
    $$\log_2(n!) \ge \frac{n}{2} \log_2\left(\frac{n}{2}\right) = \frac{n}{2}(\log_2 n - 1) \ge \frac{n}{2} \cdot \frac{1}{2}\log_2 n = \frac{1}{4} n \log_2 n$$
  - Chọn $c_1 = \frac{1}{4} \in \mathbb{R}^+, c_2 = 1 \in \mathbb{R}^+, n_0 = 4 \in \mathbb{N}$. Với mọi $n \ge n_0$, ta có:
    $$0 \le c_1 \cdot n \log_2 n \le \log_2(n!) \le c_2 \cdot n \log_2 n$$
  - Theo định nghĩa $\Theta$, suy ra $\log_2(n!) \in \Theta(n \log_2 n)$ (ĐPCM). *(1.0đ)*

---

### b. Phân lớp và Sắp xếp Big-O (1.25 điểm):

| Hàm | Dạng biến đổi chuẩn | Big-O nhỏ nhất | Giải thích ngắn gọn cách xác định |
| :---: | :--- | :---: | :--- |
| $g_1(n) = 2^{3\log_2 n} + 100n^2$ | $2^{\log_2(n^3)} + 100n^2 = n^3 + 100n^2$ | $O(n^3)$ | Áp dụng công thức đổi cơ số $2^{\log_2 x} = x$, số hạng bậc cao nhất là $n^3$. |
| $g_2(n) = \sqrt{n \log_2 n}$ | $n^{1/2} (\log n)^{1/2}$ | $O(\sqrt{n \log n})$ | Lũy thừa bậc dưới tuyến tính $n^{0.5}$, tăng chậm nhất trong nhóm đa thức. |
| $g_3(n) = \sum_{i=1}^n i^2$ | $\frac{n(n+1)(2n+1)}{6} = \frac{2n^3+3n^2+n}{6}$ | $O(n^3)$ | Tổng bình phương $n$ số tự nhiên đầu tiên thành đa thức bậc 3. |
| $g_4(n) = 3^n$ | $3^n$ | $O(3^n)$ | Hàm mũ cơ số 3. |
| $g_5(n) = n^{\sqrt{n}}$ | $2^{\sqrt{n}\log_2 n}$ | $O(n^{\sqrt{n}})$ | Hàm siêu đa thức (lớn hơn mọi $n^k$, nhỏ hơn $a^n$). |
| $g_6(n) = \log_2(n^n)$ | $n \log_2 n$ | $O(n \log n)$ | Đưa số mũ ra ngoài logarit $\log(n^n) = n \log n$. |
| $g_7(n) = n!$ | $\approx \sqrt{2\pi n}(n/e)^n$ | $O(n!)$ | Hàm giai thừa tăng nhanh hơn mọi hàm mũ $a^n$. |

**Kết luận Thứ tự các hàm tăng dần (từ nhỏ đến lớn):**
$$g_2(n) < g_6(n) < g_1(n) = g_3(n) < g_5(n) < g_4(n) < g_7(n)$$

---

## CÂU 2 (3.0 ĐIỂM) - PHÂN TÍCH THUẬT TOÁN

### a. Phân tích thuật toán nhân hai ma trận (0.75 điểm):
1. **Chức năng:** Hàm tính ma trận tích $C = A \times B$ kích thước $n \times n$.
2. **Đếm phép toán và công thức $\sum$:**
   - Phép toán cơ bản là phép nhân `A[i][k] * B[k][j]`.
   - Tổng số phép nhân thực hiện là:
     $$C(n) = \sum_{i=0}^{n-1} \sum_{j=0}^{n-1} \sum_{k=0}^{n-1} 1 = n \cdot n \cdot n = n^3$$
   - Do đó, độ phức tạp thời gian của giải thuật là **$\Theta(n^3)$** (hoặc $O(n^3)$).

---

### b. Thành lập phương trình đệ quy Merge Sort (0.75 điểm):
- Để sắp xếp mảng $n$ phần tử, thuật toán chia đôi mảng thành 2 mảng con kích thước $n/2$, gọi đệ quy sắp xếp 2 nửa (mỗi nửa mất $T(n/2)$), sau đó trộn lại mất $n - 1$ phép so sánh.
- Điều kiện dừng khi mảng có 1 phần tử ($n=1$): Không cần so sánh nào $\implies T(1) = 0$.
- **Hệ thức đệ quy:**
  $$\begin{cases} T(1) = 0 \\ T(n) = 2T(n/2) + n - 1 & (n > 1) \end{cases}$$

---

### c. Giải phương trình đệ quy (1.5 điểm):

- **Giải Phương trình 1: $T(1)=0, T(n)=2T(n/2)+n$ với $n=2^k$ (Thế ngược):**
  - Đặt $n = 2^k \implies k = \log_2 n$.
  - $T(2^k) = 2T(2^{k-1}) + 2^k = 2(2T(2^{k-2}) + 2^{k-1}) + 2^k = 2^2 T(2^{k-2}) + 2 \cdot 2^k = \dots = 2^k T(1) + k \cdot 2^k$.
  - Vì $T(1) = 0 \implies T(n) = 2^k \cdot 0 + (\log_2 n) \cdot n = n \log_2 n \implies O(n \log n)$.

- **Giải Phương trình 2: $a_0=0, a_1=1, a_n - a_{n-1} - a_{n-2} = 0$ (PT đặc trưng):**
  - PT đặc trưng: $r^2 - r - 1 = 0 \implies r_{1,2} = \frac{1 \pm \sqrt{5}}{2}$.
  - Nghiệm tổng quát: $a_n = C_1 \left(\frac{1+\sqrt{5}}{2}\right)^n + C_2 \left(\frac{1-\sqrt{5}}{2}\right)^n$.
  - Thay điều kiện đầu: $a_0=0 \implies C_1+C_2=0$; $a_1=1 \implies C_1=\frac{1}{\sqrt{5}}, C_2=-\frac{1}{\sqrt{5}}$.
  - Vậy $a_n = \frac{1}{\sqrt{5}} \left[\left(\frac{1+\sqrt{5}}{2}\right)^n - \left(\frac{1-\sqrt{5}}{2}\right)^n\right] \implies O(1.618^n)$.

---

# PHẦN 2: TỰ LUẬN (6.0 ĐIỂM)

## CÂU 3 (2.0 ĐIỂM) - PHÂN TÍCH BÀI TOÁN BA LÔ PHÂN SỐ (GREEDY)
1. **Mô hình hóa:** $\max \sum_{i=1}^n p_i x_i$ với ràng buộc $\sum w_i x_i \le M$ và $0 \le x_i \le 1$.
2. **Chiến lược Tham lam:**
   - Tính tỷ số đơn giá $v_i = p_i / w_i$ cho từng đồ vật.
   - Sắp xếp các đồ vật theo $v_i$ giảm dần.
   - Lần lượt lấy tối đa từng đồ vật cho đến khi đầy ba lô.

---

## CÂU 4 (2.0 ĐIỂM) - THIẾT KẾ THUẬT TOÁN TÌM TỪ TRONG Ô CHỮ (WORD SEARCH)

### 1. Ý tưởng & Cấu trúc dữ liệu:
- Ma trận chữ cái $Board[0..M-1][0..N-1]$ và từ cần tìm $Word$.
- Tìm kiếm DFS đệ quy 4 hướng: $(r \pm 1, c), (r, c \pm 1)$.
- Đánh dấu ô đang xét bằng ký tự tạm `'#'`, hoàn tác trả lại ký tự cũ khi quay lui (Backtrack).

### 2. Mã giả chuẩn:
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
- **Độ phức tạp:** Thời gian $O(M \cdot N \cdot 4^L)$ ($L = \text{length}(Word)$), Không gian $O(L)$.

---

## CÂU 5 (2.0 ĐIỂM) - QUY HOẠCH ĐỘNG NHÂN CHUỖI MA TRẬN (MCM)

Dãy kích thước: $p = (10, 20, 5, 15, 30)$ ($n = 4$).

### 1. Phương trình Quy hoạch động:
$$m[i][j] = \begin{cases} 0 & \text{khi } i = j \\ \min_{i \le k < j} \{ m[i][k] + m[k+1][j] + p_{i-1} p_k p_j \} & \text{khi } i < j \end{cases}$$

### 2. Bảng chi phí $m[i][j]$ và Bảng vết $s[i][j]$:

**Bảng chi phí $m[i][j]$:**

| | $j = 1$ | $j = 2$ | $j = 3$ | $j = 4$ |
| :---: | :---: | :---: | :---: | :---: |
| **$i = 1$** | **0** | **1000** | **1750** | **4750** |
| **$i = 2$** | - | **0** | **1500** | **5250** |
| **$i = 3$** | - | - | **0** | **2250** |
| **$i = 4$** | - | - | - | **0** |

**Bảng lưu vết $s[i][j]$:**

| | $j = 1$ | $j = 2$ | $j = 3$ | $j = 4$ |
| :---: | :---: | :---: | :---: | :---: |
| **$i = 1$** | - | 1 | 2 | **2** |
| **$i = 2$** | - | - | 2 | 2 |
| **$i = 3$** | - | - | - | 3 |
| **$i = 4$** | - | - | - | - |

- **Số phép nhân vô hướng tối thiểu:** $m[1][4] = \mathbf{4750}$.
- **Cách đặt dấu ngoặc tối ưu:** $((A_1 A_2)(A_3 A_4))$.
