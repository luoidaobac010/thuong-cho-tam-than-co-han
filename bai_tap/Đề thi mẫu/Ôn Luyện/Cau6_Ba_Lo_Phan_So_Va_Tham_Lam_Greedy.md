# CÂU 6: BÀI TOÁN BA LÔ PHÂN SỐ (FRACTIONAL KNAPSACK) & PHƯƠNG PHÁP THAM LAM (GREEDY)
## MÔN: PHÂN TÍCH VÀ THIẾT KẾ THUẬT TOÁN (CS112) - CÔ HUỲNH THỊ THANH THƯƠNG

---

# PHẦN 1: MÔ HÌNH HÓA BÀI TOÁN TỐI ƯU

## 1. Phát biểu toán học của bài toán
Cho $n$ đồ vật, mỗi đồ vật $i$ ($1 \le i \le n$) có:
- Trọng lượng $w_i > 0$.
- Giá trị $p_i > 0$.
Một ba lô có sức chứa tối đa là $M > 0$.
Mỗi đồ vật có thể được chia nhỏ tùy ý, với tỉ lệ lấy là $x_i \in [0, 1]$.

Bài toán tối ưu được mô hình hóa như sau:
- **Biến quyết định:** $X = (x_1, x_2, \dots, x_n)$ với $0 \le x_i \le 1$ ($\forall i = 1..n$).
- **Hàm mục tiêu (Cần tối đa hóa tổng giá trị):**
  $$\max P(X) = \sum_{i=1}^n p_i \cdot x_i$$
- **Hệ ràng buộc (Tổng trọng lượng không vượt quá sức chứa ba lô):**
  $$\sum_{i=1}^n w_i \cdot x_i \le M$$
  $$0 \le x_i \le 1 \quad (\forall i = 1, 2, \dots, n)$$

---

# PHẦN 2: THIẾT KẾ THUẬT TOÁN THAM LAM (GREEDY ALGORITHM)

## 1. Chiến lược tham lam (Greedy Choice)
- **Đơn giá giá trị (Value Density):** Tính tỷ số giá trị trên một đơn vị trọng lượng của từng đồ vật:
  $$v_i = \frac{p_i}{w_i} \quad (\forall i = 1..n)$$
- **Quy tắc lựa chọn:**
  1. Luôn ưu tiên chọn đồ vật có đơn giá $v_i$ lớn nhất trước.
  2. Nếu sức chứa còn lại $M_{con} \ge w_i$, ta lấy toàn bộ đồ vật $i$ ($x_i = 1$) và giảm sức chứa: $M_{con} = M_{con} - w_i$.
  3. Nếu sức chứa còn lại $0 < M_{con} < w_i$, ta lấy một phần đồ vật $i$: $x_i = \frac{M_{con}}{w_i}$, khi đó ba lô đầy ($M_{con} = 0$) và thuật toán kết thúc.
  4. Các đồ vật còn lại không được chọn ($x_i = 0$).

## 2. Mã giả thuật toán Tham lam (Đánh số bước chuẩn)

```text
Thuật toán Fractional_Knapsack_Greedy(n, M, w, p):
Đầu vào:
  - n: Số lượng đồ vật
  - M: Sức chứa tối đa của ba lô
  - w[1..n]: Mảng trọng lượng các đồ vật
  - p[1..n]: Mảng giá trị các đồ vật
Đầu ra: Mảng x[1..n] tỉ lệ lấy của từng đồ vật và tổng giá trị lớn nhất max_val.

1.  Khởi tạo mảng x[1..n] = 0 cho tất cả đồ vật
2.  Khởi tạo max_val = 0
3.  Khởi tạo capacity_left = M
4.  Tính tỷ số đơn giá v[i] = p[i] / w[i] cho mọi i từ 1 đến n
5.  Sắp xếp các đồ vật theo thứ tự đơn giá v[i] giảm dần
6.  Cho i chạy từ 1 đến n thực hiện:
7.      Nếu capacity_left == 0 thì:
8.          Dừng vòng lặp
9.      Nếu w[i] <= capacity_left thì:
10.         x[i] = 1.0                             // Lấy toàn bộ đồ vật i
11.         capacity_left = capacity_left - w[i]
12.         max_val = max_val + p[i]
13.     Ngược lại:
14.         x[i] = capacity_left / w[i]            // Chỉ lấy một phần vừa đủ ba lô
15.         max_val = max_val + p[i] * x[i]
16.         capacity_left = 0                      // Ba lô đã đầy
17. Trả về (x, max_val)
```

