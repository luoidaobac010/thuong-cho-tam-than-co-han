# ĐÁP ÁN & LỜI GIẢI CHI TIẾT - ĐỀ THI MẪU SỐ 03
## MÔN: CS112 - PHÂN TÍCH VÀ THIẾT KẾ THUẬT TOÁN (CS112)
### THANG ĐIỂM: 12.0 ĐIỂM (CHUẨN CÔ HUỲNH THỊ THANH THƯƠNG)

---

# PHẦN 1: CÂU TRẢ LỜI NGẮN (6.0 ĐIỂM)

## CÂU 1 (3.0 ĐIỂM) - KÝ HIỆU TIỆM CẬN

### a. Chứng minh theo định nghĩa (1.75 điểm):

- **Chứng minh 1 (0.75 điểm): Tính chất bắc cầu của Big-O.**
  - Giả thiết cho $f(n) \in O(g(n))$, theo định nghĩa:
    $$\exists c_1 \in \mathbb{R}^+, \exists n_1 \in \mathbb{N}, \forall n \ge n_1: 0 \le f(n) \le c_1 \cdot g(n)$$
  - Giả thiết cho $g(n) \in O(h(n))$, theo định nghĩa:
    $$\exists c_2 \in \mathbb{R}^+, \exists n_2 \in \mathbb{N}, \forall n \ge n_2: 0 \le g(n) \le c_2 \cdot h(n)$$
  - Với mọi $n \ge n_0 = \max(n_1, n_2)$, ta có:
    $$0 \le f(n) \le c_1 \cdot g(n) \le c_1 \cdot (c_2 \cdot h(n)) = (c_1 c_2) \cdot h(n)$$
  - Chọn $c = c_1 c_2 \in \mathbb{R}^+$ và $n_0 = \max(n_1, n_2) \in \mathbb{N}$. Với mọi $n \ge n_0$, ta có $0 \le f(n) \le c \cdot h(n)$.
  - Theo định nghĩa Big-O, suy ra $f(n) \in O(h(n))$ (ĐPCM). *(0.75đ)*

- **Chứng minh 2 (1.00 điểm): $2^{n+1} \in O(2^n)$ nhưng $2^{2n} \notin O(2^n)$.**
  - **Vế 1:** Ta có $2^{n+1} = 2 \cdot 2^n$. Chọn $c = 2 \in \mathbb{R}^+, n_0 = 1 \in \mathbb{N}$. Với mọi $n \ge 1$, ta có $0 \le 2^{n+1} \le 2 \cdot 2^n \implies 2^{n+1} \in O(2^n)$.
  - **Vế 2 (Chứng minh phản chứng):**
    - Giả sử ngược lại $2^{2n} \in O(2^n)$. Theo định nghĩa:
      $$\exists c > 0, \exists n_0 \in \mathbb{N}, \forall n \ge n_0: 0 \le 2^{2n} \le c \cdot 2^n$$
    - Chia hai vế cho $2^n > 0$, ta được: $2^n \le c$ với mọi $n \ge n_0$.
    - Điều này mâu thuẫn vì hàm $2^n$ tiến đến vô cùng khi $n \to \infty$, không thể bị chặn trên bởi một hằng số $c$ cố định.
    - Do đó, giả thiết phản chứng là sai. Vậy $2^{2n} \notin O(2^n)$ (ĐPCM). *(1.0đ)*

---

### b. Phân lớp và Sắp xếp Big-O (1.25 điểm):

