# CÂU 1: KÝ HIỆU TIỆM CẬN & PHÂN LỚP ĐỘ PHỨC TẠP THUẬT TOÁN
## MÔN: PHÂN TÍCH VÀ THIẾT KẾ THUẬT TOÁN (CS112) - CÔ HUỲNH THỊ THANH THƯƠNG

---

# PHẦN 1: LÝ THUYẾT VÀ QUY TẮC CỐT LÕI

## 1. Định nghĩa chuẩn toán học các ký hiệu tiệm cận (MANDATORY)

> 🔴 **QUY TẮC CÔ THƯƠNG:** Khi chứng minh theo định nghĩa:
> - **KHÔNG** sử dụng giới hạn ($\lim$).
> - **KHÔNG** sử dụng các định lý tắt / l'Hôpital nếu đề bài yêu cầu "dùng định nghĩa".
> - Phải chỉ ra cặp hằng số thực sự tồn tại $(c, n_0)$ hoặc $(c_1, c_2, n_0)$ với $c, c_1, c_2 > 0$ và $n_0 \in \mathbb{N}$ sao cho bất đẳng thức nghiệm đúng với mọi $n \ge n_0$.

### a. Ký hiệu $O$ (Big-O - Giới hạn trên tiệm cận / Asymptotic Upper Bound)
$$f(n) \in O(g(n)) \iff \exists c > 0, \exists n_0 \in \mathbb{N}, \forall n \ge n_0: 0 \le f(n) \le c \cdot g(n)$$
*(hoặc $|f(n)| \le c \cdot |g(n)|$ khi xét hàm tổng quát)*

### b. Ký hiệu $\Omega$ (Big-Omega - Giới hạn dưới tiệm cận / Asymptotic Lower Bound)
$$f(n) \in \Omega(g(n)) \iff \exists c > 0, \exists n_0 \in \mathbb{N}, \forall n \ge n_0: 0 \le c \cdot g(n) \le f(n)$$

### c. Ký hiệu $\Theta$ (Big-Theta - Giới hạn tiệm cận chặt / Asymptotically Tight Bound)
$$f(n) \in \Theta(g(n)) \iff \exists c_1, c_2 > 0, \exists n_0 \in \mathbb{N}, \forall n \ge n_0: 0 \le c_1 \cdot g(n) \le f(n) \le c_2 \cdot g(n)$$
*Định lý tương đương:* $f(n) \in \Theta(g(n)) \iff f(n) \in O(g(n)) \text{ và } f(n) \in \Omega(g(n))$.

---

## 2. Chuỗi phân lớp độ phức tạp chuẩn tăng dần

Khi so sánh và sắp xếp các hàm theo "Big-O nhỏ nhất", áp dụng thang bậc tăng dần sau (với $k > 1, \alpha > 1, a > 1$):

$$O(1) < O(\log \log n) < O(\log n) < O((\log n)^k) < O(\sqrt[c]{n}) < O(n) < O(n \log n) < O(n^2) < O(n^k) < O(2^{\sqrt{n}}) < O(a^n) < O(n!) < O(n^n)$$

**Quy tắc biến đổi đưa về dạng chuẩn:**
1. $a^{\log_b n} = n^{\log_b a}$ (Công thức đổi cơ số logarit lũy thừa).
   - Ví dụ: $4^{\log_2 n} = n^{\log_2 4} = n^2$.
2. $\log(a \cdot b) = \log a + \log b$ và $\log(a^k) = k \log a$.
3. $\sqrt{a^b} = a^{b/2}$.
   - Ví dụ: $\sqrt{3^{\sqrt{n}}} = 3^{\frac{\sqrt{n}}{2}}$.
4. Tổng $\sum$: Đưa về dạng tường minh đa thức trước khi phân lớp.

---

# PHẦN 2: CÁC DẠNG BÀI TẬP CHỨNG MINH ĐỊNH NGHĨA (DẠNG 1A)

## Bài 1 (Đề thi HK1 2025-2026):
**Đề bài:** Dùng định nghĩa của các ký hiệu tiệm cận để chứng minh nhận định sau:  
Nếu $g(n) \in O(f(n))$ và $f(n) \in O(g(n))$ thì $O(f(n)) = O(g(n))$.

### Lời giải chi tiết:
Để chứng minh hai tập hợp bằng nhau: $O(f(n)) = O(g(n))$, ta bắt buộc phải chứng minh 2 vế bao hàm:
1. Chứng minh $O(f(n)) \subseteq O(g(n))$
2. Chứng minh $O(g(n)) \subseteq O(f(n))$

