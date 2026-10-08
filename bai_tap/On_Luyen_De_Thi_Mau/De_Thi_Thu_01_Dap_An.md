# ĐÁP ÁN ĐỀ THI THỬ SỐ 01 - CS112

---

## PHẦN 1: CÂU TRẢ LỜI NGẮN (6 điểm)

### Câu 1 (3 điểm) Ký hiệu tiệm cận
**a. (1.5 điểm) Dùng định nghĩa chứng minh:**
1. $f(n) = 3n^2 + 5n - 2 \in \Theta(n^2)$
   - Định nghĩa: $\exists c_1, c_2 > 0$ và $n_0 > 0$ sao cho $c_1 n^2 \le 3n^2 + 5n - 2 \le c_2 n^2, \forall n \ge n_0$.
   - Giới hạn trên: $3n^2 + 5n - 2 \le 3n^2 + 5n^2 = 8n^2$. Chọn $c_2 = 8$. (Đúng với $n \ge 1$).
   - Giới hạn dưới: Xét $3n^2 + 5n - 2 \ge 3n^2 - 2 \ge 2n^2$ khi $n^2 \ge 2 \Rightarrow n \ge \sqrt{2}$. Chọn $c_1 = 2$, $n_0 = 2$.
   - Kết luận: Đúng định nghĩa $\Theta(n^2)$.
2. $g(n) = n^3 + \log_2 n \in \Omega(n^3)$
   - Định nghĩa: $\exists c > 0, n_0 > 0$ sao cho $n^3 + \log_2 n \ge c \cdot n^3, \forall n \ge n_0$.
   - Vì $\log_2 n > 0$ với mọi $n > 1$, ta có: $n^3 + \log_2 n \ge n^3$.
   - Chọn $c = 1, n_0 = 2$. Điều kiện được thỏa mãn.

**b. (1.5 điểm) Sắp xếp tăng dần của Big-O:**
Rút gọn hàm:
- $5\log_2(n^3) = 15 \log_2 n \in \Theta(\log n)$
- $\sqrt[3]{n} = n^{1/3} \in \Theta(n^{1/3})$
- $n \log_2 n \in \Theta(n \log n)$
- $0.5n^4 + n^2 \in \Theta(n^4)$
- $3^n \in \Theta(3^n)$
- $n! \in \Theta(n!)$
Thứ tự: $5\log_2(n^3)$ < $\sqrt[3]{n}$ < $n \log_2 n$ < $0.5n^4 + n^2$ < $3^n$ < $n!$

---

### Câu 2 (3 điểm) Phân tích thuật toán
**a. (1.5 điểm)**
1. Lời gọi hàm sẽ in ra tổng số lần vòng lặp trong (biến count) được thực thi.
2. Vòng lặp ngoài $i$ chạy: $1, 2, 4, ..., 2^k \le n \Rightarrow k = \lfloor\log_2 n\rfloor$. Vòng lặp ngoài chạy khoảng $\log_2 n$ lần.
   Vòng lặp trong $j$ chạy $n$ lần độc lập với $i$.
   Tổng số phép toán = $\sum_{i=0}^{\log_2 n} n = n \cdot \log_2 n$.
   Vậy độ phức tạp là $O(n \log n)$.

**b. (1.5 điểm)**
1. Phương trình đệ quy: 
   - Phần không đệ quy (vòng lặp $i$): $O(n)$ thời gian.
   - Gọi đệ quy: 1 lần gọi với kích thước $n/3$, nhưng nhân với hằng số 3 ở ngoài, tức là chỉ gọi 1 nhánh đệ quy $T(n/3)$. (Lưu ý code là `3 * recurse(...)` chứ không phải gọi hàm 3 lần).
   - $T(n) = T(n/3) + O(n)$.
2. Giải bằng định lý Master:
   - $a = 1, b = 3, f(n) = n$.
   - $n^{\log_b a} = n^{\log_3 1} = n^0 = 1$.
   - So sánh $f(n) = n$ và $n^0$: Ta có $f(n) \in \Omega(n^{0+\epsilon})$ với $\epsilon = 1$.
   - Kiểm tra điều kiện Regularity: $a \cdot f(n/b) = 1 \cdot (n/3) \le c \cdot n$ (chọn $c = 1/3 < 1$).
   - Kết luận (Trường hợp 3 Master Theorem): $T(n) \in \Theta(n)$.

---

## PHẦN 2: TỰ LUẬN (6 điểm)

### Câu 3 (2 điểm) Dò mìn (Minesweeper)
**Ý tưởng:**
Duyệt qua từng ô $(i, j)$ trong ma trận. Nếu $A[i][j] == 0$, ta sẽ kiểm tra 8 ô xung quanh nó. Đếm số mìn (số lượng ô có giá trị $-1$) và gán lại cho $A[i][j]$.