| Hàm | Dạng biến đổi chuẩn | Big-O nhỏ nhất | Giải thích ngắn gọn cách xác định |
| :---: | :--- | :---: | :--- |
| $h_1(n) = 3^{\log_2 n}$ | $n^{\log_2 3} \approx n^{1.585}$ | $O(n^{\log_2 3})$ | Áp dụng công thức đổi cơ số $a^{\log_b n} = n^{\log_b a}$. |
| $h_2(n) = \sqrt{2^{\sqrt{n}}}$ | $2^{\frac{\sqrt{n}}{2}} = (\sqrt{2})^{\sqrt{n}}$ | $O(2^{\sqrt{n}/2})$ | Hàm mũ của căn bậc hai $\sqrt{n}$ (lớn hơn mọi $n^k$, nhỏ hơn $a^n$). |
| $h_3(n) = n^2 \log_2 n$ | $n^2 \log n$ | $O(n^2 \log n)$ | Đa thức bậc 2 nhân logarit. |
| $h_4(n) = 2^{2n}$ | $(2^2)^n = 4^n$ | $O(4^n)$ | Hàm mũ cơ số 4, tăng nhanh hơn $2^n$. |
| $h_5(n) = \log_2(\log_2 n)$ | $\log \log n$ | $O(\log \log n)$ | Hàm logarit lặp, tăng chậm nhất. |
| $h_6(n) = \sum_{i=1}^n i$ | $\frac{n(n+1)}{2} = \frac{n^2+n}{2}$ | $O(n^2)$ | Tổng cấp số cộng thành đa thức bậc 2. |
| $h_7(n) = 2^n$ | $2^n$ | $O(2^n)$ | Hàm mũ cơ số 2. |

**Kết luận Thứ tự các hàm tăng dần (từ nhỏ đến lớn):**
$$h_5(n) < h_1(n) < h_6(n) < h_3(n) < h_2(n) < h_7(n) < h_4(n)$$

---

## CÂU 2 (3.0 ĐIỂM) - PHÂN TÍCH THUẬT TOÁN

### a. Phân tích thuật toán Binary Search (0.75 điểm):
1. **Chức năng:** Tìm vị trí xuất hiện của giá trị $x$ trong mảng đã sắp xếp $a$. Trả về chỉ số tìm thấy hoặc $-1$ nếu không tìm thấy.
2. **Đếm phép toán và độ phức tạp:**
   - Tại mỗi bước lặp, không gian tìm kiếm giảm đi một nửa: $n \rightarrow n/2 \rightarrow n/4 \dots$
   - Số bước lặp tối đa trong trường hợp xấu nhất là $\lfloor \log_2 n \rfloor + 1$.
   - Mỗi bước lặp thực hiện $O(1)$ phép so sánh.
   - Do đó, độ phức tạp thời gian trường hợp xấu nhất là **$O(\log n)$** (hoặc $\Theta(\log n)$).

---

### b. Phương trình đệ quy QuickSort (0.75 điểm):
- **Trường hợp tốt nhất:** Phần tử chốt luôn chia đôi mảng thành 2 nửa bằng nhau:
  $$T(n) = 2T(n/2) + O(n) \implies O(n \log n)$$
- **Trường hợp xấu nhất:** Phần tử chốt luôn là phần tử nhỏ nhất hoặc lớn nhất (chia thành 0 và $n-1$ phần tử):
  $$T(n) = T(n-1) + O(n) \implies O(n^2)$$

---

### c. Giải phương trình đệ quy (1.5 điểm):

- **Giải PT 2: $a_0=1, a_1=4, a_n - 5a_{n-1} + 6a_{n-2} = 0$ (PT đặc trưng):**
  - PT đặc trưng: $r^2 - 5r + 6 = 0 \implies (r-2)(r-3) = 0 \implies r_1 = 2, r_2 = 3$.
  - Nghiệm tổng quát: $a_n = C_1 2^n + C_2 3^n$.
  - Thay $a_0 = 1 \implies C_1 + C_2 = 1$.
  - Thay $a_1 = 4 \implies 2C_1 + 3C_2 = 4 \implies C_1 = -1, C_2 = 2$.
  - Nghiệm chính xác: $a_n = -2^n + 2 \cdot 3^n \implies O(3^n)$.

---

# PHẦN 2: TỰ LUẬN (6.0 ĐIỂM)

