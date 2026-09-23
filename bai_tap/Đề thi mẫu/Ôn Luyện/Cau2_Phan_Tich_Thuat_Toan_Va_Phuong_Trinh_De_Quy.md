# CÂU 2: PHÂN TÍCH THUẬT TOÁN & GIẢI PHƯƠNG TRÌNH ĐỆ QUY
## MÔN: PHÂN TÍCH VÀ THIẾT KẾ THUẬT TOÁN (CS112) - CÔ HUỲNH THỊ THANH THƯƠNG

---

# PHẦN 1: PHÂN TÍCH THUẬT TOÁN LẶP (DẠNG 2A)

## 1. Phương pháp luận phân tích thuật toán lặp
Khi nhận được một đoạn mã hoặc hàm lặp `func(a, n)`:
1. **Xác định Chức năng / Ý nghĩa kết quả trả về:**
   - Trả về giá trị gì (ví dụ: tổng, phần tử lớn nhất, vị trí tìm thấy, số cặp thỏa điều kiện,...).
2. **Xác định Phép toán cơ bản (Basic Operation):**
   - Phép toán nằm trong vòng lặp sâu nhất (ví dụ: phép so sánh `a[i] > a[j]`, phép gán, phép cộng `sum += ...`).
3. **Lập công thức tổng $\sum$:**
   - Thiết lập các dấu $\sum$ tương ứng từ vòng lặp ngoài vào vòng lặp trong.
4. **Khai triển và rút gọn tổng $\sum$:**
   - Sử dụng các công thức cấp số cộng, cấp số nhân, tổng bình phương:
     * $\sum_{i=1}^n 1 = n$
     * $\sum_{i=1}^n i = \frac{n(n+1)}{2} = \frac{n^2+n}{2}$
     * $\sum_{i=1}^n i^2 = \frac{n(n+1)(2n+1)}{6} = \frac{2n^3 + 3n^2 + n}{6}$
5. **Kết luận độ phức tạp:**
   - Xác định số hạng bậc cao nhất để đưa ra $O(n^k)$ hoặc $\Theta(n^k)$.

---

## 2. Bài tập mẫu phân tích thuật toán lặp

### Bài 1: Thuật toán đếm cặp
```c
int func(int a[], int n) {
    int count = 0;
    for (int i = 0; i < n - 1; i++) {
        for (int j = i + 1; j < n; j++) {
            if (a[i] == a[j]) {
                count++;
            }
        }
    }
    return count;
}
```
**Trả lời câu hỏi:**
1. **Lời gọi hàm `func(a, n)` trả về thông tin gì?**
   - Hàm trả về số lượng cặp phần tử trùng nhau $(a[i], a[j])$ với chỉ số $0 \le i < j < n$ trong mảng $a$.
2. **Đếm phép toán và xác định độ phức tạp:**
   - Phép toán cơ bản là phép so sánh `a[i] == a[j]`.
   - Tổng số phép so sánh thực hiện là:
     $$C(n) = \sum_{i=0}^{n-2} \sum_{j=i+1}^{n-1} 1 = \sum_{i=0}^{n-2} (n - 1 - i)$$
     Đặt $k = n - 1 - i$, khi $i = 0 \implies k = n-1$; khi $i = n-2 \implies k = 1$:
     $$C(n) = \sum_{k=1}^{n-1} k = \frac{(n-1)n}{2} = \frac{n^2 - n}{2}$$
   - Do số hạng bậc cao nhất là $n^2$, độ phức tạp thời gian của giải thuật là $O(n^2)$ (hoặc $\Theta(n^2)$).

---

# PHẦN 2: THÀNH LẬP PHƯƠNG TRÌNH ĐỆ QUY (DẠNG 2B)

## 1. Bài toán Tháp Hà Nội (Đề thi HK1 2025-2026)

