# CÂU 4: LIỆT KÊ HOÁN VỊ - QUAY LUI (BACKTRACKING) VS GIẢM ĐỂ TRỊ (DECREASE-AND-CONQUER)
## MÔN: PHÂN TÍCH VÀ THIẾT KẾ THUẬT TOÁN (CS112) - CÔ HUỲNH THỊ THANH THƯƠNG

---

# PHẦN 1: BÀI TOÁN VÀ ĐẶT VẤN ĐỀ

**Đề bài:** Cho một tập hợp $a = (a_1, a_2, \dots, a_n)$ gồm $n$ phần tử đôi một khác nhau. Hãy liệt kê tất cả các hoán vị của dãy $n$ phần tử này.
- Ví dụ với $a = (7, 2, 4)$, có tổng cộng $3! = 6$ hoán vị:
  $(7, 2, 4), (7, 4, 2), (2, 7, 4), (2, 4, 7), (4, 2, 7), (4, 7, 2)$.
- **Yêu cầu:** Thiết kế thuật toán theo 2 phương pháp:
  1. Phương pháp Quay lui (Backtracking)
  2. Phương pháp Giảm để trị (Decrease-and-Conquer)
  3. So sánh độ phức tạp thời gian và không gian của 2 thuật toán đã thiết kế.

---

# PHẦN 2: THIẾT KẾ THUẬT TOÁN BẰNG PHƯƠNG PHÁP QUAY LUI (BACKTRACKING)

## 1. Ý tưởng thiết kế & Cấu trúc dữ liệu
- Ta xây dựng dần từng phần tử của hoán vị tại vị trí $k$ từ $1$ đến $n$.
- Sử dụng một mảng kết quả $X[1..n]$ để lưu hoán vị hiện tại đang xây dựng.
- Sử dụng một mảng boolean `used[1..n]` (ban đầu tất cả là `False`) để đánh dấu phần tử $a[i]$ đã được chọn vào hoán vị hay chưa, nhằm đảm bảo tính phân biệt của hoán vị.
- Khi xây dựng đến vị trí $k = n$, ta ghi nhận/in ra một hoán vị hoàn chỉnh. Sau đó quay lui (backtrack), hủy chọn phần tử (`used[i] = False`) để thử các nhánh tiếp theo.

## 2. Mã giả thuật toán Quay lui (Đánh số bước chuẩn)

```text
Thuật toán Backtrack_Permutation(k, n, a, X, used):
Đầu vào:
  - k: Vị trí hiện tại cần chọn giá trị (1 <= k <= n)
  - n: Số lượng phần tử
  - a[1..n]: Mảng n phần tử ban đầu
  - X[1..n]: Mảng lưu hoán vị đang xây dựng
  - used[1..n]: Mảng boolean đánh dấu phần tử đã dùng
Đầu ra: In ra toàn bộ n! hoán vị của mảng a.

1.  Cho i chạy từ 1 đến n thực hiện:
2.      Nếu used[i] == False thì:
3.          X[k] = a[i]                 // Chọn phần tử a[i] vào vị trí k
4.          used[i] = True              // Đánh dấu a[i] đã được sử dụng
5.          Nếu k == n thì:
6.              In mảng X[1..n]         // Đã xây dựng đủ n phần tử -> In kết quả
7.          Ngược lại:
8.              Backtrack_Permutation(k + 1, n, a, X, used) // Đệ quy chọn vị trí tiếp theo
9.          used[i] = False             // Quay lui (Backtrack): trả lại trạng thái chưa dùng

Thuật toán Sinh_Hoan_Vi_Quay_Lui(a, n):
1.  Khởi tạo mảng X[1..n]
2.  Khởi tạo mảng used[1..n] = False với mọi i từ 1 đến n
3.  Gọi Backtrack_Permutation(1, n, a, X, used)
```

## 3. Phân tích độ phức tạp của Quay lui
- **Số nút lá trên cây không gian trạng thái:** Có đúng $n!$ hoán vị, tương ứng $n!$ lá.
- **Tổng số nút trên cây đệ quy:**
  $$1 + n + n(n-1) + n(n-1)(n-2) + \dots + n! = \sum_{k=0}^n \frac{n!}{(n-k)!} = O(n!)$$
- **Tại mỗi nút lá (bước 6):** Cần $O(n)$ phép toán để in/sao chép mảng $X[1..n]$.
- **Độ phức tạp thời gian:** $T(n) = O(n \cdot n!)$.
- **Độ phức tạp không gian (bộ nhớ):** $O(n)$ cho mảng `used`, mảng `X` và ngăn xếp đệ quy có độ sâu tối đa là $n$.

---

# PHẦN 3: THIẾT KẾ THUẬT TOÁN BẰNG PHƯƠNG PHÁP GIẢM ĐỂ TRỊ (DECREASE-AND-CONQUER)