## CÂU 3 (2.0 ĐIỂM) - PHÂN TÍCH BÀI TOÁN TÍNH ĐIỂM MÔN HỌC (WECODE)
1. **Input:** $n$ cột điểm, mảng trọng số $w_1 \dots w_n$, điểm mục tiêu $I_{target}$.
2. **Output:** Tất cả bộ điểm $(S_1 \dots S_n)$ có điểm trung bình làm tròn bằng $I_{target}$.
3. **Chiến lược:** Quy đổi nhân 400 để thành số nguyên $\text{min\_T} \le \sum V_i w_i \le \text{max\_T}$. Dùng Quay lui kết hợp Nhánh cận $rem\_max, rem\_min$ để cắt tỉa các nhánh không thể đạt mục tiêu.

---

## CÂU 4 (2.0 ĐIỂM) - THIẾT KẾ THUẬT TOÁN MÃ ĐI TUẦN (KNIGHT'S TOUR)

```text
Thuật toán KnightTour(x, y, step, n, Board):
1.  Nếu step == n * n thì:
2.      In ma trận Board[1..n][1..n]
3.      Trả về
4.  Cho i chạy từ 1 đến 8 thực hiện:
5.      u = x + dx[i]; v = y + dy[i]
6.      Nếu (1 <= u <= n) và (1 <= v <= n) và (Board[u][v] == 0) thì:
7.          Board[u][v] = step + 1
8.          KnightTour(u, v, step + 1, n, Board)
9.          Board[u][v] = 0                     // Quay lui (Backtrack)
```
- Heuristic Warnsdorff: Sắp xếp các ô kế tiếp $(u, v)$ theo số nước đi tiếp theo tăng dần để ưu tiên đi vào góc/rìa trước.

---

## CÂU 5 (2.0 ĐIỂM) - QUY HOẠCH ĐỘNG BÀI TOÁN CÁI TÚI 0/1 (0/1 KNAPSACK)

### 1. Phương trình Quy hoạch động:
- $DP[i][w]$: Giá trị lớn nhất khi xét $i$ đồ vật đầu tiên với sức chứa $w$.
$$DP[i][w] = \begin{cases} DP[i-1][w] & \text{khi } w_i > w \\ \max(DP[i-1][w], DP[i-1][w - w_i] + v_i) & \text{khi } w_i \le w \end{cases}$$

### 2. Bảng Quy hoạch động $DP[i][w]$ ($0 \le i \le 4, 0 \le w \le 10$):

| $i \backslash w$ | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ | $6$ | $7$ | $8$ | $9$ | $10$ |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **$i = 0$** | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** |
| **$i = 1$ ($w_1=2, v_1=3$)** | **0** | **0** | **3** | **3** | **3** | **3** | **3** | **3** | **3** | **3** | **3** |
| **$i = 2$ ($w_2=3, v_2=4$)** | **0** | **0** | **3** | **4** | **4** | **7** | **7** | **7** | **7** | **7** | **7** |
| **$i = 3$ ($w_3=4, v_3=5$)** | **0** | **0** | **3** | **4** | **5** | **7** | **8** | **9** | **9** | **12** | **12** |
| **$i = 4$ ($w_4=5, v_4=8$)** | **0** | **0** | **3** | **4** | **5** | **8** | **8** | **11** | **12** | **13** | **15** |

### 3. Kết luận & Truy vết:
- **Tổng giá trị lớn nhất đạt được:** $DP[4][10] = \mathbf{15}$.
- **Truy vết đồ vật chọn:**
  - $DP[4][10]=15 \ne DP[3][10]=12 \implies$ Chọn Đồ vật 4 ($w_4=5, v_4=8$). Sức chứa còn $10-5=5$.
  - $DP[3][5]=7 == DP[2][5]=7 \implies$ Không chọn Đồ vật 3. Sức chứa còn 5.
  - $DP[2][5]=7 \ne DP[1][5]=3 \implies$ Chọn Đồ vật 2 ($w_2=3, v_2=4$). Sức chứa còn $5-3=2$.
  - $DP[1][2]=3 \ne DP[0][2]=0 \implies$ Chọn Đồ vật 1 ($w_1=2, v_1=3$). Sức chứa còn $2-2=0$.
- **Các đồ vật được chọn vào ba lô:** **Đồ vật 1, Đồ vật 2, Đồ vật 4** (Tổng trọng lượng $2+3+5=10\text{ kg}$, Tổng giá trị $3+4+8 = 15$).
