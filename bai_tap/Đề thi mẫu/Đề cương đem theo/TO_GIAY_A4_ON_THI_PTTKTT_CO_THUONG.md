# TÀI LIỆU TỔNG HỢP TỜ GIẤY A4 (2 MẶT VIẾT TAY) MÔN PTTKTT (CS112)
## GIẢNG VIÊN: CÔ HUỲNH THỊ THANH THƯƠNG - TRƯỜNG ĐH CÔNG NGHỆ THÔNG TIN (UIT)

> Cập nhật 27/9/2026 theo buổi ôn cuối (buổi 10). Nội dung giống bản `.tex` và `.pdf` cùng tên. Đề ghi tổng 13 điểm: phân tích 6, thiết kế 7. Cô dặn chỉ chép công thức, không chép lời giải vì đề luôn đổi số.

---

# ==========================================
# 📄 MẶT 1: KÝ HIỆU TIỆM CẬN & PHÂN TÍCH THUẬT TOÁN (PHẦN 1 - 6 ĐIỂM)
# ==========================================

## 1. ĐỊNH NGHĨA TOÁN HỌC KÝ HIỆU TIỆM CẬN

> ⚠️ Ghi đủ lượng từ ($\exists, \forall, \in \mathbb{R}^+, \in \mathbb{N}$), luôn viết $T(n), g(n)$. Suy ra từ định nghĩa mà thiếu cụm $\exists c, \exists n_0, \forall n \ge n_0$ (vd $T(n) \in O(g(n)) \implies T(n) \le c \cdot g(n)$) là 0 điểm cả câu.

- **Big-O ($O$):** $f(n) \in O(g(n)) \iff \exists c \in \mathbb{R}^+, \exists n_0 \in \mathbb{N}, \forall n \ge n_0: 0 \le f(n) \le c \cdot g(n)$.
- **Big-Omega ($\Omega$):** $f(n) \in \Omega(g(n)) \iff \exists c \in \mathbb{R}^+, \exists n_0 \in \mathbb{N}, \forall n \ge n_0: 0 \le c \cdot g(n) \le f(n)$.
- **Big-Theta ($\Theta$):** $f(n) \in \Theta(g(n)) \iff \exists c_1, c_2 \in \mathbb{R}^+, \exists n_0 \in \mathbb{N}, \forall n \ge n_0: 0 \le c_1 \cdot g(n) \le f(n) \le c_2 \cdot g(n)$.

## 2. MẪU CHỨNG MINH TẬP BẰNG NHAU $O(f) = O(g)$

**Đề bài:** Cho $g \in O(f)$ và $f \in O(g)$, chứng minh $O(f) = O(g)$.

> ⚠️ Bắt buộc tách 2 vế và có chữ **"bất kỳ"**.

- **Vế 1: Chứng minh $O(f(n)) \subseteq O(g(n))$:**
  - Do $f \in O(g) \implies \exists c_1 \in \mathbb{R}^+, \exists n_1 \in \mathbb{N}, \forall n \ge n_1: 0 \le f(n) \le c_1 \cdot g(n)$.
  - Xét một hàm **bất kỳ** $h(n) \in O(f(n)) \implies \exists c_2 \in \mathbb{R}^+, \exists n_2 \in \mathbb{N}, \forall n \ge n_2: 0 \le h(n) \le c_2 \cdot f(n)$.
  - Với mọi $n \ge n_0 = \max(n_1, n_2): 0 \le h(n) \le c_2 (c_1 g(n)) = (c_1 c_2) g(n)$.
  - Chọn $c = c_1 c_2 \in \mathbb{R}^+, n_0 = \max(n_1, n_2) \in \mathbb{N} \implies h(n) \in O(g(n))$.
  - Do $h(n)$ bất kỳ $\implies O(f(n)) \subseteq O(g(n)) \quad (1)$.
