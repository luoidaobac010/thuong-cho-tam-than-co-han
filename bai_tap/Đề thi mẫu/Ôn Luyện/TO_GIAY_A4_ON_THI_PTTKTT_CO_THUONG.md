# TÀI LIỆU TỔNG HỢP TỜ GIẤY A4 (2 MẶT VIẾT TAY) MÔN PTTKTT (CS112)
## GIẢNG VIÊN: CÔ HUỲNH THỊ THANH THƯƠNG - TRƯỜNG ĐH CÔNG NGHỆ THÔNG TIN (UIT)

---

# ==========================================
# 📄 MẶT 1: KÝ HIỆU TIỆM CẬN & PHÂN TÍCH THUẬT TOÁN (PHẦN 1 - 6.0 ĐIỂM)
# ==========================================

## 1. ĐỊNH NGHĨA TOÁN HỌC & MẪU CHỨNG MINH CHUẨN CÔ THƯƠNG

### a. Ba Định nghĩa cơ bản (BẮT BUỘC ghi đầy đủ lượng từ):
- **Big-O ($O$):** $f(n) \in O(g(n)) \iff \exists c \in \mathbb{R}^+, \exists n_0 \in \mathbb{N}, \forall n \ge n_0: 0 \le f(n) \le c \cdot g(n)$.
- **Big-Omega ($\Omega$):** $f(n) \in \Omega(g(n)) \iff \exists c \in \mathbb{R}^+, \exists n_0 \in \mathbb{N}, \forall n \ge n_0: 0 \le c \cdot g(n) \le f(n)$.
- **Big-Theta ($\Theta$):** $f(n) \in \Theta(g(n)) \iff \exists c_1, c_2 \in \mathbb{R}^+, \exists n_0 \in \mathbb{N}, \forall n \ge n_0: 0 \le c_1 \cdot g(n) \le f(n) \le c_2 \cdot g(n)$.

---

### b. Mẫu chứng minh hai tập bằng nhau: $O(f(n)) = O(g(n))$ khi $g \in O(f) \land f \in O(g)$:
> ⚠️ **Câu thần chú bắt buộc:** Phải có chữ **"bất kỳ"** và chia **2 vế bao hàm** riêng biệt:
- **Vế 1: Chứng minh $O(f) \subseteq O(g)$:**
  - Vì $f \in O(g) \implies \exists c_1 \in \mathbb{R}^+, \exists n_1 \in \mathbb{N}, \forall n \ge n_1: 0 \le f(n) \le c_1 \cdot g(n)$.
  - Xét một hàm **bất kỳ** $h(n) \in O(f(n)) \implies \exists c_2 \in \mathbb{R}^+, \exists n_2 \in \mathbb{N}, \forall n \ge n_2: 0 \le h(n) \le c_2 \cdot f(n)$.
  - Với mọi $n \ge n_0 = \max(n_1, n_2)$, ta có: $0 \le h(n) \le c_2 \cdot (c_1 \cdot g(n)) = (c_1 c_2) \cdot g(n)$.
  - Chọn $c = c_1 c_2 \in \mathbb{R}^+, n_0 = \max(n_1, n_2) \in \mathbb{N}$. Theo định nghĩa $O$, suy ra $h(n) \in O(g(n))$.
  - Do $h(n)$ bất kỳ $\implies O(f(n)) \subseteq O(g(n)) \quad (1)$.
- **Vế 2: Chứng minh $O(g) \subseteq O(f)$:**
  - Chứng minh hoàn toàn tương tự: dùng $c_3, n_3$ và xét hàm **bất kỳ** $k(n) \in O(g(n))$ với $c_4, n_4 \implies O(g(n)) \subseteq O(f(n)) \quad (2)$.
- **Kết luận:** Từ (1) và (2) suy ra $O(f(n)) = O(g(n))$ (ĐPCM).

---

### c. Các bài toán chứng minh định nghĩa mẫu:
- **$f+g \in O(\max(f, g))$:** Ta có $f \le \max(f, g)$ và $g \le \max(f, g) \implies f+g \le 2\max(f, g)$. Chọn $c = 2, n_0 = 1$.
- **$(n+a)^b \in \Theta(n^b)$ ($b>0$):** Với $n \ge 2|a| \implies \frac{n}{2} \le n+a \le 2n \implies (1/2)^b n^b \le (n+a)^b \le 2^b n^b$. Chọn $c_1 = (1/2)^b, c_2 = 2^b, n_0 = \lceil 2|a| \rceil$.
- **$\log(n!) \in \Theta(n \log n)$:** $n! \le n^n \implies \log(n!) \le n \log n$. Với $n \ge 4 \implies n! \ge (n/2)^{n/2} \implies \log(n!) \ge \frac{1}{4} n \log n$. Chọn $c_1 = 1/4, c_2 = 1, n_0 = 4$.

---

## 2. CHUỖI PHÂN LỚP ĐỘ PHỨC TẠP TĂNG DẦN & CÔNG THỨC BIẾN ĐỔI