## 1. Ý tưởng thiết kế (Bottom-Up / Insertion Approach)
- **Kỹ thuật Giảm kích thước bài toán (Decrease-by-1):**
  - Để sinh tất cả hoán vị của $n$ phần tử $\{a_1, a_2, \dots, a_n\}$, ta giả sử đã có danh sách tất cả các hoán vị của $n-1$ phần tử đầu tiên $\{a_1, a_2, \dots, a_{n-1}\}$.
  - Với mỗi hoán vị $P$ có độ dài $n-1$, ta chèn phần tử thứ $n$ ($a_n$) vào tất cả $n$ vị trí có thể có (từ vị trí đầu tiên $0$, giữa các phần tử, đến vị trí cuối cùng $n-1$).
- **Trường hợp cơ sở:** Khi $n = 1$, hoán vị duy nhất của dãy $\{a_1\}$ chính là $(a_1)$.

## 2. Mã giả thuật toán Giảm để trị

```text
Thuật toán Generate_Permutations_Decrease_Conquer(a, n):
Đầu vào: Mảng a[1..n] gồm n phần tử đôi một khác nhau.
Đầu ra: Danh sách L chứa tất cả n! hoán vị.

1.  Nếu n == 1 thì:
2.      Tạo danh sách L chỉ chứa 1 hoán vị duy nhất: [[a[1]]]
3.      Trả về L
4.  L_prev = Generate_Permutations_Decrease_Conquer(a, n - 1)  // Giải bài toán con quy mô n-1
5.  Khởi tạo danh sách kết quả rỗng L_current = []
6.  Với mỗi hoán vị P trong danh sách L_prev thực hiện:
7.      Cho pos chạy từ 0 đến length(P) thực hiện:
8.          Tạo hoán vị mới new_P bằng cách chèn phần tử a[n] vào vị trí pos của P
9.          Thêm new_P vào danh sách L_current
10. Trả về L_current
```

## 3. Minh họa từng bước với $a = (7, 2, 4)$:
- $n = 1$: $\{ (7) \}$
- $n = 2$: Chèn phần tử $2$ vào mọi vị trí của $(7)$:
  - Chèn đầu: $(2, 7)$
  - Chèn đuôi: $(7, 2)$
  $\implies L_2 = \{ (2, 7), (7, 2) \}$
- $n = 3$: Chèn phần tử $4$ vào mọi vị trí của từng hoán vị trong $L_2$:
  - Từ $(2, 7) \implies (4, 2, 7), (2, 4, 7), (2, 7, 4)$
  - Từ $(7, 2) \implies (4, 7, 2), (7, 4, 2), (7, 2, 4)$
  $\implies$ Thu được đúng $6$ hoán vị.

## 4. Phân tích độ phức tạp của Giảm để trị
- **Thời gian:**
  - Để tạo danh sách hoán vị cấp $n$, ta cần duyệt qua $(n-1)!$ hoán vị của cấp $n-1$, mỗi hoán vị tạo ra $n$ hoán vị mới kích thước $n$, thao tác chèn mất $O(n)$.
  - Phương trình đệ quy: $T(n) = T(n-1) + n \cdot (n-1)! \cdot O(n) = T(n-1) + O(n \cdot n!)$.
  - Suy ra tổng thời gian: $T(n) = O(n \cdot n!)$.
- **Không gian:** Cần lưu trữ toàn bộ $n!$ hoán vị trong bộ nhớ danh sách $\implies O(n \cdot n!)$.

---

# PHẦN 4: BẢNG SO SÁNH ĐỘ PHỨC TẠP HAI PHƯƠNG PHÁP

| Tiêu chí so sánh | Phương pháp Quay lui (Backtracking) | Phương pháp Giảm để trị (Decrease & Conquer) |
| :--- | :--- | :--- |
| **Bản chất tiếp cận** | Top-Down: Xây dựng từng vị trí bằng đệ quy và thử - sai (trial-and-error). | Bottom-Up / Reduce: Mở rộng nghiệm từ bài toán quy mô $n-1$ lên $n$. |
| **Độ phức tạp thời gian** | $\Theta(n \cdot n!)$ (Tối ưu để duyệt và in ra) | $\Theta(n \cdot n!)$ (Tương đương về mặt tiệm cận) |
| **Độ phức tạp không gian** | **$O(n)$** (Rất tối ưu, chỉ lưu 1 trạng thái hoán vị hiện tại và stack đệ quy). | **$O(n \cdot n!)$** (Tốn rất nhiều RAM vì phải lưu toàn bộ danh sách các hoán vị trong bộ nhớ). |
| **Khả năng mở rộng / Ứng dụng** | Dễ dàng cài đặt thêm các điều kiện cắt tỉa (pruning/nhánh cận) khi giải bài toán tối ưu. | Phù hợp khi cần lưu trữ hoặc truyền toàn bộ danh sách kết quả dạng cấu trúc dữ liệu. |