**Vế 1: Chứng minh $O(f(n)) \subseteq O(g(n))$**
- Theo giả thiết $f(n) \in O(g(n))$, theo định nghĩa Big-O ta có:
  $$\exists c_1 \in \mathbb{R}^+, \exists n_1 \in \mathbb{N}, \forall n \ge n_1: 0 \le f(n) \le c_1 \cdot g(n)$$
- Xét một hàm **bất kỳ** $h(n) \in O(f(n))$, theo định nghĩa Big-O ta có:
  $$\exists c_2 \in \mathbb{R}^+, \exists n_2 \in \mathbb{N}, \forall n \ge n_2: 0 \le h(n) \le c_2 \cdot f(n)$$
- Khi đó, với mọi $n \ge n_0 = \max(n_1, n_2)$, ta có:
  $$0 \le h(n) \le c_2 \cdot f(n) \le c_2 \cdot (c_1 \cdot g(n)) = (c_2 \cdot c_1) \cdot g(n)$$
- Suy ra chọn hằng số $c = c_2 \cdot c_1 > 0$ ($c \in \mathbb{R}^+$) và $n_0 = \max(n_1, n_2) \in \mathbb{N}$.
- Với mọi $n \ge n_0$, ta có $0 \le h(n) \le c \cdot g(n)$.
- Theo định nghĩa của Big-O, suy ra $h(n) \in O(g(n))$.
- Vì điều này đúng với mọi hàm $h(n)$ bất kỳ thuộc $O(f(n))$, ta có:
  $$O(f(n)) \subseteq O(g(n)) \quad (1)$$

**Vế 2: Chứng minh $O(g(n)) \subseteq O(f(n))$**
- Theo giả thiết $g(n) \in O(f(n))$, theo định nghĩa Big-O ta có:
  $$\exists c_3 \in \mathbb{R}^+, \exists n_3 \in \mathbb{N}, \forall n \ge n_3: 0 \le g(n) \le c_3 \cdot f(n)$$
- Xét một hàm **bất kỳ** $k(n) \in O(g(n))$, theo định nghĩa Big-O ta có:
  $$\exists c_4 \in \mathbb{R}^+, \exists n_4 \in \mathbb{N}, \forall n \ge n_4: 0 \le k(n) \le c_4 \cdot g(n)$$
- Khi đó, với mọi $n \ge n_0' = \max(n_3, n_4)$, ta có:
  $$0 \le k(n) \le c_4 \cdot g(n) \le c_4 \cdot (c_3 \cdot f(n)) = (c_4 \cdot c_3) \cdot f(n)$$
- Suy ra chọn hằng số $c' = c_4 \cdot c_3 > 0$ ($c' \in \mathbb{R}^+$) và $n_0' = \max(n_3, n_4) \in \mathbb{N}$.
- Với mọi $n \ge n_0'$, ta có $0 \le k(n) \le c' \cdot f(n)$.
- Theo định nghĩa của Big-O, suy ra $k(n) \in O(f(n))$.
- Vì điều này đúng với mọi hàm $k(n)$ bất kỳ thuộc $O(g(n))$, ta có:
  $$O(g(n)) \subseteq O(f(n)) \quad (2)$$

**Kết luận:** Từ $(1)$ và $(2)$, theo định nghĩa của quan hệ bằng nhau giữa hai tập hợp, ta có:
$$O(f(n)) = O(g(n)) \quad (\text{ĐPCM})$$

---

## Bài 2: Chứng minh $f(n) + g(n) \in O(\max(f(n), g(n)))$ với $f(n), g(n) \ge 0$
### Lời giải:
- Với mọi $n$, ta có:
  $$f(n) \le \max(f(n), g(n))$$
  $$g(n) \le \max(f(n), g(n))$$
- Cộng hai bất đẳng thức vế theo vế:
  $$0 \le f(n) + g(n) \le 2 \cdot \max(f(n), g(n))$$
- Chọn $c = 2 > 0$ và $n_0 = 1$.
- Với mọi $n \ge n_0 = 1$, bất đẳng thức $0 \le f(n) + g(n) \le c \cdot \max(f(n), g(n))$ luôn đúng.
- Theo định nghĩa Big-O, suy ra $f(n) + g(n) \in O(\max(f(n), g(n)))$ (ĐPCM).

---

## Bài 3: Chứng minh $(n+a)^b \in \Theta(n^b)$ với mọi $b > 0, a \in \mathbb{R}$
### Lời giải:
- Xét $n > |a|$, ta có $n - |a| \le n + a \le n + |a|$.
- Vì $n \ge 2|a| > 0$, ta có: $\frac{n}{2} \le n - |a| \le n + a \le n + \frac{n}{2} \le 2n$.
- Do $b > 0$, lũy thừa bậc $b$ các vế:
  $$\left(\frac{1}{2}\right)^b \cdot n^b \le (n+a)^b \le 2^b \cdot n^b$$
