# ĐÁP ÁN CHUYÊN ĐỀ 2: THIẾT KẾ THUẬT TOÁN

---

## BÀI 1: QUAY LUI (BACKTRACKING) - HOÁN VỊ
**Ý tưởng:** Dùng mảng đánh dấu `visited` để biết chữ số nào đã được chọn. Tại mỗi vị trí $i$ (từ 0 đến $N-1$), ta thử đặt một chữ số chưa được đánh dấu. Lặp lại đến khi độ dài số đủ $N$.

**Mã giả:**
```cpp
Permute(A, N):
    // A: mảng chứa N chữ số
    visited = array of size N, filled with false
    current_perm = empty array
    result = empty list
    Backtrack(A, N, visited, current_perm, result)
    return result

Backtrack(A, N, visited, current_perm, result):
    if current_perm.length == N:
        result.append(current_perm)
        return
    
    for i = 0 to N - 1:
        if not visited[i]:
            visited[i] = true
            current_perm.append(A[i])
            
            Backtrack(A, N, visited, current_perm, result)
            
            // Quay lui (trả lại trạng thái)
            current_perm.pop()
            visited[i] = false
```
**Độ phức tạp:**
Có $N!$ hoán vị, mỗi hoán vị mất $O(N)$ để copy kết quả. Thời gian: $O(N \cdot N!)$. Không gian: $O(N)$ cho mảng nhớ tạm và call stack đệ quy.

---

## BÀI 2: CHIA ĐỂ TRỊ (DIVIDE AND CONQUER) - LŨY THỪA NHANH
**Ý tưởng:**
- Nếu $n = 0$: $x^0 = 1$.
- Nếu $n$ chẵn: $x^n = (x^{n/2}) \cdot (x^{n/2})$.
- Nếu $n$ lẻ: $x^n = x \cdot (x^{n/2}) \cdot (x^{n/2})$.

**Mã giả:**
```cpp
Power(x, n):
    if n == 0: 
        return 1
    
    half = Power(x, n / 2)
    
    if n % 2 == 0:
        return half * half
    else:
        return x * half * half
```
**Độ phức tạp:**
Phương trình đệ quy: $T(n) = T(n/2) + O(1)$. (Chỉ gọi đệ quy 1 lần vì ta lưu `half`).
Theo Master Theorem: $a=1, b=2, f(n)=1 \Rightarrow T(n) \in O(\log n)$.

---

## BÀI 3: THAM LAM (GREEDY) - XẾP LỊCH
**Ý tưởng Tham lam:**
Luôn ưu tiên chọn hoạt động **kết thúc sớm nhất** (có $f_i$ nhỏ nhất) để để lại nhiều thời gian nhất cho các hoạt động tiếp theo.
Giả sử danh sách hoạt động đã được sắp xếp tăng dần theo thời gian kết thúc $f$.

**Mã giả:**
```cpp
ActivitySelection(s, f, n): // s: start times, f: finish times (đã sort)
    selected = empty list
    selected.append(hoạt động 1) // Chọn hoạt động kết thúc sớm nhất
    last_finish = f[1]
    
    for i = 2 to n:
        if s[i] >= last_finish: // Không xung đột
            selected.append(hoạt động i)
            last_finish = f[i]
            
    return selected
```
**Độ phức tạp:**
Vòng lặp duyệt 1 lần qua mảng $n$ phần tử $\Rightarrow O(n)$.
*(Lưu ý: Nếu mảng chưa sắp xếp, tốn thêm $O(n \log n)$ để sort).*

---

## BÀI 4.1: QUY HOẠCH ĐỘNG - CÁI TÚI 0/1
1. **Cấu trúc con tối ưu:** 
Gọi $F(i, j)$ là tổng giá trị lớn nhất khi chọn trong $i$ đồ vật đầu tiên, với sức chứa tối đa của túi là $j$.
2. **Hệ thức truy hồi:**
Xét đồ vật thứ $i$ có khối lượng $w_i$, giá trị $v_i$.
- Nếu $w_i > j$ (nặng quá, không bỏ vào được): $F(i, j) = F(i-1, j)$.
- Nếu $w_i \le j$ (có thể bỏ vào): 
  - Không chọn: $F(i-1, j)$.
  - Có chọn: $v_i + F(i-1, j - w_i)$.
  $\Rightarrow F(i, j) = \max(F(i-1, j), v_i + F(i-1, j - w_i))$.
- Cơ sở đệ quy: $F(0, j) = 0$ và $F(i, 0) = 0$.

3. **Mã giả:**
```cpp
Knapsack(w, v, n, W):
    F = matrix of size (n+1) x (W+1), initialized to 0
    
    for i = 1 to n:
        for j = 1 to W:
            if w[i] > j:
                F[i][j] = F[i-1][j]
            else:
                F[i][j] = max(F[i-1][j], v[i] + F[i-1][j - w[i]])
                
    return F[n][W]
```
**Độ phức tạp:** $O(n \cdot W)$ thời gian và không gian.

---

## BÀI 4.2: QUY HOẠCH ĐỘNG - CẮT THANH SẮT
**Hệ thức truy hồi:**
Gọi $DP[i]$ là doanh thu tối đa có thể kiếm được từ thanh sắt dài $i$.
Ta có thể cắt một đoạn độ dài $j$ ($1 \le j \le i$) để bán với giá $P[j]$, và tiếp tục tìm cách bán tối ưu đoạn sắt còn lại $i-j$.
$DP[i] = \max_{1 \le j \le i} (P[j] + DP[i-j])$.
Cơ sở đệ quy: $DP[0] = 0$.

**Mã giả (Bottom-up DP):**
```cpp
RodCutting(P, n):
    DP = array of size n+1, initialized to 0
    
    for i = 1 to n: // Tính DP[i] cho từng độ dài từ 1 đến n
        max_val = 0
        for j = 1 to i: // Thử cắt đoạn độ dài j
            if max_val < P[j] + DP[i - j]:
                max_val = P[j] + DP[i - j]
        DP[i] = max_val
        
    return DP[n]
```
**Độ phức tạp:** 
2 vòng lặp lồng nhau $\Rightarrow O(n^2)$ thời gian. Không gian $O(n)$ cho mảng nhớ DP.
