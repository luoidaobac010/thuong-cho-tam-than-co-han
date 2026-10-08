# Ôn thi CS112 - Buổi 1: Big-O từ đầu

Quy ước: công thức viết bằng ký tự thường. Khi chép lên giấy thi thì đổi sang ký hiệu toán: thuộc = ∈, tồn tại = ∃, với mọi = ∀, <= = ≤, c > 0 (c thực) = c ∈ R⁺, n0 (tự nhiên) = n₀ ∈ N.

---

# PHẦN A. Big-O từ đầu

## 1. Big-O dùng để làm gì
Hai bạn cùng viết chương trình tìm một số trong danh sách n số.
- Bạn A xét từng số một, nên chạy khoảng **n bước**.
- Bạn B so mỗi số với tất cả các số còn lại, nên chạy khoảng **n^2 bước**.

Với n = 1000 thì A chạy 1000 bước, còn B chạy 1.000.000 bước. Big-O là cách viết gọn và chính xác câu "chương trình này nhanh cỡ nào khi n lớn".

## 2. T(n) là gì
**T(n) là số bước chương trình chạy khi đầu vào có n phần tử.**

Ví dụ T(n) = 3n + 5:
- n = 1 thì 3*1 + 5 = 8 bước
- n = 10 thì 35 bước
- n = 100 thì 305 bước

## 3. Ý chính: "không vượt quá c lần"
Câu hỏi: **3n + 5 có tăng nhanh hơn n không?** Thử so với 4n:

| n | 3n+5 | 4n | 3n+5 <= 4n ? |
|---|---|---|---|
| 1 | 8 | 4 | sai |
| 2 | 11 | 8 | sai |
| 4 | 17 | 16 | sai |
| 5 | 20 | 20 | **đúng** |
| 10 | 35 | 40 | **đúng** |
| 100 | 305 | 400 | **đúng** |

Từ n = 5 trở đi thì 3n + 5 luôn nhỏ hơn hoặc bằng 4n. Vì vậy **3n + 5 thuộc O(n)**. Có 2 con số quan trọng:
- **c = 4**: số lần nhân thêm cho n
- **n0 = 5**: mốc bắt đầu đúng mãi mãi

## 4. Đọc định nghĩa từng mảnh
```
T(n) thuộc O(g(n))  <=>  tồn tại c > 0, tồn tại n0
                         sao cho T(n) <= c * g(n) với mọi n >= n0
```

| Mảnh | Nghĩa | Trong ví dụ |
|---|---|---|
| T(n) | hàm cần chứng minh | 3n + 5 |
| g(n) | hàm đem ra so | n |
| tồn tại c > 0 | tìm được một hệ số dương | c = 4 |
| tồn tại n0 | tìm được một mốc | n0 = 5 |
| T(n) <= c*g(n) với mọi n >= n0 | từ mốc đó trở đi luôn đúng | 3n+5 <= 4n khi n >= 5 |

Làm bài chứng minh Big-O chỉ có một việc: **tìm c và n0**, rồi chỉ ra bất đẳng thức đúng với mọi n từ n0 trở đi.

## 5. Tìm c cho nhanh
Mẹo: **với n >= 1 thì mỗi số hằng nhỏ hơn hoặc bằng số đó nhân n**, ví dụ 5 <= 5n. Áp dụng cho 3n + 5:
```
Với n >= 1:  5 <= 5n
Nên:         3n + 5 <= 3n + 5n = 8n
```
Chọn **c = 8, n0 = 1**. Cách này dễ hơn c = 4, n0 = 5, và cả hai đều đúng. Đề chỉ cần một cặp c, n0 nào đó.

## 6. Cách trình bày để được điểm (theo cô, b10:407-413)
```
Ta cần chứng minh 3n + 5 thuộc O(n).
Với mọi n >= 1 ta có 5 <= 5n.
Suy ra T(n) = 3n + 5 <= 3n + 5n = 8n, với mọi n >= 1.
Chọn c = 8 > 0, n0 = 1, ta có T(n) <= c * g(n) với mọi n >= n0.
Theo định nghĩa Big O, ta có điều cần chứng minh.
```
Lỗi bị trừ điểm:
- Thiếu (n), viết "T thuộc O(g)" thay vì T(n), g(n).
- Viết tắt "T thuộc O(g) => T <= c*g" thì cả câu 0 điểm.
- Không nêu c và n0 cụ thể.
- Thiếu câu kết luận.

## 7. Bài điền chỗ trống: 5n + 7 thuộc O(n)
```
Với n >= 1 ta có 7 <= ___ n.
Suy ra 5n + 7 <= 5n + ___ n = ___ n.
Chọn c = ___ , n0 = ___ .
```
Đáp án: **7, 7, 12, 12, 1**.