## 3. Phân tích độ phức tạp
- **Bước tính đơn giá (Bước 4):** $O(n)$.
- **Bước sắp xếp đồ vật (Bước 5):** $O(n \log n)$ (sử dụng MergeSort hoặc QuickSort).
- **Vòng lặp tham lam chọn đồ vật (Bước 6-16):** $O(n)$.
- **Tổng độ phức tạp thời gian:** $T(n) = O(n \log n)$.
- **Độ phức tạp không gian:** $O(n)$ để lưu mảng tỷ số và kết quả.

---

# PHẦN 3: ÁP DỤNG THUẬT TOÁN CHO BÀI TOÁN CỤ THỂ (ĐỀ THI 2025)

## 1. Dữ liệu đề bài:
- Số đồ vật: $n = 3$.
- Sức chứa ba lô: $M = 20\text{ kg}$.
- Trọng lượng: $(w_1, w_2, w_3) = (18, 15, 10)$.
- Giá trị: $(p_1, p_2, p_3) = (25, 24, 15)$.

---

## 2. Các bước tính toán chi tiết:

### Bước 1: Tính đơn giá $v_i = \frac{p_i}{w_i}$ của 3 đồ vật
- Đồ vật 1: $v_1 = \frac{25}{18} \approx 1.3889$
- Đồ vật 2: $v_2 = \frac{24}{15} = 1.6000$
- Đồ vật 3: $v_3 = \frac{15}{10} = 1.5000$

### Bước 2: Sắp xếp các đồ vật theo đơn giá giảm dần
Thứ tự ưu tiên chọn là: **Đồ vật 2** ($v_2 = 1.60$) $\rightarrow$ **Đồ vật 3** ($v_3 = 1.50$) $\rightarrow$ **Đồ vật 1** ($v_1 \approx 1.39$).

### Bước 3: Thực hiện chiến lược Tham lam

| Bước | Đồ vật xét | Đơn giá $v_i$ | Trọng lượng $w_i$ | Sức chứa còn lại trước khi chọn | Quyết định chọn $x_i$ | Trọng lượng đã lấy | Giá trị nhận được | Sức chứa còn lại sau khi chọn |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | Đồ vật 2 | $1.60$ | $15\text{ kg}$ | $20\text{ kg}$ | $x_2 = 1.0$ (Lấy hết) | $15\text{ kg}$ | $24.0$ | $20 - 15 = 5\text{ kg}$ |
| **2** | Đồ vật 3 | $1.50$ | $10\text{ kg}$ | $5\text{ kg}$ | $x_3 = \frac{5}{10} = 0.5$ (Lấy 1/2) | $5\text{ kg}$ | $15 \times 0.5 = 7.5$ | $5 - 5 = 0\text{ kg}$ |
| **3** | Đồ vật 1 | $1.39$ | $18\text{ kg}$ | $0\text{ kg}$ | $x_1 = 0.0$ (Không lấy) | $0\text{ kg}$ | $0.0$ | $0\text{ kg}$ |

---

## 3. Kết luận nghiệm tối ưu:
- **Phương án chọn (Tỉ lệ lấy các đồ vật):**
  $$X = (x_1, x_2, x_3) = (0, 1, 0.5)$$
  *(tức không lấy đồ vật 1, lấy toàn bộ đồ vật 2, và lấy 50% đồ vật 3)*
- **Tổng trọng lượng của ba lô:**
  $$W = 18 \times 0 + 15 \times 1 + 10 \times 0.5 = 20\text{ kg} \quad (\le M = 20\text{ kg})$$
- **Tổng giá trị lớn nhất đạt được:**
  $$P_{max} = 25 \times 0 + 24 \times 1 + 15 \times 0.5 = 24 + 7.5 = \mathbf{31.5}$$