- **Vế 2: Chứng minh $O(g(n)) \subseteq O(f(n))$:**
  - Do $g \in O(f) \implies \exists c_3, n_3$. Xét hàm **bất kỳ** $k(n) \in O(g) \implies \exists c_4, n_4$. Lấy $n_0' = \max(n_3, n_4), c' = c_3 c_4 \implies k(n) \in O(f(n)) \implies O(g) \subseteq O(f) \quad (2)$.
- **Kết luận:** Từ $(1)$ và $(2)$ suy ra $O(f(n)) = O(g(n))$ (ĐPCM).

## 3. CÁC BÀI CHỨNG MINH ĐỊNH NGHĨA KINH ĐIỂN

- **$f+g \in O(\max(f, g))$:** $f+g \le 2\max(f, g) \implies c=2, n_0=1$.
- **$T_1 \in O(f), T_2 \in O(g) \implies T_1+T_2 \in O(\max(f, g))$:** 2 giả thiết lấy hằng số khác tên $(c_1, n_1), (c_2, n_2)$. Chọn $c = c_1 + c_2, n_0 = \max(n_1, n_2)$.
- **Hạng tử âm ở vế bị so sánh (vd $7n^2 \in O(n^2 - 80n)$):** chọn $c$ lớn hơn hệ số, $7n^2 \le 8(n^2 - 80n) \iff n \ge 640 \implies c = 8, n_0 = 640$.
- **$(n+a)^b \in \Theta(n^b)$ ($b>0$):** Xét $n \ge 2|a| \implies n/2 \le n+a \le 2n \implies (1/2)^b n^b \le (n+a)^b \le 2^b n^b \implies c_1=(1/2)^b, c_2=2^b, n_0=\lceil 2|a| \rceil$.
- **$\log(n!) \in \Theta(n \log n)$:** Có $n! \le n^n \implies \log(n!) \le n\log n$. Mặt khác $n! \ge (n/2)^{n/2} \implies \log(n!) \ge \frac{1}{4}n\log n$ ($\forall n \ge 4$). Chọn $c_1=1/4, c_2=1, n_0=4$.

## 4. CHUỖI PHÂN LỚP BIG-O & CÔNG THỨC BIẾN ĐỔI

**Chuỗi chuẩn tăng dần:**
$$1 \prec \log \log n \prec \log n \prec \log^k n \prec \sqrt[c]{n} \prec n \prec n \log n$$
$$\prec n^2 \prec n^k \prec a^{\sqrt{n}} \prec a^n \prec n! \prec n^n$$

**Công thức biến đổi đưa về dạng chuẩn:**
- $a^{\log_b n} = n^{\log_b a}$ (Vd: $4^{\log_2 n} = n^{\log_2 4} = n^2$).
- $\sqrt{a^b} = a^{b/2}$ (Vd: $\sqrt{3^{\sqrt{n}}} = 3^{\frac{\sqrt{n}}{2}}$), $\sqrt{n} \cdot 3^{n/2} = \sqrt{n}(\sqrt{3})^n$.
- $\sum_{i=1}^n i = \frac{n(n+1)}{2} = \Theta(n^2)$, $\sum_{i=1}^n i^2 = \frac{n(n+1)(2n+1)}{6} = \Theta(n^3)$.
- $\sum_{i=1}^n \sum_{j=1}^n (i \cdot j) = [\frac{n(n+1)}{2}]^2 = \frac{n^4+2n^3+n^2}{4} = \Theta(n^4)$.
- Cấp số nhân: $\sum_{i=0}^{k} a^i = \frac{a^{k+1}-1}{a-1}$ ($a \ne 1$).

## 5. PHÂN TÍCH THUẬT TOÁN LẶP & THÁP HÀ NỘI