### Đề bài:
```c
hanoi(n, A, B, C) {
    if (n == 1) 
        transfer(A, C);
    else {
        hanoi(n-1, A, C, B);
        transfer(A, C);  // chuyển 1 đĩa từ cột A sang cột C
        hanoi(n-1, B, A, C);
    }
}
```
*Yêu cầu:* Thành lập phương trình đệ quy biểu diễn số thao tác chuyển đĩa được thực hiện trong thuật toán, kèm theo giải thích ngắn gọn cách thiết lập phương trình (đếm chính xác số thao tác, không dùng hằng số $c_1, c_2$).

### Lời giải:
Gọi $T(n)$ là số thao tác chuyển đĩa (`transfer`) cần thực hiện để chuyển $n$ đĩa từ cột $A$ sang cột $C$.

**Phân tích các trường hợp:**
1. **Trường hợp cơ sở ($n = 1$):**
   - Chỉ có 1 đĩa, thuật toán thực hiện 1 lần gọi hàm `transfer(A, C)` trực tiếp.
   - Do đó: $T(1) = 1$.
2. **Trường hợp đệ quy ($n > 1$):**
   - Để chuyển $n$ đĩa từ $A$ sang $C$ qua cột trung gian $B$, thuật toán thực hiện 3 bước:
     1. `hanoi(n-1, A, C, B)`: Chuyển $n-1$ đĩa từ $A$ sang $B$ (sử dụng $C$ làm trung gian) $\rightarrow$ Cần $T(n-1)$ lần chuyển.
     2. `transfer(A, C)`: Chuyển đĩa lớn nhất thứ $n$ từ $A$ sang $C$ $\rightarrow$ Đúng $1$ lần chuyển.
     3. `hanoi(n-1, B, A, C)`: Chuyển $n-1$ đĩa từ $B$ sang $C$ (sử dụng $A$ làm trung gian) $\rightarrow$ Cần $T(n-1)$ lần chuyển.
   - Tổng số thao tác chuyển là: $T(n) = T(n-1) + 1 + T(n-1) = 2T(n-1) + 1$.

**Hệ thức đệ quy hoàn chỉnh:**
$$\begin{cases} T(1) = 1 \\ T(n) = 2T(n-1) + 1 & \text{với } n > 1 \end{cases}$$

---

# PHẦN 3: GIẢI PHƯƠNG TRÌNH ĐỆ QUY (DẠNG 2C)

> 🔴 **CẢNH BÁO QUAN TRỌNG:** Cô Thương **KHÔNG CHO PHÉP** sử dụng Master Theorem (Định lý thợ). Sinh viên phải nắm vững 3 phương pháp chính thống:
> 1. Phương pháp Truy hồi lặp / Thế ngược (Backward Substitution)
> 2. Phương pháp Phương trình đặc trưng (Characteristic Equation)
> 3. Phương pháp Hàm sinh (Generating Functions)

---

## BÀI TOÁN TRỌNG TÂM: GIẢI HỆ THỨC THÁP HÀ NỘI
$$\begin{cases} T(1) = 1 \\ T(n) = 2T(n-1) + 1 & (n > 1) \end{cases}$$

### PHƯƠNG PHÁP 1: TRUY HỒI THẾ NGƯỢC (BACKWARD SUBSTITUTION)

Áp dụng liên tiếp hệ thức đệ quy $T(n) = 2T(n-1) + 1$:
- Bước 1: $T(n) = 2T(n-1) + 1$
- Bước 2: Thay $T(n-1) = 2T(n-2) + 1$:
  $$T(n) = 2(2T(n-2) + 1) + 1 = 2^2 T(n-2) + 2^1 + 2^0$$
- Bước 3: Thay $T(n-2) = 2T(n-3) + 1$:
  $$T(n) = 2^2(2T(n-3) + 1) + 2 + 1 = 2^3 T(n-3) + 2^2 + 2^1 + 2^0$$
- ...
- Bước $k$: Tổng quát sau $k$ lần thế:
  $$T(n) = 2^k T(n-k) + \sum_{i=0}^{k-1} 2^i$$