**Mã giả:**
```cpp
Minesweeper(A, m, n):
    // Các hướng di chuyển: trên, dưới, trái, phải và 4 góc chéo
    dx = [-1, -1, -1, 0, 0, 1, 1, 1]
    dy = [-1, 0, 1, -1, 1, -1, 0, 1]

    for i = 0 to m-1:
        for j = 0 to n-1:
            if A[i][j] == 0:
                mines_count = 0
                for k = 0 to 7: // Kiểm tra 8 hướng
                    nx = i + dx[k]
                    ny = j + dy[k]
                    // Kiểm tra (nx, ny) có nằm trong ma trận không
                    if (nx >= 0 and nx < m and ny >= 0 and ny < n):
                        if A[nx][ny] == -1:
                            mines_count = mines_count + 1
                A[i][j] = mines_count
```
**Độ phức tạp:**
- Hai vòng lặp lồng nhau duyệt $m \times n$ phần tử.
- Bên trong, kiểm tra 8 hướng mất thời gian hằng số $O(1)$.
- Độ phức tạp thời gian: $O(m \cdot n)$. Không gian: $O(1)$ (tính trực tiếp trên ma trận).

### Câu 4 (2 điểm) Khôi phục địa chỉ IP
**Ý tưởng:** 
Dùng đệ quy quay lui (Backtracking). Duyệt từng đoạn con của chuỗi $S$. Tại mỗi bước, ta cắt một đoạn dài 1, 2 hoặc 3 ký tự, kiểm tra xem nó có hợp lệ không (giá trị $\le 255$ và không có leading zero). Nếu hợp lệ, đi tiếp. Đạt 4 đoạn và hết chuỗi thì nhận.

**Mã giả:**
```cpp
RestoreIP(S):
    result = empty list
    Backtrack(S, start_idx, current_ip_parts, result)
    return result

Backtrack(S, index, parts, result):
    if parts.size == 4:
        if index == S.length: // Đã cắt hết chuỗi và có đủ 4 phần
            result.append(join(parts, "."))
        return
    
    // Cắt từ 1 đến 3 ký tự từ vị trí index
    for length = 1 to 3:
        if index + length <= S.length:
            segment = S[index ... index+length-1]
            if isValid(segment):
                parts.append(segment)
                Backtrack(S, index + length, parts, result)
                parts.pop() // Backtrack

isValid(segment):
    if segment.length > 1 and segment[0] == '0':
        return false // Leading zero
    if toInteger(segment) > 255:
        return false // Vượt quá 255
    return true
```
**Độ phức tạp:**
Tại mỗi phần (trong 4 phần), ta có tối đa 3 lựa chọn (độ dài 1, 2, 3). Do đó, tổng số cấu hình tối đa là $3^4 = 81$.
- Thời gian: $O(3^4) = O(1)$ vì số lượng cấu hình bị giới hạn cứng.
- Không gian: $O(1)$ cho chiều sâu ngăn xếp đệ quy (tối đa 4 tầng).

### Câu 5 (2 điểm) Dãy con tăng dài nhất (LIS)
1. **Cấu trúc con tối ưu:**
Gọi $L[i]$ là độ dài dãy con tăng dài nhất kết thúc tại phần tử $A[i]$.
Để tính $L[i]$, ta có thể nối $A[i]$ vào phía sau một dãy con tăng kết thúc tại $A[j]$ (với $j < i$) miễn là $A[j] < A[i]$. Ta sẽ chọn $j$ sao cho $L[j]$ lớn nhất.
**Hệ thức truy hồi:**
$L[i] = 1 + \max( \{L[j]\} )$ với mọi $j < i$ và $A[j] < A[i]$. Nếu không có $j$ nào thoả, $L[i] = 1$.
Độ dài dãy con dài nhất của cả mảng là $\max( \{L[1], L[2], ..., L[n]\} )$.

2. **Mã giả (Quy hoạch động):**
```cpp
LIS(A, n):
    // Khởi tạo mảng L, L[i] = 1 với mọi i
    L = array of size n, initialized to 1
    max_len = 1

    for i = 1 to n-1: // Chỉ số từ 0 đến n-1, giả sử 1-indexed ở đây dùng 0-indexed
        for j = 0 to i-1:
            if A[j] < A[i] and L[i] < L[j] + 1:
                L[i] = L[j] + 1
        
        if L[i] > max_len:
            max_len = L[i]
            
    return max_len
```
**Độ phức tạp:**
- Hai vòng lặp lồng nhau duyệt qua $i$ và $j$, số phép so sánh là $1 + 2 + ... + (n-1) = \frac{n(n-1)}{2}$.
- Độ phức tạp thời gian: $O(n^2)$.
- Độ phức tạp không gian: $O(n)$ để lưu mảng $L$.
