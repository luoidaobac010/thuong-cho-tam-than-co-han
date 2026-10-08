# BẢNG TỔNG HỢP ÔN TẬP MÔN PTTKTT (CS112) - TỜ A4 VIẾT TAY
*(Trích xuất toàn bộ các mục "Chép lên tờ A4" từ Giao_Trinh_Tu_Hoc_7_Ngay_CS112_DAY_DU.pdf)*

## MẶT 1 - PHẦN PHÂN TÍCH

### 1. Ký hiệu tiệm cận và Biến đổi
**Định nghĩa chuẩn (không dùng lim, bắt buộc đủ lượng từ):**
*   **Big-O:** $f(n) \in O(g(n)) \iff \exists c > 0, \exists n_0 \ge 0, \forall n \ge n_0 : 0 \le f(n) \le c \cdot g(n)$
*   **Big-$\Omega$:** $f(n) \in \Omega(g(n)) \iff \exists c > 0, \exists n_0 \ge 0, \forall n \ge n_0 : 0 \le c \cdot g(n) \le f(n)$
*   **Big-$\Theta$:** $f(n) \in \Theta(g(n)) \iff \exists c_1, c_2 > 0, \exists n_0 \ge 0, \forall n \ge n_0 : 0 \le c_1 \cdot g(n) \le f(n) \le c_2 \cdot g(n)$

**Thang chuẩn tăng dần:**
$1 \prec \log \log n \prec \log n \prec \log^2 n \prec \sqrt{n} \prec n \prec n \log n \prec n^2 \prec n^3 \prec n^{\log n} \prec 2^{\sqrt{n}} \prec 2^n \prec n \cdot 2^n \prec 3^n \prec n! \prec n^n$

**Công cụ đưa hàm về dạng chuẩn:**
*   $a^{\log_b n} = n^{\log_b a}$
*   $\sqrt[k]{n} = n^{1/k}$
*   $\log(x^k) = k \log x$

### 2. Các công thức tổng cần nhớ
*   **Đổi cận (đếm số hạng):** $\sum_{i=l}^u 1 = u - l + 1$
*   **Cấp số cộng:** $\sum_{i=1}^n i = \frac{n(n+1)}{2}$. **Tổng bình phương:** $\sum_{i=1}^n i^2 = \frac{n(n+1)(2n+1)}{6}$
*   **Tổng lập phương:** $\sum_{i=1}^n i^3 = \left(\frac{n(n+1)}{2}\right)^2$
*   **Cấp số nhân:** $\sum_{i=0}^k a^i = \frac{a^{k+1}-1}{a-1} \quad (a \neq 1)$
*   **Chuỗi điều hòa:** $\sum_{i=1}^n \frac{1}{i} = H_n \approx \ln n + \gamma \in \Theta(\log n)$
*   **Telescoping:** $\sum_{i=1}^n \frac{1}{i(i+1)} = 1 - \frac{1}{n+1} = \frac{n}{n+1}$
*   **Tổng log (Stirling):** $\sum_{i=1}^n \lg i = \lg(n!) \in \Theta(n \log n)$

### 3. Phương trình đệ quy
**Công thức khung:**
$T(n) = (\text{số lời gọi đệ quy}) \times T(\text{kích thước bài con}) + f(n)$
*(Trong đó $f(n)$ gồm chi phí phân chia và tổng hợp).*
$T(\text{cơ sở}) = \text{chi phí ở nhánh dừng (thường là hằng số } c_1)$

**Quy tắc phương trình đặc trưng:**
Với $T(n) = a_1T(n-1) + a_2T(n-2) + \dots$:
1. Viết PT đặc trưng: $x^m = a_1x^{m-1} + a_2x^{m-2} + \dots$ (chuyển hết về 1 vế = 0).
2. **Nghiệm đơn** $r_1, r_2 \implies T(n) = Ar_1^n + Br_2^n$.
3. **Nghiệm kép** $r$ (bội 2) $\implies T(n) = (A + Bn)r^n$.
4. **Vế phải khác 0:** cộng thêm một nghiệm riêng; nếu dạng nghiệm riêng trùng nghiệm đặc trưng bội $m$ thì nhân thêm $n^m$.
5. Dùng điều kiện đầu $(T(0), T(1),...)$ giải hệ tìm $A, B$.

**Năm hàm sinh đáng nhớ:**
*   $\frac{1}{1-x} = \sum_{n \ge 0} x^n$
*   $\frac{x}{(1-x)^2} = \sum_{n \ge 0} n x^n$
*   $\frac{1}{(1-x)^2} = \sum_{n \ge 0} (n+1) x^n$
*   $\frac{1}{(1-x)^3} = \sum_{n \ge 0} \frac{(n+1)(n+2)}{2} x^n$
*   $\frac{1}{1-ax} = \sum_{n \ge 0} a^n x^n$

---
<div style="page-break-after: always"></div>

## MẶT 2 - PHẦN THIẾT KẾ

### 4. Ba chiến lược "Để trị"
*   **Chia để trị (Divide):** Từ 2 bài con trở lên, cùng dạng, nhỏ hơn.
*   **Giảm để trị (Decrease):** Đúng 1 bài con cùng dạng, nhỏ hơn (thường bớt 1 phần tử).
*   **Biến đổi để trị (Transform):** Đổi thành bài toán khác hẳn $Q$, giải $Q$ ra là có lời giải bài gốc $B$.

### 5. Khung Quay Lui (Backtracking)
**4 ý mô hình hóa bắt buộc:**
1. **Biểu diễn lời giải:** Lời giải là bộ $X = (x_1, \dots, x_n)$. Nói rõ mỗi $x_i$ là gì và bộ có mấy thành phần.
2. **Tập ứng viên $S_i$:** Mỗi bước có những lựa chọn nào.
3. **Ràng buộc (IsValid):** Điều kiện để một ứng viên được chấp nhận.
4. **Điều kiện nghiệm hoàn chỉnh:** Khi nào thì $X$ là một lời giải để xuất (đủ $n$ thành phần, đã tới đích...). Cần tất cả hay một nghiệm.

**Mã giả chuẩn (Khung Try):**
```text
function Try(i)
    for mỗi ứng viên j trong S_i do
        if j chấp nhận được (IsValid) then
            x_i = j
            cập nhật trạng thái (đánh dấu đã dùng)
            if i = n then
                xuất lời giải X
            else
                Try(i + 1)
            end if
            hoàn tác trạng thái (bỏ đánh dấu j)  <-- Bắt buộc phải có
        end if
    end for
end function
```

### 6. Quy trình 6 bước làm bài Quy hoạch động
1. **Chọn bảng** 1 chiều hay 2 chiều, và cho biết kích thước bảng.
2. **Ô lưu gì:** (Nói thật cụ thể, là một con số tính được). Đây là bước quan trọng nhất.
3. **Cơ sở + phương trình QHĐ:** Làm được tới đây là đã nhiều điểm.
4. **Thứ tự điền:** (Điền ô nào trước) và điền bảng trên ví dụ đề cho, ghi quá trình tính từng ô.
5. **Lấy đáp án** ở đúng ô (không phải cứ là ô cuối hay max cả bảng, tùy bài).
6. **Truy vết** nếu đề đòi nghiệm: lưu bảng lựa chọn rồi lần ngược.