- Dừng lại khi chạm điều kiện cơ sở: $n - k = 1 \implies k = n - 1$.
  $$T(n) = 2^{n-1} T(1) + \sum_{i=0}^{n-2} 2^i$$
- Vì $T(1) = 1$ và tổng cấp số nhân $\sum_{i=0}^{n-2} 2^i = \frac{2^{n-1} - 1}{2 - 1} = 2^{n-1} - 1$:
  $$T(n) = 2^{n-1} \cdot 1 + 2^{n-1} - 1 = 2 \cdot 2^{n-1} - 1 = 2^n - 1$$

**Kết luận:** $T(n) = 2^n - 1 \implies T(n) \in O(2^n)$ (hoặc $\Theta(2^n)$).

---

### PHƯƠNG PHÁP 2: PHƯƠNG TRÌNH ĐẶC TRƯNG (CHARACTERISTIC EQUATION)

Xét phương trình sai phân tuyến tính không thuần nhất:
$$T(n) - 2T(n-1) = 1 \quad \text{với } T(1) = 1$$

Nghiệm tổng quát của phương trình gồm 2 phần: $T(n) = T^{(h)}(n) + T^{(p)}(n)$
trong đó $T^{(h)}(n)$ là nghiệm của phương trình thuần nhất, và $T^{(p)}(n)$ là một nghiệm riêng.

**Bước 1: Tìm nghiệm thuần nhất $T^{(h)}(n)$**
- Xét phương trình thuần nhất: $T(n) - 2T(n-1) = 0$.
- Phương trình đặc trưng: $r - 2 = 0 \implies r = 2$.
- Nghiệm thuần nhất có dạng:
  $$T^{(h)}(n) = C \cdot 2^n \quad (C \text{ là hằng số})$$

**Bước 2: Tìm nghiệm riêng $T^{(p)}(n)$**
- Vế phải là đa thức bậc 0: $f(n) = 1 = 1 \cdot (1)^n$.
- Cơ số của vế phải là $s = 1$. Vì $s = 1$ không phải là nghiệm của phương trình đặc trưng ($r = 2 \ne 1$), nghiệm riêng có dạng một hằng số $A$:
  $$T^{(p)}(n) = A$$
- Thay $T^{(p)}(n) = A$ vào phương trình ban đầu $T(n) - 2T(n-1) = 1$:
  $$A - 2A = 1 \iff -A = 1 \iff A = -1$$
- Vậy nghiệm riêng là $T^{(p)}(n) = -1$.

**Bước 3: Nghiệm tổng quát và xác định hằng số $C$**
- Nghiệm tổng quát là:
  $$T(n) = C \cdot 2^n - 1$$
- Áp dụng điều kiện đầu $T(1) = 1$:
  $$T(1) = C \cdot 2^1 - 1 = 1 \iff 2C = 2 \iff C = 1$$
- Do đó:
  $$T(n) = 1 \cdot 2^n - 1 = 2^n - 1$$

**Kết luận:** Độ phức tạp thời gian là $O(2^n)$.

---

### PHƯƠNG PHÁP 3: HÀM SINH (GENERATING FUNCTIONS)

Xét dãy $\{T_n\}$ với $n \ge 1$ thỏa mãn:
$$T_n - 2T_{n-1} = 1 \quad (\forall n \ge 2) \quad \text{với } T_1 = 1$$

**Bước 1: Định nghĩa hàm sinh**
Đặt $G(x) = \sum_{n=1}^\infty T_n x^n$.

**Bước 2: Biến đổi phương trình sai phân sang hàm sinh**
- Nhân hai vế của phương trình sai phân với $x^n$ và lấy tổng từ $n = 2$ đến $\infty$:
  $$\sum_{n=2}^\infty T_n x^n - 2 \sum_{n=2}^\infty T_{n-1} x^n = \sum_{n=2}^\infty x^n$$
