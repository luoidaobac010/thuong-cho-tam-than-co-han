# ĐÁP ÁN CHUYÊN ĐỀ 1: LÝ THUYẾT

---

## DẠNG 1: CHỨNG MINH KÝ HIỆU TIỆM CẬN
**Bài 1.1:** $f(n) = 5n^3 + 2n^2 + 10 \in O(n^3)$
- Với $n \ge 1$: $5n^3 + 2n^2 + 10 \le 5n^3 + 2n^3 + 10n^3 = 17n^3$.
- Chọn $c = 17, n_0 = 1$. Thỏa mãn định nghĩa $O$.

**Bài 1.2:** $f(n) = n^2 \log n + n^3 \in \Omega(n^3)$
- Với mọi $n > 1$, $n^2 \log n > 0$, do đó $n^2 \log n + n^3 \ge n^3$.
- Chọn $c = 1, n_0 = 2$. Thỏa mãn định nghĩa $\Omega$.

**Bài 1.3:** $f(n) = \frac{1}{2} n^2 - 3n \in \Theta(n^2)$
- Giới hạn trên: $\frac{1}{2} n^2 - 3n \le \frac{1}{2} n^2$. Chọn $c_2 = 1/2$. (Đúng với mọi $n \ge 1$).
- Giới hạn dưới: $\frac{1}{2} n^2 - 3n \ge \frac{1}{4} n^2 \Leftrightarrow \frac{1}{4}n^2 \ge 3n \Leftrightarrow n \ge 12$.
- Chọn $c_1 = 1/4, c_2 = 1/2, n_0 = 12$. Thỏa định nghĩa $\Theta$.

---

## DẠNG 2: SẮP XẾP BẬC TĂNG TRƯỞNG
**Bài 2.1:**
- $2^{\log_2 n} = n \in \Theta(n)$
- $\log_2(n^5) = 5 \log_2 n \in \Theta(\log n)$
- $n \sqrt{n} = n^{1.5} \in \Theta(n^{1.5})$
- $10n^3 + n^2 \in \Theta(n^3)$
- $4^n \in \Theta(4^n)$
- $(n-1)! \in \Theta(n!)$
Thứ tự: $\log_2(n^5) \prec 2^{\log_2 n} \prec n \sqrt{n} \prec 10n^3 + n^2 \prec 4^n \prec (n-1)!$

**Bài 2.2:**
So sánh $n^2 \log n$ và $n^{1.5} \log^2 n$.
Bỏ phần chung là $\log n$: ta đang so $n^2$ với $n^{1.5} \log n$.
Rõ ràng $n^2$ (bậc 2) tăng nhanh hơn $n^{1.5} \log n$ rất nhiều.
Vậy thuật toán B ($O(n \sqrt{n} \log^2 n)$) chạy nhanh hơn khi $n$ rất lớn.

---

## DẠNG 3: ĐẾM SỐ PHÉP TOÁN
**Bài 3.1:**
- Vòng $k$ chạy đúng $100$ lần.
- Vòng $j$ chạy $i$ lần.
- Vòng $i$ chạy $n$ lần.
- Số phép toán: $\sum_{i=1}^n \sum_{j=1}^i 100 = 100 \sum_{i=1}^n i = 100 \frac{n(n+1)}{2} \in O(n^2)$.

**Bài 3.2:**
- Vòng ngoài $i$ lặp $i = n, n/2, n/4... \Rightarrow \approx \log_2 n$ lần.
- Vòng trong $j$ lặp $j = 1, 3, 9... \Rightarrow \approx \log_3 n$ lần.
- Số phép toán: $\log_2 n \times \log_3 n \in O(\log^2 n)$.

---

## DẠNG 4: PHƯƠNG TRÌNH ĐỆ QUY
**Bài 4.1:** Binary Search
- Gọi đệ quy: Mỗi lần chia đôi mảng và chỉ đi vào 1 nhánh. Phép tính $mid$ mất $O(1)$.
- $T(n) = T(n/2) + O(1)$.
- Giải (Master): $a = 1, b = 2, f(n) = 1 = n^0$. $\log_2 1 = 0$. Thuộc Case 2 của Master Theorem: $T(n) = \Theta(\log n)$.

**Bài 4.2:** Strassen
- $T(n) = 7T(n/2) + O(n^2)$.
- $a = 7, b = 2, f(n) = n^2$. $\log_b a = \log_2 7 \approx 2.81$.
- Vì $\log_2 7 > 2 \Rightarrow n^{\log_2 7} > n^2$.
- Thuộc Case 1 của Master Theorem: $T(n) = \Theta(n^{\log_2 7})$.