- **Thuật toán lặp:** (1) Nêu rõ chức năng hàm, (2) Chỉ ra phép toán cơ bản, (3) Lập tổng: $C(n) = \sum_{i=0}^{n-2} \sum_{j=i+1}^{n-1} 1 = \sum_{i=0}^{n-2}(n-1-i) = \frac{n(n-1)}{2} \implies O(n^2)$.
- **Thành lập PT đệ quy Tháp Hà Nội:**
  $$\begin{cases} T(1) = 1 & \text{(chuyển 1 đĩa trực tiếp } A \to C) \\ T(n) = 2T(n-1) + 1 & (n > 1: A \to B, A \to C, B \to C) \end{cases}$$

## 6. BỘ 3 CÁCH GIẢI PT ĐỆ QUY (MASTER KHÔNG THI)

**Giải hệ thức Tháp Hà Nội: $T(1)=1, T(n)=2T(n-1)+1$:**

1. **Phương pháp 1: Thế ngược (Backward Substitution):**
   - $T(n) = 2T(n-1) + 1 = 2^2 T(n-2) + 2 + 1 = \dots = 2^k T(n-k) + \sum_{i=0}^{k-1} 2^i$.
   - Dừng khi $n-k=1 \implies k=n-1$:
     $$T(n) = 2^{n-1}T(1) + (2^{n-1}-1) = 2^n - 1 \implies O(2^n).$$
2. **Phương pháp 2: Phương trình đặc trưng:**
   - PT thuần nhất: $r - 2 = 0 \implies r = 2 \implies T^{(h)}(n) = C \cdot 2^n$.
   - Nghiệm riêng: vế phải $f(n)=1 \implies T^{(p)}(n) = A \implies A - 2A = 1 \implies A = -1$.
   - Nghiệm tổng quát: $T(n) = C \cdot 2^n - 1$. Với $T(1)=1 \implies 2C - 1 = 1 \implies C = 1 \implies T(n) = 2^n - 1 \implies O(2^n)$.
3. **Phương pháp 3: Hàm sinh (Generating Functions):**
   - Đặt $G(x) = \sum T_n x^n$, nhân $x^n$ vào 2 vế, lấy tổng, rút $G(x)$, tách phân thức rồi đọc hệ số của $x^n$.
   - 4 công thức: $\frac{1}{1-x} = \sum_{n \ge 0} x^n$, $\frac{1}{(1-x)^2} = \sum_{n \ge 0} (n+1) x^n$, $\frac{x}{(1-x)^2} = \sum_{n \ge 0} n x^n$, $\frac{1}{(1-x)^3} = \sum_{n \ge 0} \frac{(n+1)(n+2)}{2} x^n$. Thay $x$ bằng $ax$: $\frac{1}{1-ax} = \sum_{n \ge 0} a^n x^n$. Quên thì đạo hàm 2 vế công thức trước.
   - Vd Hà Nội: $G(x) = \sum_{n \ge 1} T_n x^n$. Nhân $x^n$ vào $T_n - 2T_{n-1} = 1$ rồi lấy tổng $n \ge 2$:
     $$(G(x) - T_1 x) - 2x G(x) = \frac{x^2}{1-x}$$
     $$\implies G(x) = \frac{x}{(1-x)(1-2x)} = \frac{1}{1-2x} - \frac{1}{1-x}$$
     $\implies T_n = 2^n - 1 \implies O(2^n)$.

---
---

# ==========================================
# 📄 MẶT 2: QUY HOẠCH ĐỘNG, THAM LAM, QUAY LUI & WECODE (PHẦN 2 - 7 ĐIỂM)
# ==========================================

## 1. QUY TRÌNH 4 BƯỚC QUY HOẠCH ĐỘNG (DP)

- **B1 (Ý nghĩa bảng):** Nêu rõ $DP[i][j]$ (hoặc $M[i]$) lưu đại lượng tối ưu gì.
- **B2 (Công thức DP):** Ghi rõ cơ sở ($i=j$) + công thức chuyển trạng thái ($i<j$).
- **B3 (Điền bảng Bottom-Up):** Điền theo độ dài đường chéo $L=j-i+1$.
- **B4 (Truy vết):** Dùng bảng vết $trace[i][j]=k$ (hoặc $S[i]$) để in nghiệm.