- Chọn:
  - $c_1 = \left(\frac{1}{2}\right)^b > 0$
  - $c_2 = 2^b > 0$
  - $n_0 = \max(1, \lceil 2|a| \rceil)$
- Khi đó với mọi $n \ge n_0$, ta có:
  $$0 \le c_1 \cdot n^b \le (n+a)^b \le c_2 \cdot n^b$$
- Theo định nghĩa $\Theta$, suy ra $(n+a)^b \in \Theta(n^b)$ (ĐPCM).

---

## Bài 4: Chứng minh $\log(n!) \in \Theta(n \log n)$
### Lời giải:
- Ta có $n! = 1 \cdot 2 \cdot 3 \cdots n \le n \cdot n \cdots n = n^n$.
  Lấy logarit cơ số 2 hai vế:
  $$\log(n!) \le \log(n^n) = n \log n \quad (\forall n \ge 1)$$
- Mặt khác:
  $$n! = 1 \cdot 2 \cdots \left\lfloor\frac{n}{2}\right\rfloor \cdot \left(\left\lfloor\frac{n}{2}\right\rfloor + 1\right) \cdots n \ge \left(\frac{n}{2}\right)^{\frac{n}{2}}$$
  Lấy logarit hai vế với $n \ge 2$:
  $$\log(n!) \ge \log\left(\left(\frac{n}{2}\right)^{n/2}\right) = \frac{n}{2} \log\left(\frac{n}{2}\right) = \frac{n}{2}(\log n - 1)$$
  Với mọi $n \ge 4 \implies \log n \ge 2 \implies \log n - 1 \ge \frac{1}{2}\log n$.
  Do đó:
  $$\log(n!) \ge \frac{n}{2} \cdot \frac{1}{2}\log n = \frac{1}{4} n \log n \quad (\forall n \ge 4)$$
- Kết hợp cả hai vế:
  $$\frac{1}{4} n \log n \le \log(n!) \le 1 \cdot n \log n \quad (\forall n \ge 4)$$
- Chọn $c_1 = \frac{1}{4} > 0$, $c_2 = 1 > 0$, $n_0 = 4$.
- Theo định nghĩa $\Theta$, suy ra $\log(n!) \in \Theta(n \log n)$ (ĐPCM).

---

# PHẦN 3: PHÂN LỚP VÀ SẮP XẾP HÀM THEO BIG-O NHỎ NHẤT (DẠNG 1B)

## Bài toán mẫu trong Đề thi 2025:
**Đề bài:** Phân lớp 07 hàm bên dưới vào các “Big-O nhỏ nhất”, có giải thích ngắn gọn cách xác định. Sắp xếp các hàm theo thứ tự tăng dần của Big-O:
- $f_1(n) = 4^{\log n} + \log \log n$
- $f_2(n) = n \cdot \sqrt[3]{n}$
- $f_3(n) = \sum_{i=1}^n \sum_{j=1}^n (i \cdot j)$
- $f_4(n) = n \cdot (\log n)^4$
- $f_5(n) = n^5 (\log n)^2$
- $f_6(n) = \sqrt{3^{\sqrt{n}}}$
- $f_7(n) = \sqrt{n} \cdot 3^{n/2}$

### BẢNG BIẾN ĐỔI VÀ PHÂN LỚP:

| Hàm | Dạng biến đổi chuẩn | Big-O nhỏ nhất | Giải thích ngắn gọn |
| :--- | :--- | :---: | :--- |
| $f_1(n) = 4^{\log n} + \log \log n$ | $4^{\log_2 n} = n^{\log_2 4} = n^2$<br>$\implies n^2 + \log \log n$ | $O(n^2)$ | Áp dụng công thức đổi cơ số $a^{\log_b n} = n^{\log_b a}$, số hạng bậc cao nhất là $n^2$. |
| $f_2(n) = n \cdot \sqrt[3]{n}$ | $n \cdot n^{1/3} = n^{4/3} = n^{1.333}$ | $O(n^{4/3})$ | Tích hai lũy thừa cùng cơ số $n^{1 + 1/3} = n^{4/3}$. |
| $f_3(n) = \sum_{i=1}^n \sum_{j=1}^n (i \cdot j)$ | $\left(\sum_{i=1}^n i\right)\left(\sum_{j=1}^n j\right) = \left[\frac{n(n+1)}{2}\right]^2 = \frac{n^4 + 2n^3 + n^2}{4}$ | $O(n^4)$ | Tổng hai vòng lặp độc lập thành tích hai cấp số cộng bậc 2, nhân lại thành đa thức bậc 4. |
| $f_4(n) = n \cdot (\log n)^4$ | $n \cdot (\log n)^4$ | $O(n \log^4 n)$ | Hàm Polylogarithmic kết hợp tuyến tính, có tốc độ tăng nhỏ hơn mọi $n^{1+\epsilon}$ ($\epsilon = 1/3$). |
| $f_5(n) = n^5 (\log n)^2$ | $n^5 (\log n)^2$ | $O(n^5 \log^2 n)$ | Đa thức bậc 5 nhân logarit bậc 2. |
| $f_6(n) = \sqrt{3^{\sqrt{n}}}$ | $(3^{\sqrt{n}})^{1/2} = 3^{\frac{\sqrt{n}}{2}} = (\sqrt{3})^{\sqrt{n}}$ | $O(3^{\sqrt{n}/2})$ | Hàm mũ hạ căn bậc hai của số mũ $\sqrt{n}$, nhỏ hơn hàm mũ $a^n$ tuyến tính nhưng lớn hơn mọi đa thức $n^k$. |
| $f_7(n) = \sqrt{n} \cdot 3^{n/2}$ | $\sqrt{n} \cdot (\sqrt{3})^n$ | $O(\sqrt{n} \cdot 3^{n/2})$ | Hàm mũ thực sự với số mũ bậc nhất $n/2$, tăng nhanh nhất trong các hàm đã cho. |

### SO SÁNH CÁC HÀM VÀ KẾT LUẬN THỨ TỰ TĂNG DẦN:

1. **So sánh $f_4$ và $f_2$:**
   $f_4(n) = n \log^4 n$ và $f_2(n) = n^{4/3} = n \cdot n^{1/3}$. Vì với mọi $\epsilon > 0$, $(\log n)^4 = o(n^\epsilon)$, chọn $\epsilon = 1/3 \implies n \log^4 n < n \cdot n^{1/3} \implies f_4 < f_2$.
2. **So sánh $f_2$ và $f_1$:**
   $f_2(n) = O(n^{1.333}) < f_1(n) = O(n^2)$.
3. **So sánh $f_1, f_3, f_5$:**
   $f_1 = O(n^2) < f_3 = O(n^4) < f_5 = O(n^5 \log^2 n)$.
4. **So sánh $f_5, f_6, f_7$:**
   - Mọi đa thức $n^k = o(a^{\sqrt{n}})$ với $a > 1 \implies f_5(n) = n^5 \log^2 n < f_6(n) = 3^{\sqrt{n}/2}$.
   - Hàm mũ căn $3^{\sqrt{n}/2} <$ hàm mũ tuyến tính $3^{n/2} \implies f_6 < f_7$.

### 🏆 KẾT LUẬN: THỨ TỰ TĂNG DẦN CỦA CÁC HÀM LÀ:
$$f_4(n) < f_2(n) < f_1(n) < f_3(n) < f_5(n) < f_6(n) < f_7(n)$$

---

# PHẦN 4: BÀI TẬP TỰ LUYỆN NÂNG CAO CÓ ĐÁP ÁN

## Đề Luyện Tập 1:
Phân lớp và sắp xếp các hàm sau theo thứ tự tăng dần của Big-O nhỏ nhất:
1. $g_1(n) = 2^{3 \log_2 n} + 100 n^2$
2. $g_2(n) = n!$
3. $g_3(n) = 2^{2^n}$
4. $g_4(n) = \sqrt{n \log n}$
5. $g_5(n) = n^{\sqrt{n}}$
6. $g_6(n) = 3^n$
7. $g_7(n) = \log(n^n)$

### Đáp án tóm tắt:
- $g_4(n) = \sqrt{n \log n} = O(n^{0.5} \log^{0.5} n)$
- $g_7(n) = \log(n^n) = n \log n = O(n \log n)$
- $g_1(n) = 2^{\log_2(n^3)} + 100n^2 = n^3 + 100n^2 = O(n^3)$
- $g_6(n) = 3^n = O(3^n)$
- $g_5(n) = n^{\sqrt{n}} = (2^{\log_2 n})^{\sqrt{n}} = 2^{\sqrt{n}\log_2 n}$ (Nằm giữa $a^{\sqrt{n}}$ và $a^n$)
- $g_2(n) = n! \approx \sqrt{2\pi n}(n/e)^n = O(n^n)$
- $g_3(n) = 2^{2^n}$ (Hàm siêu mũ tăng nhanh nhất)

**Thứ tự tăng dần:** $g_4 < g_7 < g_1 < g_6 < g_5 < g_2 < g_3$.
