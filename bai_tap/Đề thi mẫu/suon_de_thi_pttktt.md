# Sườn Đề Thi & Lưu Ý Môn Phân Tích & Thiết Kế Thuật Toán (Cô Thương)
*Trích xuất từ nội dung buổi học số 9*

## 🚨 1. LƯU Ý SỐNG CÒN TRONG PHÒNG THI
- **Tài liệu:** Sinh viên chỉ được phép sử dụng **duy nhất 01 tờ giấy A4 viết tay** (được viết cả mặt trước và mặt sau). Tuyệt đối không mang nhiều hơn.
- **Gian lận:** Cô Thương chấm bài rất kỹ. Tuyệt đối không gian lận (sử dụng điện thoại, dùng AI để giải, hay xin ra ngoài đi toilet để tra tài liệu). Nếu bị phát hiện, bài thi lập tức 0 điểm và **toàn bộ môn học 0 điểm** (không cứu vớt).
- **Mã giả (Pseudo-code):** Môn này là Thiết kế thuật toán, KHÔNG yêu cầu sinh viên phải viết code hoàn chỉnh bằng C++, Python hay Java. Các em chỉ cần trình bày bằng Mã giả. Nếu tự tin với ngôn ngữ lập trình thì có thể viết, nhưng Mã giả có đánh số bước, giải thích rõ ràng là đủ và an toàn nhất.
- **Thang điểm:** Đề thi chia làm 2 phần: Phân tích (6 điểm) + Thiết kế (6 điểm) = Tổng 12 điểm. Tuy nhiên, có thể giải thêm để nhận điểm bonus (có thể lên 14-15 điểm). Nhưng làm được 10 điểm là đã quá xuất sắc.

---

## 📝 2. SƯỜN ĐỀ THI CHI TIẾT (Khoảng 5 - 6 Câu)

### Câu 1: Ký hiệu tiệm cận (Khoảng 2 điểm)
- **Dạng 1:** Chứng minh tính đúng/sai của một số khẳng định liên quan đến $O$ (Big-O), $\Omega$ (Omega), $\Theta$ (Theta). (Có thể cho 2 câu chứng minh).
- **Dạng 2:** Cho một danh sách các hàm số độ phức tạp. Yêu cầu **phân lớp (group)** và **sắp xếp** chúng theo thứ tự độ phức tạp tăng dần (dùng O lớn). Yêu cầu phải có giải thích ngắn gọn, rõ ràng tại sao hàm này nằm trong nhóm nào, hàm nào tăng nhanh hơn hàm nào.

### Câu 2: Phân tích thuật toán (Khoảng 3 điểm)
- **Nội dung:** Cho một hoặc hai đoạn mã giả (có thể bao gồm 1 bài đệ quy và 1 bài không đệ quy).
- **Yêu cầu:**
  1. Xác định Input, Output và Chức năng của đoạn mã (hàm này dùng để làm gì).
  2. Đếm số lượng một phép toán cụ thể (ví dụ: đếm số phép gán, đếm số phép so sánh). Chú ý: Phải trình bày cách đếm rõ ràng.
  3. Xây dựng công thức tính độ phức tạp thời gian. 
     - *Nếu là đệ quy:* Phải lập được phương trình truy hồi.
  4. Giải phương trình và kết luận độ phức tạp $O(...)$.

### Câu 3: Ý tưởng Thiết kế thuật toán
- **Nội dung:** Cho bài toán cụ thể (Dùng kỹ thuật Chia để trị, Tham lam, v.v.).
- **Yêu cầu:**
  1. Nêu rõ Input / Output của bài toán.
  2. Trình bày **ý tưởng/chiến lược** giải quyết bài toán (Chỉ nói ý tưởng, chưa cần viết mã giả).
  3. Minh họa ý tưởng đó thông qua việc áp dụng vào một **ví dụ cụ thể** do đề bài cung cấp.

### Câu 4: Triển khai Mã giả thuật toán
- **Yêu cầu:**
  1. Viết mã giả (Pseudo-code) cho bài toán ở Câu 3 (hoặc một bài toán mới). Mã giả cần giải thích rõ cấu trúc dữ liệu sử dụng (Mảng, Biến,...).
  2. Đánh giá độ phức tạp thời gian (Time Complexity) và Không gian (Space Complexity) của thuật toán vừa thiết kế.

### Câu 5: Quy Hoạch Động (Trọng tâm CỰC KỲ quan trọng)
- **Lý thuyết nền tảng:**
  - Để dùng Quy hoạch động (Dynamic Programming - DP), bài toán phải có 2 tính chất: Cấu trúc con tối ưu (Optimal Substructure) và Bài toán con gối nhau (Overlapping Subproblems).
  - Quá trình giải ưu tiên cách tiếp cận **Bottom-Up** (Lập bảng) thay vì Top-Down đệ quy.
- **Yêu cầu thường gặp trong đề thi:**
  1. Trình bày **Bài toán cơ sở** (Base cases / Điều kiện dừng).
  2. Xây dựng **Phương trình quy hoạch động (Phương trình truy hồi)**. Giải thích các biến số trong công thức.
  3. Xác định **Kích thước bảng** và **Thứ tự điền bảng** (Ví dụ: điền từ trái qua phải, từ dưới lên trên, hay điền theo đường chéo).
  4. Thực hiện việc **Điền bảng tính toán** trên một ví dụ cụ thể do đề cho.
  5. (Bonus) Truy vết (Traceback) để tìm ra nghiệm tối ưu từ bảng đã điền.
- **Các bài toán trọng tâm (Buổi 9):**
  - Bài toán tính Tổ hợp chập k của n (Ứng dụng tam giác Pascal, quy hoạch động mảng 2 chiều).
  - **Bài toán Nhân chuỗi ma trận (Matrix Chain Multiplication):** Rất dễ thi. Cách thiết lập ma trận M lưu số phép nhân vô hướng tối thiểu và ma trận S lưu vị trí đặt dấu ngoặc. Cách điền bảng theo đường chéo song song với đường chéo chính.