## 2. CÔNG THỨC 6 BÀI TOÁN QUY HOẠCH ĐỘNG

- **(1) Đặt dấu ngoặc biểu thức số thực ($x_0 o_0 x_1 \dots x_n$):**
  $$DP[i][i] = x_i, \quad DP[i][j] = \max_{i \le k < j} \{ DP[i][k] \circ_k DP[k+1][j] \}$$
  Bảng vết $trace[i][j]=k$. Giá trị lớn nhất: $DP[0][n]$.
  **Có số âm:** lưu cả $MAX[i][j]$ và $MIN[i][j]$. Phép $+$: $MAX = MAX + MAX$, $MIN = MIN + MIN$. Phép $\times$: $MAX$ (và $MIN$) là max (và min) của 4 tích $MAX \cdot MAX, MAX \cdot MIN, MIN \cdot MAX, MIN \cdot MIN$ của 2 nửa.
- **(2) Dãy con tăng dài nhất (LIS - Buổi 8):** $M[i]$ là độ dài dãy con tăng dài nhất kết thúc tại $a_i$, cơ sở $M[i] = 1$.
  $$M[i] = 1 + \max_{0 \le j < i, a_j < a_i} \{ M[j] \}, \quad S[i] = j^*$$
  Kết quả: $L_{max} = \max_{0 \le i < n} M[i]$ (ô lớn nhất mảng $M$, không phải ô cuối).
- **(3) Nhân chuỗi ma trận (MCM):**
  $$m[i][i] = 0, \quad m[i][j] = \min_{i \le k < j} \{ m[i][k] + m[k+1][j] + p_{i-1}p_kp_j \}$$
  Bảng vết $s[i][j]=k$. Độ phức tạp: $O(n^3)$ thời gian, $O(n^2)$ bộ nhớ.
- **(4) Tính tổ hợp $C_n^k$ / Pascal:** $C[i][0]=1, C[i][i]=1$, $C[i][j] = C[i-1][j-1] + C[i-1][j]$. Top-down có ghi nhớ chỉ điền ô cần tới, ô được ghi khi lời gọi trả về: $C(3,2)$ điền lần lượt $C(1,0), C(1,1), C(2,1), C(2,2), C(3,2)$.
- **(5) Cái túi 0/1 (Knapsack):** $DP[i][w] = \max(DP[i-1][w], DP[i-1][w-w_i] + v_i)$ khi $w_i \le w$, ngược lại bằng $DP[i-1][w]$.
- **(6) Dãy con chung dài nhất LCS ($|X| = n, |Y| = m$):** $M[i][j]$ là độ dài LCS của $X[1..i]$ và $Y[1..j]$, cơ sở $M[i][0] = M[0][j] = 0$.
  $$M[i][j] = \begin{cases} M[i-1][j-1] + 1 & x_i = y_j \\ \max(M[i-1][j], M[i][j-1]) & x_i \ne y_j \end{cases}$$
  Đáp án ở ô cuối $M[n][m]$, không lấy max cả bảng. Truy vết từ ô cuối: bằng nhau thì ghi ký tự rồi đi chéo, khác nhau thì đi về ô lớn hơn.

## 3. THAM LAM (GREEDY) - BA LÔ PHÂN SỐ

