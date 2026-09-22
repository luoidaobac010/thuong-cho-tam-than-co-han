# ĐẠI HỌC QUỐC GIA TP.HCM — TRƯỜNG ĐH KHOA HỌC TỰ NHIÊN / UIT
### KHOA CÔNG NGHỆ THÔNG TIN

---

## ĐỀ THI CUỐI KỲ & HƯỚNG DẪN CẤU TRÚC ĐỀ THI (DỰ THẢO)
**Môn học:** PHÂN TÍCH VÀ THIẾT KẾ THUẬT TOÁN  
**Giảng viên phụ trách:** ThS. Huỳnh Thị Thanh Thương  
*(Tài liệu mô phỏng chính xác file Word được Cô Thương trình chiếu tại Buổi học số 9)*

- **Thời gian làm bài:** 90 phút
- **Hình thức thi:** Tự luận (Sinh viên làm bài trực tiếp trên đề thi)
- **Cấu trúc điểm:** 12.0 ĐIỂM (Phần I Phân tích 6.0đ + Phần II Thiết kế 6.0đ, thang điểm chấm mở rộng có thể lên tới 14 - 15 điểm)

---

### 🚨 LƯU Ý VÀ QUY CHẾ SỐNG CÒN TRONG PHÒNG THI (CÔ THƯƠNG QUÁN TRIỆT)

1. **Tài liệu cho phép:** Sinh viên chỉ được phép sử dụng **DUY NHẤT 01 TỜ GIẤY A4 VIẾT TAY** (được viết cả 2 mặt trước và sau). Tuyệt đối không mang giấy in photo hay mang nhiều hơn 1 tờ.
2. **Kỷ luật thi & Gian lận:** Cô Thương chấm bài trực tiếp và hậu kiểm từng bài. Tuyệt đối nghiêm cấm sử dụng điện thoại, AI giải đề hay trốn ra toilet tra tài liệu. Nếu bị phát hiện vi phạm: **0 ĐIỂM TOÀN BỘ BÀI THI VÀ 0 ĐIỂM TOÀN BỘ MÔN HỌC (RỚT MÔN, KHÔNG CỨU VỚT)**.
3. **Quy định về Mã giả (Pseudo-code):** Môn này là Thiết kế thuật toán, KHÔNG ép buộc viết đúng cú pháp C++/Python/Java chuẩn. Chỉ cần viết Mã giả có đánh số bước (Bước 1, Bước 2,...), chú thích biến và cấu trúc dữ liệu rõ ràng. **Không vẽ lưu đồ (flowchart)**.
4. **Nội dung giảm tải (Không thi):** Bỏ **Định lý Thợ (Master Theorem)** và bỏ bài toán giải tối ưu bằng **Thuật toán Ford-Fulkerson** (tìm luồng cực đại) do tính toán dài mất thời gian.

---

## PHẦN I: PHÂN TÍCH THUẬT TOÁN (6.0 ĐIỂM)

### Câu 1: Ký hiệu tiệm cận (2.0 điểm)
**a) (1.0 điểm)** Dùng định nghĩa toán học của ký hiệu tiệm cận, hãy chứng minh tính đúng/sai của các khẳng định sau:
- Khẳng định 1 (0.5đ): $3n^2 + 5n + 10 = O(n^2)$
- Khẳng định 2 (0.5đ): $n! = \Omega(2^n)$ *(hoặc chứng minh một đẳng thức tiệm cận với $\Theta$ / $\Omega$)*

*(Chừa khoảng trống 6 dòng để sinh viên trình bày tìm hằng số $c > 0, n_0 > 0$)*

**b) (1.0 điểm)** Cho danh sách các hàm số độ phức tạp sau đây:
$$f_1(n) = n \log n, \quad f_2(n) = 10000, \quad f_3(n) = 2^n, \quad f_4(n) = n^2, \quad f_5(n) = \sqrt{n}, \quad f_6(n) = n!, \quad f_7(n) = n^{\log n}$$
- Yêu cầu: Hãy phân lớp (group) các hàm số và sắp xếp theo thứ tự độ phức tạp thời gian tăng dần (sử dụng ký hiệu $O$ lớn). Giải thích ngắn gọn các bước biến đổi trung gian và chốt thứ tự sắp xếp cuối cùng.

---

### Câu 2: Phân tích thuật toán & Đếm phép toán (3.0 điểm)

**a) Phân tích thuật toán không đệ quy (1.0 điểm):**  
Cho đoạn mã lặp sau đây xử lý trên ma trận vuông $A[1..n, 1..n]$:

```text
Algorithm ProcessMatrix(A[1..n, 1..n])
1.  count = 0
2.  for i = 1 to n do
3.      for j = i to n do
4.          if A[i, j] > 0 then
5.              count = count + A[i, j]
6.  return count
```

- **Yêu cầu:**
  1. Xác định Input, Output và Chức năng của hàm trên.
  2. Đếm chính xác số phép so sánh (hoặc phép gán) thực hiện theo $n$ (lập công thức tổng $\sum$ và rút gọn).
  3. Kết luận độ phức tạp thời gian theo $O$ lớn.

**b) Phân tích thuật toán đệ quy (1.0 điểm):**  
Cho giải thuật đệ quy sau:

```text
Algorithm RecursiveCount(A[1..n])
1.  if n == 1 return A[1]
2.  mid = n / 2
3.  left_sum = RecursiveCount(A[1..mid])
4.  right_sum = RecursiveCount(A[mid+1..n])
5.  return left_sum + right_sum
```

- **Yêu cầu:** Thiết lập phương trình truy hồi $T(n)$ và giải thích ngắn gọn cơ sở thành lập phương trình.

**c) Giải phương trình đệ quy (1.0 điểm):**  
Sinh viên được chọn **1 TRONG 3** phương trình sau đây để giải theo phương pháp chỉ định:
- **Phương trình 1:** $T(n) = 2T(n/2) + n$, với $T(1) = 1$ *(Phương pháp thế / Truy hồi lặp)*
- **Phương trình 2:** $T(n) = 5T(n-1) - 6T(n-2)$, với $T(0) = 1, T(1) = 4$ *(Phương trình đặc trưng)*
- **Phương trình 3:** $T(n) = T(n-1) + n$, với $T(0) = 0$ *(Hàm sinh / Biến đổi đại số)*

---

## PHẦN II: THIẾT KẾ THUẬT TOÁN (6.0 ĐIỂM)

> **★ Lưu ý chấm thi:** Trong trường hợp chưa xây dựng được mã giả hoàn chỉnh, sinh viên hãy trình bày **Ý tưởng / Chiến lược thiết kế** mạch lạc kèm ví dụ minh họa để vẫn nhận được điểm phần ý tưởng.

### Câu 3: Phân tích bài toán & Ý tưởng thiết kế (2.0 điểm)
Sinh viên chọn **1 TRONG 2 BÀI TOÁN** sau:
- **Bài toán 3.1:** Cho dãy $n$ số nguyên $A[1..n]$. Tìm đoạn con liên tiếp có tổng lớn nhất bằng chiến lược **Chia để trị (Divide and Conquer)**.
- **Bài toán 3.2:** Bài toán Lựa chọn công việc (Activity Selection) - Cho $n$ công việc với thời gian bắt đầu $s_i$ và kết thúc $f_i$. Tìm tập công việc tương thích tối đa bằng chiến lược **Tham lam (Greedy)**.

- **Yêu cầu trình bày:**
  1. Xác định Input, Output và cho 1 ví dụ cụ thể.
  2. Trình bày ý tưởng / chiến lược giải thuật (Chưa cần viết mã giả).
  3. Minh họa ý tưởng chạy từng bước trên ví dụ.

---

### Câu 4: Triển khai Mã giả thuật toán & Đánh giá (2.0 điểm)
Cho bài toán: Thiết kế thuật toán tìm cặp điểm gần nhất (**Closest Pair of Points**) trên mặt phẳng 2D sử dụng kỹ thuật Chia để trị (hoặc bài toán Quay lui sinh dãy nhị phân/hoán vị có ràng buộc).

- **Yêu cầu:**
  1. Viết Mã giả (Pseudo-code) có đánh số thứ tự từng bước (Bước 1, Bước 2,...).
  2. Giải thích rõ ràng các biến, mảng hoặc cấu trúc dữ liệu được sử dụng.
  3. Đánh giá độ phức tạp thời gian (Time Complexity) và không gian (Space Complexity).

---

### Câu 5: Thiết kế thuật toán Quy hoạch động (Dynamic Programming) (2.0 điểm - TRỌNG TÂM)
Sinh viên chọn **1 TRONG 2 BÀI TOÁN QUY HOẠCH ĐỘNG** sau:
- **Bài toán 5.1: Nhân chuỗi ma trận (Matrix Chain Multiplication - MCM)** — Tìm thứ tự đặt dấu ngoặc tối ưu cho tích $A_1 \times A_2 \times \dots \times A_n$ để số phép nhân vô hướng là nhỏ nhất.
- **Bài toán 5.2: Tính tổ hợp chập $k$ của $n$ ($C_n^k$)** hoặc **Bài toán Cái túi 0/1 (0-1 Knapsack)** bằng tiếp cận Bottom-Up.

- **Yêu cầu các bước bắt buộc:**
  1. Phân tích 2 tính chất nền tảng: **Cấu trúc con tối ưu** và **Bài toán con gối nhau**.
  2. Xác định **Bài toán cơ sở (Base cases / Điều kiện dừng)**.
  3. Thiết lập **Phương trình Quy hoạch động (Phương trình truy hồi)** và giải thích các biến số.
  4. Xác định kích thước bảng và **Thứ tự điền bảng** (Bottom-Up: điền theo hàng, cột hay đường chéo song song đường chéo chính).
  5. Thực hiện việc **điền bảng tính toán** trên một ví dụ cụ thể do đề cho.
  6. *(Bonus)* Nêu giải thuật **truy vết (Traceback)** để tìm nghiệm tối ưu.

---

## TRANG GIẤY DỰ PHÒNG
*(Dành cho sinh viên làm lại bài khi bị hủy / sai sót ở các phần trên. Ghi rõ làm lại cho Câu số mấy và gạch chéo phần bài làm bị hủy ở phía trên)*

`....................................................................................................................................................................................................`