Kiểm bằng số: n = 1 thì 12 <= 12, n = 10 thì 57 <= 120. Lời giải đầy đủ:
```
Với n >= 1 ta có 7 <= 7n.
Suy ra 5n + 7 <= 5n + 7n = 12n, với mọi n >= 1.
Chọn c = 12 > 0, n0 = 1, ta có T(n) <= c * g(n) với mọi n >= n0.
Theo định nghĩa Big O, ta có điều cần chứng minh.
```

---

# PHẦN B. Giải chi tiết 2 bài

## Bài 1: `2n^3 + 10n^2 + 3` thuộc `O(n^3)`

**Mục tiêu:** tìm c, n0 để `2n^3 + 10n^2 + 3 <= c * n^3` với mọi n >= n0.

**Ý tưởng:** bên phải chỉ có n^3, nên biến 2 hạng tử nhỏ (10n^2 và 3) thành n^3.

**Bước 1:** chọn n0 = 1, tức là chỉ xét n >= 1.

**Bước 2:** biến hạng tử nhỏ thành n^3.
- Vì n >= 1 nên n^2 <= n^3 (nhân 2 vế của n >= 1 với n^2). Kiểm: n = 5 thì 25 <= 125.
- Suy ra `10n^2 <= 10n^3`.
- Vì n >= 1 nên n^3 >= 1, tức `1 <= n^3`. Suy ra `3 <= 3n^3`. Kiểm: n = 2 thì 3 <= 24.

**Bước 3:** cộng lại.
```
2n^3 + 10n^2 + 3  <=  2n^3 + 10n^3 + 3n^3  =  15n^3
```
Hệ số: 2 + 10 + 3 = 15, nên **c = 15**.

**Lời giải viết vào bài thi:**
```
Với n >= 1 ta có n^2 <= n^3 và 1 <= n^3.
Suy ra 2n^3 + 10n^2 + 3 <= 2n^3 + 10n^3 + 3n^3 = 15n^3, với mọi n >= 1.
Chọn c = 15 > 0, n0 = 1, ta có T(n) <= c * g(n) với mọi n >= n0.
Theo định nghĩa Big O, ta có điều cần chứng minh.
```

## Bài 2: `n(n+1)/2` thuộc `O(n^2)`

**Bước 1:** nhân ra trước.
```
n(n+1)/2 = (n^2 + n)/2 = n^2/2 + n/2
```
**Bước 2:** với n >= 1 thì n <= n^2, nên `n/2 <= n^2/2`.

**Bước 3:** cộng lại.
```
n(n+1)/2 = n^2/2 + n/2  <=  n^2/2 + n^2/2  =  n^2
```
Hệ số ra 1, nên **c = 1, n0 = 1**. Kiểm: n = 1 thì 1 <= 1, n = 2 thì 3 <= 4, n = 10 thì 55 <= 100.

**Lời giải viết vào bài thi:**
```
Ta có n(n+1)/2 = n^2/2 + n/2.
Với n >= 1 ta có n <= n^2, nên n/2 <= n^2/2.
Suy ra n(n+1)/2 <= n^2/2 + n^2/2 = n^2, với mọi n >= 1.
Chọn c = 1 > 0, n0 = 1, ta có T(n) <= c * g(n) với mọi n >= n0.
Theo định nghĩa Big O, ta có điều cần chứng minh.
```

## Quy tắc chung
1. Chọn n0 = 1.
2. Với n >= 1, hạng tử bậc thấp luôn <= hạng tử bậc cao nhất (n <= n^2 <= n^3, và 3 <= 3n^3).
3. Đổi hết thành hạng tử bậc cao nhất rồi cộng hệ số lại. Tổng đó là c.

---

# PHẦN C. Bài tự làm

## C1. Bài đang chờ
Chứng minh `4n^2 + 6n + 9` thuộc `O(n^2)`:
```
Với n >= 1 ta có n <= ___ và 1 <= ___.
Suy ra 4n^2 + 6n + 9 <= 4n^2 + ___ n^2 + ___ n^2 = ___ n^2, với mọi n >= 1.
Chọn c = ___, n0 = ___.
```

## C2. Bài khó (làm sau)
Chứng minh `7n^2` thuộc `O(n^2 - 80n)`. Hạng tử âm nằm ở vế bị so sánh nên không bỏ được. Gợi ý: thử c = 8, chuyển vế, tìm n0 (cô chữa ở b4:223-231).

---

# Nguồn
- Luật chấm và cách trình bày: `bai_tap/Đề thi mẫu/Đề cương đem theo/Khung_Nhan_Dang_De_CS112.md` mục 2.1 (b4:213-231, b10:407-415).
