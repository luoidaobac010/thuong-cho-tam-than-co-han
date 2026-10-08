# CHUYÊN ĐỀ 2: THIẾT KẾ THUẬT TOÁN (TỰ LUẬN)
*(Tài liệu ôn tập Phần 2 - Đề thi CS112)*

---

*Lưu ý chung: Yêu cầu của các bài tập trong phần này là trình bày ý tưởng thuật toán, viết mã giả (pseudocode) có chú thích, và đánh giá độ phức tạp thời gian/không gian.*

## BÀI 1: THUẬT TOÁN QUAY LUI (BACKTRACKING)
**Bài 1: Sinh hoán vị chữ số**
Cho $N$ chữ số phân biệt. Hãy liệt kê tất cả các số có $N$ chữ số được tạo thành từ $N$ chữ số đó (hoán vị).
Yêu cầu:
- Thiết kế thuật toán Quay lui.
- Viết mã giả. Đánh giá độ phức tạp thuật toán.

## BÀI 2: THUẬT TOÁN CHIA ĐỂ TRỊ (DIVIDE AND CONQUER)
**Bài 2: Tính lũy thừa nhanh (Fast Exponentiation)**
Cho số thực $x$ và số nguyên dương $n$. Hãy tính $x^n$. 
Nếu dùng vòng lặp `for` nhân $n$ lần thì độ phức tạp là $O(n)$. Hãy thiết kế thuật toán Chia để trị (Divide and Conquer) để giảm độ phức tạp xuống $O(\log n)$.
Yêu cầu:
- Mô tả công thức đệ quy phân chia bài toán.
- Viết mã giả thuật toán và đánh giá độ phức tạp.

## BÀI 3: THUẬT TOÁN THAM LAM (GREEDY)
**Bài 3: Bài toán xếp lịch (Activity Selection Problem)**
Cho $n$ hoạt động, mỗi hoạt động $i$ có thời gian bắt đầu $s_i$ và thời gian kết thúc $f_i$ ($s_i < f_i$). Hai hoạt động được gọi là "không xung đột" nếu khoảng thời gian thực hiện của chúng không giao nhau (tức là $f_i \le s_j$ hoặc $f_j \le s_i$).
Hãy tìm một tập hợp gồm số lượng tối đa các hoạt động không xung đột để có thể thực hiện trên cùng một hội trường.
Yêu cầu:
- Nêu ý tưởng Tham lam (Greedy).
- Viết mã giả thuật toán và đánh giá độ phức tạp (bỏ qua thời gian sắp xếp).

## BÀI 4: QUY HOẠCH ĐỘNG (DYNAMIC PROGRAMMING)
**Bài 4.1: Bài toán Cái Túi 0/1 (0/1 Knapsack)**
Có một cái túi chịu được khối lượng tối đa là $W$. Có $n$ đồ vật, đồ vật thứ $i$ có khối lượng $w_i$ và giá trị $v_i$. Mỗi đồ vật chỉ có 1 cái và ta chỉ được chọn "lấy" (1) hoặc "không lấy" (0).
Hãy chọn các đồ vật bỏ vào túi sao cho tổng khối lượng không vượt quá $W$ và tổng giá trị đạt lớn nhất.
Yêu cầu:
- Xác định cấu trúc con tối ưu (gọi hàm $F(i, j)$ mang ý nghĩa gì?)
- Viết hệ thức truy hồi (phương trình đệ quy DP).
- Viết mã giả.

**Bài 4.2: Bài toán Cắt thanh sắt (Rod Cutting)**
Cho một thanh sắt dài $n$ mét và bảng giá $P$. Trong đó $P[i]$ là giá bán của một đoạn sắt dài $i$ mét ($1 \le i \le n$). Ta có quyền cắt thanh sắt thành các đoạn nhỏ hơn (độ dài nguyên) để bán.
Hỏi làm thế nào để cắt thanh sắt bán được nhiều tiền nhất?
Yêu cầu:
- Lập hệ thức truy hồi.
- Viết mã giả thuật toán Quy hoạch động (sử dụng kỹ thuật Bottom-up hoặc Top-down có nhớ). Đánh giá độ phức tạp.