- Ta có:
  * $\sum_{n=2}^\infty T_n x^n = G(x) - T_1 x = G(x) - x$ (vì $T_1 = 1$).
  * $\sum_{n=2}^\infty T_{n-1} x^n = x \sum_{n=2}^\infty T_{n-1} x^{n-1} = x \sum_{k=1}^\infty T_k x^k = x G(x)$.
  * $\sum_{n=2}^\infty x^n = x^2 \sum_{i=0}^\infty x^i = \frac{x^2}{1-x}$ (chuỗi hình học với $|x| < 1$).
- Thay vào phương trình:
  $$(G(x) - x) - 2x G(x) = \frac{x^2}{1-x}$$
  $$G(x)(1 - 2x) = x + \frac{x^2}{1-x} = \frac{x(1-x) + x^2}{1-x} = \frac{x}{1-x}$$
  $$G(x) = \frac{x}{(1-x)(1-2x)}$$

**Bước 3: Phân tích phân thức hữu tỉ thành các phân thức tối giản**
- Phân tích:
  $$\frac{x}{(1-x)(1-2x)} = \frac{A}{1-x} + \frac{B}{1-2x}$$
- Quy đồng mẫu số:
  $$x = A(1-2x) + B(1-x)$$
- Tìm các hệ số $A, B$:
  * Cho $x = 1 \implies 1 = A(1-2) = -A \implies A = -1$.
  * Cho $x = \frac{1}{2} \implies \frac{1}{2} = B\left(1 - \frac{1}{2}\right) = \frac{1}{2}B \implies B = 1$.
- Do đó:
  $$G(x) = \frac{1}{1-2x} - \frac{1}{1-x}$$

**Bước 4: Khai triển chuỗi Taylor và xác định hệ số $T_n$**
- Áp dụng công thức khai triển chuỗi hình học $\frac{1}{1-u} = \sum_{n=0}^\infty u^n$:
  * $\frac{1}{1-2x} = \sum_{n=0}^\infty (2x)^n = \sum_{n=0}^\infty 2^n x^n$
  * $\frac{1}{1-x} = \sum_{n=0}^\infty x^n$
- Suy ra:
  $$G(x) = \sum_{n=0}^\infty (2^n - 1) x^n$$
- Vì $G(x) = \sum_{n=1}^\infty T_n x^n$ (với $n=0$ thì $2^0 - 1 = 0$), nên hệ số của $x^n$ chính là:
  $$T_n = 2^n - 1 \quad (\forall n \ge 1)$$

**Kết luận:** $T(n) = 2^n - 1 \implies O(2^n)$.

---

# PHẦN 4: BẢNG TỔNG HỢP CÁC PHƯƠNG TRÌNH ĐỆ QUY KINH ĐIỂN

| Thuật toán / Hệ thức | Phương trình đệ quy | Phương pháp giải | Nghiệm chính xác | Big-O |
| :--- | :--- | :--- | :--- | :---: |
| **Tháp Hà Nội** | $T(n) = 2T(n-1) + 1, T(1)=1$ | Thế ngược / PT đặc trưng / Hàm sinh | $T(n) = 2^n - 1$ | $O(2^n)$ |
| **Tìm kiếm nhị phân** | $T(n) = T(n/2) + 1, T(1)=1$ | Đặt $n = 2^k$, thế ngược | $T(n) = \log_2 n + 1$ | $O(\log n)$ |
| **Merge Sort** | $T(n) = 2T(n/2) + n, T(1)=0$ | Đặt $n = 2^k$, chia 2 vế cho $n$ | $T(n) = n \log_2 n$ | $O(n \log n)$ |
| **Fibonacci** | $F(n) = F(n-1) + F(n-2)$ | Phương trình đặc trưng bậc 2 | $F(n) = \frac{1}{\sqrt{5}}[\phi^n - \hat{\phi}^n]$ | $O(1.618^n)$ |
| **Hệ thức sai phân bậc 2** | $a_n - 5a_{n-1} + 6a_{n-2} = 0$ | $r^2 - 5r + 6 = 0 \implies r = 2, 3$ | $a_n = C_1 2^n + C_2 3^n$ | $O(3^n)$ |