- **Mô hình hóa:** $\max \sum p_i x_i$ thỏa $\sum w_i x_i \le M, 0 \le x_i \le 1$.
- **Chiến lược:** Tính đơn giá $v_i = p_i/w_i$, sắp xếp giảm dần.
- **Mã giả:**
  1. Tính $v[i] = p[i]/w[i]$, sắp xếp đồ vật theo $v[i]$ giảm dần. Gán $cap = M$, $max\_p = 0$.
  2. Với $i = 1..n$: nếu $cap = 0$ thì dừng.
  3. Nếu $w[i] \le cap$: $x[i] = 1$, $cap = cap - w[i]$, $max\_p = max\_p + p[i]$.
  4. Ngược lại: $x[i] = cap/w[i]$, $max\_p = max\_p + p[i] \cdot x[i]$, $cap = 0$.
  5. Trả về $(x, max\_p)$. Độ phức tạp: $O(n\log n)$ do bước sắp xếp.

## 4. KHUNG QUAY LUI (BACKTRACKING) & WECODE

**Khung mã giả Quay lui chuẩn:**

1. Với mỗi $v \in S_k$: Nếu $IsValid(v, k, State)$ thì:
2. Gán $X[k] = v$, cập nhật $State$.
3. Nếu $k == n$ thì: In nghiệm $X[1..n]$.
4. Ngược lại: Gọi đệ quy $Backtrack(k+1, n, State)$.
5. Hoàn tác $State$ (**Quay lui / Undo**).

## 5. TỔNG HỢP 10 BÀI TOÁN WECODE CHUẨN THI

- **1. Tính điểm môn học:** Nhân 400 để thành số nguyên: $\text{min\_T} \le \sum V_i w_i \le \text{max\_T}$. Nhánh cận: $rem\_max = rem\_w[i] \times 40, rem\_min = rem\_w[i] \times 1$. Cắt tỉa nếu ngoài khoảng. $O(40^n)$, bộ nhớ $O(n)$.
- **2. Khôi phục IP:** Thử độ dài đoạn $1..3$. Ràng buộc $0 \le val \le 255$, không có số 0 đầu nếu $len > 1$. Khi $part==4 \land start==length(S) \implies$ Lưu IP. $O(1)$.
- **3. Tách chuỗi đối xứng (Palindrome):** Cắt $S[start..end]$, nếu $IsPalindrome \implies$ thêm vào list, đệ quy $end+1$, quay lui xóa phần tử cuối. $O(n \cdot 2^n)$.
- **4. Tìm từ trong ô chữ (Word Search):** DFS 4 hướng, gán tạm $Board[r][c] = '\#'$ để đánh dấu, quay lui trả lại ký tự cũ. $O(M \cdot N \cdot 4^L)$.
- **5. Giải Sudoku 9x9:** Thử điền $1..9$ vào ô trống, kiểm tra Hàng, Cột, Khối $3 \times 3$, quay lui $Board[r][c]=0$. $O(9^{81})$.
- **6. Sinh hoán vị:** Dùng $X[1..n]$ và $used[1..n]$. Quay lui $O(n \cdot n!)$, bộ nhớ $O(n)$. So với Giảm để trị (chèn $a_n$ vào mọi vị trí của các hoán vị $n-1$ phần tử) tốn $O(n \cdot n!)$ RAM.
- **7. Dò mìn (Minesweeper):** Click trúng $'M' \to 'X'$, ô có mìn lân cận $\to$ ghi số, ô rỗng $\to 'B'$ và lan truyền đệ quy 8 hướng. $O(M \cdot N)$.
- **8. Mã đi tuần (Knight's Tour):** 8 hướng $(\pm 1, \pm 2), (\pm 2, \pm 1)$. $Board[u][v] = step + 1$, hoàn tác gán 0. Warnsdorff: ưu tiên ô có bậc đi tiếp nhỏ nhất. $O(8^{n^2})$.
- **9. N-Queens:** 3 mảng đánh dấu: $col[j], diag_1[i+j], diag_2[i-j+n]$. $O(n!)$.
- **10. Tô màu đồ thị:** Thử màu $1..M$ cho đỉnh $u$, kiểm tra không trùng màu đỉnh kề, đệ quy $u+1$, hoàn tác gán 0. $O(M^n)$.
