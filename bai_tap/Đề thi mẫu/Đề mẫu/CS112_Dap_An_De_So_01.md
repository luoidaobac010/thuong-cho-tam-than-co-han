# ĐÁP ÁN & LỜI GIẢI CHI TIẾT - ĐỀ THI MẪU SỐ 01
## MÔN: CS112 - PHÂN TÍCH VÀ THIẾT KẾ THUẬT TOÁN (CS112)
### THANG ĐIỂM: 12.0 ĐIỂM (CHUẨN CÔ HUỲNH THỊ THANH THƯƠNG)

---

# PHẦN 1: CÂU TRẢ LỜI NGẮN (6.0 ĐIỂM)

## CÂU 1 (3.0 ĐIỂM) - KÝ HIỆU TIỆM CẬN

### a. Chứng minh theo định nghĩa (1.75 điểm):

- **Chứng minh 1 (0.75 điểm): Nếu $g(n) \in O(f(n))$ và $f(n) \in O(g(n))$ thì $O(f(n)) = O(g(n))$.**
  - **Vế 1: Chứng minh $O(f(n)) \subseteq O(g(n))$:**
    + Theo giả thiết $f(n) \in O(g(n))$, theo định nghĩa Big-O:
      $$\exists c_1 \in \mathbb{R}^+, \exists n_1 \in \mathbb{N}, \forall n \ge n_1: 0 \le f(n) \le c_1 \cdot g(n)$$
    + Xét một hàm **bất kỳ** $h(n) \in O(f(n))$, theo định nghĩa Big-O:
      $$\exists c_2 \in \mathbb{R}^+, \exists n_2 \in \mathbb{N}, \forall n \ge n_2: 0 \le h(n) \le c_2 \cdot f(n)$$
    + Với mọi $n \ge n_0 = \max(n_1, n_2)$, ta có:
      $$0 \le h(n) \le c_2 \cdot f(n) \le c_2 \cdot (c_1 \cdot g(n)) = (c_2 \cdot c_1) \cdot g(n)$$
    + Chọn $c = c_2 \cdot c_1 \in \mathbb{R}^+, n_0 = \max(n_1, n_2) \in \mathbb{N}$. Với mọi $n \ge n_0$, ta có $0 \le h(n) \le c \cdot g(n)$.
    + Suy ra $h(n) \in O(g(n))$. Vì $h(n)$ bất kỳ $\implies O(f(n)) \subseteq O(g(n)) \quad (1)$.
  - **Vế 2: Chứng minh $O(g(n)) \subseteq O(f(n))$:**
    + Hoàn toàn tương tự: dùng $c_3, n_3$ cho $g \in O(f)$ và xét hàm **bất kỳ** $k(n) \in O(g)$ với $c_4, n_4 \implies$ chọn $c' = c_4 \cdot c_3, n_0' = \max(n_3, n_4) \implies O(g(n)) \subseteq O(f(n)) \quad (2)$.
  - **Kết luận:** Từ $(1)$ và $(2)$ suy ra $O(f(n)) = O(g(n))$ (ĐPCM). *(0.75đ)*

- **Chứng minh 2 (1.00 điểm): $(n + a)^b \in \Theta(n^b)$ với $b > 0, a \in \mathbb{R}$.**
  - Xét $n \ge 2|a| > 0$, ta có: $n - |a| \le n + a \le n + |a|$.
  - Vì $|a| \le \frac{n}{2} \implies \frac{n}{2} \le n - |a| \le n + a \le n + \frac{n}{2} \le 2n$.
  - Do $b > 0$, lũy thừa bậc $b$ các vế:
    $$\left(\frac{1}{2}\right)^b \cdot n^b \le (n + a)^b \le 2^b \cdot n^b$$
  - Chọn $c_1 = \left(\frac{1}{2}\right)^b \in \mathbb{R}^+, c_2 = 2^b \in \mathbb{R}^+, n_0 = \max(1, \lceil 2|a| \rceil) \in \mathbb{N}$.
  - Với mọi $n \ge n_0$, ta có $0 \le c_1 \cdot n^b \le (n+a)^b \le c_2 \cdot n^b$.
  - Theo định nghĩa $\Theta$, suy ra $(n + a)^b \in \Theta(n^b)$ (ĐPCM). *(1.0đ)*