### Chuỗi chuẩn:
$$1 \prec \log \log n \prec \log n \prec \log^k n \prec \sqrt[c]{n} \prec n \prec n \log n \prec n^2 \prec n^k \prec a^{\sqrt{n}} \prec a^n \prec n! \prec n^n$$

### Công thức biến đổi đưa về dạng chuẩn:
- $a^{\log_b n} = n^{\log_b a}$ (Ví dụ: $4^{\log_2 n} = n^{\log_2 4} = n^2$).
- $\sqrt{a^b} = a^{b/2}$ (Ví dụ: $\sqrt{3^{\sqrt{n}}} = 3^{\frac{\sqrt{n}}{2}}$).
- $\sum_{i=1}^n i = \frac{n(n+1)}{2} = \Theta(n^2)$; $\quad \sum_{i=1}^n i^2 = \frac{n(n+1)(2n+1)}{6} = \Theta(n^3)$; $\quad \sum_{i=1}^n \sum_{j=1}^n (i \cdot j) = [\frac{n(n+1)}{2}]^2 = \Theta(n^4)$.

---

## 3. PHÂN TÍCH THUẬT TOÁN & GIẢI PHƯƠNG TRÌNH ĐỆ QUY

### a. Phân tích thuật toán lặp:
1. Nêu rõ chức năng của hàm (trả về cái gì).
2. Xác định phép toán cơ bản (so sánh / gán).
3. Lập tổng: $C(n) = \sum_{i=0}^{n-2} \sum_{j=i+1}^{n-1} 1 = \sum_{i=0}^{n-2} (n-1-i) = \frac{n(n-1)}{2} \implies O(n^2)$.

---

### b. Thành lập phương trình đệ quy Tháp Hà Nội:
- $T(1) = 1$ (chuyển 1 đĩa trực tiếp từ $A \rightarrow C$).
- $T(n) = 2T(n-1) + 1$ với $n > 1$ ($T(n-1)$ chuyển $n-1$ đĩa $A \rightarrow B$, $+1$ chuyển đĩa đáy $A \rightarrow C$, $T(n-1)$ chuyển $n-1$ đĩa $B \rightarrow C$).

---

### c. Bộ 3 Phương pháp giải phương trình đệ quy:
> 🚫 **Lưu ý:** Cô Thương **CẤM** dùng Master Theorem! Phải giải bằng 1 trong 3 cách sau:

1. **Phương pháp 1: Thế ngược (Backward Substitution):**
   $$T(n) = 2T(n-1) + 1 = 2^2 T(n-2) + 2 + 1 = \dots = 2^k T(n-k) + \sum_{i=0}^{k-1} 2^i$$
   Dừng khi $n-k=1 \implies k=n-1$:
   $$T(n) = 2^{n-1} T(1) + (2^{n-1} - 1) = 2^n - 1 \implies O(2^n)$$

2. **Phương pháp 2: Phương trình đặc trưng:**
   - PT thuần nhất: $r - 2 = 0 \implies r = 2 \implies T^{(h)}(n) = C \cdot 2^n$.
   - Nghiệm riêng: vế phải $f(n)=1 \implies T^{(p)}(n) = A \implies A - 2A = 1 \implies A = -1$.
   - Nghiệm tổng quát: $T(n) = C \cdot 2^n - 1$. Với $T(1) = 1 \implies C \cdot 2 - 1 = 1 \implies C = 1 \implies T(n) = 2^n - 1$.

3. **Phương pháp 3: Hàm sinh (Generating Function):**
   - Đặt $G(x) = \sum_{n=1}^\infty T_n x^n$.
   - Nhân $x^n$ vào $T_n - 2T_{n-1} = 1$ và lấy tổng $n \ge 2$:
     $$(G(x) - T_1 x) - 2x G(x) = \frac{x^2}{1-x} \implies G(x)(1-2x) = \frac{x}{1-x} \implies G(x) = \frac{x}{(1-x)(1-2x)}$$
   - Tách phân thức: $G(x) = \frac{1}{1-2x} - \frac{1}{1-x} = \sum_{n=0}^\infty (2^n - 1) x^n \implies T_n = 2^n - 1 \implies O(2^n)$.

---
---

# ==========================================
# 📄 MẶT 2: TỰ LUẬN - QUY HOẠCH ĐỘNG, THAM LAM, QUAY LUI (PHẦN 2 - 6.0 ĐIỂM)
# ==========================================

## 1. KHUNG 4 BƯỚC THIẾT KẾ QUY HOẠCH ĐỘNG (DP - TRỌNG TÂM 100% CÓ THI)

- **Bước 1 (Bài toán con & Bảng DP):** Định nghĩa ý nghĩa $DP[i][j]$ (hoặc $M[i]$) lưu đại lượng tối ưu gì.
- **Bước 2 (Công thức DP):** Nêu trường hợp cơ sở + công thức chuyển trạng thái.
- **Bước 3 (Điền bảng Bottom-Up):** Nêu thứ tự tính toán (theo đường chéo $L=j-i+1$, từ trái sang phải), điền bảng chi tiết.
- **Bước 4 (Truy vết tối ưu):** Dùng bảng lưu vết $trace[i][j] = k$ (hoặc $S[i]$) để đệ quy/lần ngược in nghiệm.

