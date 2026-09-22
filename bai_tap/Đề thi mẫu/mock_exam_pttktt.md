# ĐỀ THI THỬ (MOCK EXAM) - PHÂN TÍCH & THIẾT KẾ THUẬT TOÁN
**Thời gian làm bài:** 90 phút
**Hình thức:** Tự luận (Được sử dụng duy nhất 01 tờ giấy A4 viết tay)

---

## Câu 1 (2.0 điểm): Ký hiệu tiệm cận
**a) (1.0đ)** Sắp xếp các hàm số sau theo thứ tự độ phức tạp thời gian tăng dần (sử dụng ký hiệu $O$ lớn). Giải thích ngắn gọn tại sao:
$f_1(n) = n \log n$, $f_2(n) = 10000$, $f_3(n) = 2^n$, $f_4(n) = n^2$, $f_5(n) = \sqrt{n}$

**b) (1.0đ)** Dùng định nghĩa Toán học của ký hiệu $O$ lớn (Big-O), hãy chứng minh rằng: $3n^2 + 5n + 10 = O(n^2)$.

---

## Câu 2 (3.0 điểm): Phân tích thuật toán
Cho đoạn mã giả sau đây, xử lý trên một mảng $A$ chứa $n$ số nguyên ($n > 0$):

```text
Algorithm Mystery(A[0..n-1])
1.  if n == 1 return A[0]
2.  mid = n / 2   // phép chia lấy phần nguyên
3.  L = Mystery(A[0..mid-1])
4.  R = Mystery(A[mid..n-1])
5.  if L > R 
6.      return L
7.  else 
8.      return R
```

**a) (0.5đ)** Xác định rõ Input, Output và Chức năng của đoạn mã giả này (Hàm này làm nhiệm vụ gì?).
**b) (0.5đ)** Xác định phép toán cơ bản (Basic Operation) của thuật toán này.
**c) (1.0đ)** Gọi $T(n)$ là số lần thực hiện phép toán cơ bản khi gọi hàm `Mystery` với mảng kích thước $n$. Hãy thiết lập phương trình truy hồi cho $T(n)$. (Để đơn giản, giả sử $n = 2^k$).
**d) (1.0đ)** Áp dụng định lý Thợ (Master Theorem) để giải phương trình truy hồi và kết luận độ phức tạp thuật toán bằng ký hiệu $O$ lớn.

---

## Câu 3 (2.0 điểm): Ý tưởng Thiết kế Thuật toán
**Bài toán: Xếp lịch họp (Interval Scheduling)**
Trong một ngày, có $n$ cuộc họp cần sử dụng chung một phòng họp. Cuộc họp thứ $i$ có thời gian bắt đầu là $s_i$ và thời gian kết thúc là $f_i$ ($s_i < f_i$). Hai cuộc họp không thể được xếp cùng lúc nếu thời gian của chúng giao nhau. Bạn cần thiết kế thuật toán Tham lam (Greedy) để chọn được **số lượng cuộc họp tối đa** được diễn ra.

**a) (0.5đ)** Xác định Input và Output của bài toán.
**b) (0.5đ)** Trình bày ý tưởng chiến lược Tham lam (Greedy Strategy) để giải bài toán này. Tại sao chiến lược này mang lại số cuộc họp tối đa?
**c) (1.0đ)** Minh họa ý tưởng của bạn trên tập dữ liệu sau (n = 6 cuộc họp):
- H1: (1, 4)
- H2: (3, 5)
- H3: (0, 6)
- H4: (5, 7)
- H5: (3, 9)
- H6: (5, 9)
- H7: (6, 10)
- H8: (8, 11)

---

## Câu 4 (2.0 điểm): Triển khai Mã giả
**a) (1.0đ)** Dựa trên ý tưởng ở Câu 3, hãy viết Mã giả (Pseudo-code) hoàn chỉnh cho bài toán Xếp lịch họp. Đánh số bước rõ ràng. *(Gợi ý: Mảng các cuộc họp có thể cần được sắp xếp trước).*
**b) (1.0đ)** Phân tích đánh giá độ phức tạp thời gian (Time Complexity) và Không gian (Space Complexity) của thuật toán tham lam vừa thiết kế.

---

## Câu 5 (3.0 điểm): Quy Hoạch Động (Trọng Tâm)
**Bài toán: Nhân chuỗi ma trận (Matrix Chain Multiplication)**
Cần tính tích của một chuỗi $n$ ma trận $A_1 \times A_2 \times ... \times A_n$. Kích thước của ma trận $A_i$ là $p_{i-1} \times p_i$. Bài toán yêu cầu đặt các dấu ngoặc để số lượng phép nhân vô hướng (scalar multiplications) là tối thiểu.

**a) (0.5đ)** Nêu rõ bài toán cơ sở (Base case) của bài toán này.
**b) (1.0đ)** Gọi $M[i, j]$ là số phép nhân vô hướng tối thiểu để nhân chuỗi từ $A_i$ đến $A_j$. Hãy viết phương trình truy hồi (phương trình Quy hoạch động) để tính $M[i, j]$ với $i < j$.
**c) (1.5đ)** Cho chuỗi 4 ma trận với mảng kích thước là $P = [10, 20, 50, 1, 100]$. Cụ thể:
- $A_1: 10 \times 20$
- $A_2: 20 \times 50$
- $A_3: 50 \times 1$
- $A_4: 1 \times 100$

Bằng phương pháp Bottom-Up (lập bảng), hãy chỉ ra thứ tự điền bảng và tính các giá trị điền vào bảng $M[i, j]$ để tìm số phép nhân vô hướng tối thiểu cho chuỗi 4 ma trận này. (Tính toán cụ thể các bước).