---

### b. Phân lớp và Sắp xếp Big-O (1.25 điểm):

| Hàm | Dạng biến đổi chuẩn | Big-O nhỏ nhất | Giải thích ngắn gọn cách xác định |
| :---: | :--- | :---: | :--- |
| $f_1(n) = 4^{\log_2 n} + \log_2 \log_2 n$ | $4^{\log_2 n} = n^{\log_2 4} = n^2 \implies n^2 + \log \log n$ | $O(n^2)$ | Áp dụng công thức đổi cơ số $a^{\log_b n} = n^{\log_b a}$, bậc cao nhất là $n^2$. |
| $f_2(n) = n \cdot \sqrt[3]{n}$ | $n \cdot n^{1/3} = n^{4/3} = n^{1.333}$ | $O(n^{4/3})$ | Tích hai lũy thừa cùng cơ số $n^{1+1/3} = n^{4/3}$. |
| $f_3(n) = \sum_{i=1}^n \sum_{j=1}^n (i \cdot j)$ | $\left(\sum_{i=1}^n i\right)\left(\sum_{j=1}^n j\right) = \left[\frac{n(n+1)}{2}\right]^2 = \frac{n^4+2n^3+n^2}{4}$ | $O(n^4)$ | Tách thành tích 2 cấp số cộng, số hạng cao nhất là $\frac{n^4}{4}$. |
| $f_4(n) = n \cdot (\log_2 n)^4$ | $n \cdot (\log n)^4$ | $O(n \log^4 n)$ | Đa thức bậc 1 nhân logarit bậc 4 (nhỏ hơn mọi $n^{1+\epsilon}$). |
| $f_5(n) = n^5 (\log_2 n)^2$ | $n^5 (\log n)^2$ | $O(n^5 \log^2 n)$ | Đa thức bậc 5 nhân logarit bậc 2. |
| $f_6(n) = \sqrt{3^{\sqrt{n}}}$ | $(3^{\sqrt{n}})^{1/2} = 3^{\frac{\sqrt{n}}{2}} = (\sqrt{3})^{\sqrt{n}}$ | $O(3^{\sqrt{n}/2})$ | Hàm mũ của căn bậc hai $\sqrt{n}$ (lớn hơn mọi $n^k$, nhỏ hơn $a^n$). |
| $f_7(n) = \sqrt{n} \cdot 3^{n/2}$ | $\sqrt{n} \cdot (\sqrt{3})^n$ | $O(\sqrt{n} \cdot 3^{n/2})$ | Hàm mũ thực sự theo số mũ bậc nhất $n/2$, tăng nhanh nhất. |

**Kết luận Thứ tự các hàm theo thứ tự tăng dần (từ nhỏ đến lớn):**
$$f_4(n) < f_2(n) < f_1(n) < f_3(n) < f_5(n) < f_6(n) < f_7(n)$$

---

## CÂU 2 (3.0 ĐIỂM) - PHÂN TÍCH THUẬT TOÁN

### a. Phân tích thuật toán lặp (0.75 điểm):
1. **Chức năng:** Hàm trả về số lượng các cặp phần tử trùng nhau $(a[i], a[j])$ với $0 \le i < j < n$ trong mảng $a$.
2. **Đếm phép toán và công thức $\sum$:**
   - Phép toán cơ bản là phép so sánh `a[i] == a[j]`.
   - Tổng số phép so sánh là:
     $$C(n) = \sum_{i=0}^{n-2} \sum_{j=i+1}^{n-1} 1 = \sum_{i=0}^{n-2} (n - 1 - i) = \sum_{k=1}^{n-1} k = \frac{n(n-1)}{2} = \frac{n^2 - n}{2}$$
   - Số hạng bậc cao nhất là $n^2 \implies$ Độ phức tạp thời gian: **$O(n^2)$** (hoặc $\Theta(n^2)$).