---

## 2. CÔNG THỨC 5 BÀI TOÁN QUY HOẠCH ĐỘNG KINH ĐIỂN CỦA CÔ THƯƠNG

### ① Đặt dấu ngoặc biểu thức số thực tối ưu ($x_0 o_0 x_1 \dots x_n$ với $+, \times$):
- $DP[i][i] = x_i$.
- $DP[i][j] = \max_{i \le k < j} \{ DP[i][k] \circ_k DP[k+1][j] \}$. Điền theo độ dài $L = 2, 3, \dots, n+1$.
- Bảng vết $trace[i][j] = k$. Giá trị lớn nhất: $DP[0][n]$.

### ② Dãy con tăng dài nhất (LIS - Buổi 8):
- $M[i]$: Độ dài dãy con tăng dài nhất kết thúc tại $a_i$. Cơ sở: $M[i] = 1, S[i] = -1$.
- Công thức: $M[i] = 1 + \max_{0 \le j < i, a_j < a_i} \{ M[j] \}$; Cập nhật $S[i] = j^*$.
- Kết quả bài toán gốc: $L_{max} = \max_{0 \le i < n} M[i]$ (Ô lớn nhất mảng $M$).

### ③ Nhân chuỗi ma trận (MCM - Matrix Chain Multiplication):
- $m[i][i] = 0$.
- $m[i][j] = \min_{i \le k < j} \{ m[i][k] + m[k+1][j] + p_{i-1} p_k p_j \}$. Bảng vết $s[i][j] = k$.
- Độ phức tạp: Thời gian $O(n^3)$, Không gian $O(n^2)$.

### ④ Tính tổ hợp $C_n^k$ / Tam giác Pascal (Bottom-Up):
- Cơ sở: $C[i][0] = 1$ và $C[i][i] = 1$.
- Công thức: $C[i][j] = C[i-1][j-1] + C[i-1][j]$ với $1 \le j < i$.

### ⑤ Bài toán Cái túi 0/1 (0/1 Knapsack):
- $DP[i][w] = \max(DP[i-1][w], DP[i-1][w - w_i] + v_i)$ khi $w_i \le w$; ngược lại bằng $DP[i-1][w]$.

---

## 3. THUẬT TOÁN THAM LAM (GREEDY) - BA LÔ PHÂN SỐ (FRACTIONAL KNAPSACK)

1. **Mô hình hóa:** $\max \sum p_i x_i$ thỏa $\sum w_i x_i \le M$ và $0 \le x_i \le 1$.
2. **Chiến lược:** Tính đơn giá $v_i = \frac{p_i}{w_i}$, sắp xếp giảm dần.
3. **Mã giả tham lam:**
   ```text
   Thuật toán Fractional_Knapsack(n, M, w, p):
   1. Tính v[i] = p[i] / w[i] cho mọi i = 1..n
   2. Sắp xếp đồ vật theo v[i] giảm dần; cap = M; max_p = 0
   3. Cho i từ 1 đến n:
   4.    Nếu cap == 0 thì dừng
   5.    Nếu w[i] <= cap thì:
   6.        x[i] = 1.0; cap = cap - w[i]; max_p += p[i]
   7.    Ngược lại:
   8.        x[i] = cap / w[i]; max_p += p[i] * x[i]; cap = 0
   9. Trả về (x, max_p)
   ```
4. **Độ phức tạp:** Thời gian $O(n \log n)$, Bộ nhớ $O(n)$.

---

## 4. THUẬT TOÁN QUAY LUI (BACKTRACKING) & GIẢM ĐỂ TRỊ

### a. Khung mã giả Quay lui chuẩn:
```text
Thuật toán Backtrack(k, n, State):
1. Cho mỗi giá trị v trong tập ứng viên S_k:
2.    Nếu IsValid(v, k, State) == True thì:
3.        Gán X[k] = v; Cập nhật State
4.        Nếu k == n thì: In nghiệm X[1..n]
5.        Ngược lại: Backtrack(k + 1, n, State)
6.        Hoàn tác State  // Quay lui (Backtrack)
```

### b. Các bài toán quay lui tiêu biểu:
- **Liệt kê hoán vị:** Dùng mảng $X[1..n]$ và `used[1..n]`. Độ phức tạp $O(n \cdot n!)$, Bộ nhớ $O(n)$. So với Giảm để trị (chèn $a_n$ vào mọi vị trí của $P_{n-1}$) tốn bộ nhớ $O(n \cdot n!)$.
- **Mã đi tuần (Knight's Tour):** $Board[1..n][1..n]$ khởi tạo 0, 8 hướng $dx = [2, 1, -1, -2, -2, -1, 1, 2], dy = [1, 2, 2, 1, -1, -2, -2, -1]$. Thử đi ô kế tiếp $Board[u][v] = step + 1$, hoàn tác $Board[u][v] = 0$. Tối ưu với Heuristic Warnsdorff (chọn ô có bậc đi tiếp nhỏ nhất).
- **N-Queens:** 3 mảng đánh dấu $col[j]$, $diag_1[i+j]$, $diag_2[i-j+n]$. Độ phức tạp $O(n!)$.