---

### b. Thành lập phương trình đệ quy Tháp Hà Nội (0.75 điểm):
- Gọi $T(n)$ là số thao tác chuyển đĩa `transfer` để chuyển $n$ đĩa từ cột $A$ sang $C$.
- Khi $n = 1$: Thuật toán gọi trực tiếp `transfer(A, C)` đúng 1 lần $\implies T(1) = 1$.
- Khi $n > 1$: Thuật toán thực hiện 3 bước:
  1. `Hanoi(n-1, A, C, B)`: Cần $T(n-1)$ lần chuyển.
  2. `transfer(A, C)`: Đúng 1 lần chuyển.
  3. `Hanoi(n-1, B, A, C)`: Cần $T(n-1)$ lần chuyển.
  $\implies T(n) = T(n-1) + 1 + T(n-1) = 2T(n-1) + 1$.
- **Hệ thức đệ quy:**
  $$\begin{cases} T(1) = 1 \\ T(n) = 2T(n-1) + 1 & (n > 1) \end{cases}$$

---

### c. Giải phương trình đệ quy (1.5 điểm):

- **Cách 1: Phương pháp Thế ngược (Backward Substitution):**
  $$T(n) = 2T(n-1) + 1 = 2(2T(n-2) + 1) + 1 = 2^2 T(n-2) + 2 + 1 = \dots = 2^k T(n-k) + \sum_{i=0}^{k-1} 2^i$$
  Tại điều kiện dừng $n - k = 1 \implies k = n - 1$:
  $$T(n) = 2^{n-1} T(1) + \sum_{i=0}^{n-2} 2^i = 2^{n-1} \cdot 1 + (2^{n-1} - 1) = 2^n - 1 \implies O(2^n)$$

- **Cách 2: Phương pháp Phương trình đặc trưng:**
  - PT thuần nhất $r - 2 = 0 \implies r = 2 \implies T^{(h)}(n) = C \cdot 2^n$.
  - Nghiệm riêng $T^{(p)}(n) = A \implies A - 2A = 1 \implies A = -1$.
  - Nghiệm tổng quát $T(n) = C \cdot 2^n - 1$. Với $T(1) = 1 \implies 2C - 1 = 1 \implies C = 1 \implies T(n) = 2^n - 1 \implies O(2^n)$.

- **Cách 3: Phương pháp Hàm sinh (Generating Functions):**
  - Đặt $G(x) = \sum_{n=1}^\infty T_n x^n$. Nhân $x^n$ vào $T_n - 2T_{n-1} = 1$ và lấy tổng $\sum_{n=2}^\infty$:
    $$(G(x) - T_1 x) - 2x G(x) = \frac{x^2}{1-x} \implies G(x)(1-2x) = \frac{x}{1-x} \implies G(x) = \frac{x}{(1-x)(1-2x)}$$
  - Phân tích: $G(x) = \frac{1}{1-2x} - \frac{1}{1-x} = \sum_{n=0}^\infty (2^n - 1)x^n \implies T_n = 2^n - 1 \implies O(2^n)$.

---

# PHẦN 2: TỰ LUẬN (6.0 ĐIỂM)

## CÂU 3 (2.0 ĐIỂM) - PHÂN TÍCH BÀI TOÁN

### Lời giải Bài toán 3.1: Khôi phục địa chỉ IP
1. **Xác định Input/Output:**
   - Input: Chuỗi ký tự số $S$ có độ dài $4 \le \text{length}(S) \le 12$.
   - Output: Danh sách tất cả các địa chỉ IPv4 hợp lệ có dạng $A.B.C.D$.
   - Ví dụ: $S = "25525511135" \implies ["255.255.11.135", "255.255.111.35"]$.
2. **Ý tưởng giải & Chiến lược Quay lui (Backtracking):**
   - Ta cần chèn 3 dấu chấm để chia chuỗi $S$ thành 4 đoạn (octet).
   - Tại mỗi đoạn $part \in \{1, 2, 3, 4\}$, ta thử lấy độ dài $len \in \{1, 2, 3\}$.
   - Kiểm tra tính hợp lệ của đoạn: Giá trị nguyên nằm trong $[0, 255]$ và không có số 0 ở đầu nếu $len > 1$.
   - Khi đã đủ 4 đoạn và duyệt hết toàn bộ ký tự của $S$, ghi nhận địa chỉ IP.

---

## CÂU 4 (2.0 ĐIỂM) - THIẾT KẾ THUẬT TOÁN LIỆT KÊ HOÁN VỊ

### 1. Ý tưởng & Cấu trúc dữ liệu:
- Mảng $X[1..n]$ lưu hoán vị đang xây dựng.
- Mảng boolean $used[1..n]$ khởi tạo `False` để đánh dấu phần tử $a[i]$ đã chọn hay chưa.
- Xây dựng từng vị trí $k$ từ $1$ đến $n$. Khi $k = n$, in hoán vị $X$. Khi quay lui, trả `used[i] = False`.

### 2. Mã giả chuẩn:
```text
Thuật toán Backtrack_Perm(k, n, a, X, used):
1.  Cho i chạy từ 1 đến n thực hiện:
2.      Nếu used[i] == False thì:
3.          X[k] = a[i]
4.          used[i] = True
5.          Nếu k == n thì:
6.              In mảng X[1..n]
7.          Ngược lại:
8.              Backtrack_Perm(k + 1, n, a, X, used)
9.          used[i] = False                     // Quay lui (Backtrack)
```

### 3. Đánh giá độ phức tạp:
- Cây trạng thái có $n!$ lá, mỗi lá in mảng mất $O(n) \implies$ Thời gian: **$\Theta(n \cdot n!)$**.
- Bộ nhớ: Mảng $X$, `used` và ngăn xếp đệ quy sâu tối đa $n \implies$ Không gian: **$O(n)$**.

---

## CÂU 5 (2.0 ĐIỂM) - QUY HOẠCH ĐỘNG DÃY CON TĂNG DÀI NHẤT (LIS)

### 1. Ý nghĩa mảng DP & Bảng vết:
- $M[i]$: Độ dài của dãy con tăng dài nhất kết thúc tại phần tử $A[i]$.
- $S[i]$: Chỉ số của phần tử đứng ngay trước $A[i]$ trong dãy con tăng tối ưu kết thúc tại $A[i]$ ($S[i] = -1$ nếu $A[i]$ là phần tử đầu).

### 2. Phương trình Quy hoạch động:
- **Cơ sở:** $M[i] = 1, S[i] = -1 \quad (\forall 0 \le i < n)$.
- **Công thức chuyển trạng thái:**
  $$M[i] = 1 + \max_{\substack{0 \le j < i \\ A[j] < A[i]}} \{ M[j] \}$$
  Cập nhật $S[i] = j^*$ với $j^*$ là chỉ số đạt giá trị $M[j]$ lớn nhất.

### 3. Minh họa tính toán trên mảng $A = [5, 1, 3, 9, 10, 2, 6]$ ($n = 7$):

| Chỉ số $i$ | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ | $6$ |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Giá trị $A[i]$** | **5** | **1** | **3** | **9** | **10** | **2** | **6** |
| **Mảng $M[i]$** | **1** | **1** | **2** | **3** | **4** | **2** | **3** |
| **Mảng vết $S[i]$** | **-1** | **-1** | **1** | **2** | **3** | **1** | **2** |

- **Kết quả bài toán gốc:** $L_{max} = \max_{0 \le i < 7} M[i] = M[4] = \mathbf{4}$.
- **Truy vết tìm dãy con:** $i = 4$ ($A[4]=10$) $\rightarrow S[4]=3$ ($A[3]=9$) $\rightarrow S[3]=2$ ($A[2]=3$) $\rightarrow S[2]=1$ ($A[1]=1$) $\rightarrow S[1]=-1$ (Dừng).
- **Dãy con tăng dài nhất là:** **$[1, 3, 9, 10]$** với độ dài là **4**.
