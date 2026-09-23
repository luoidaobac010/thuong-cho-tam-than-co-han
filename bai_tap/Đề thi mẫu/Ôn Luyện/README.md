# TỔNG HỢP ÔN LUYỆN ĐỀ THI CUỐI KỲ CS112 - PHÂN TÍCH VÀ THIẾT KẾ THUẬT TOÁN
## THEO CẤU TRÚC ĐỀ THI MẪU 2025-2026 (CÔ HUỲNH THỊ THANH THƯƠNG)

---

### MỤC LỤC BỘ TÀI LIỆU ÔN TẬP TỪNG CÂU

0. 🌟 **[BẢNG TỔNG HỢP TỜ GIẤY A4 (2 MẶT VIẾT TAY) MANG VÀO PHÒNG THI](file:///Users/thangdo/www/thuong-cho-tam-than-co-han/bai_tap/Đề%20thi%20mẫu/Ôn%20Luyện/TO_GIAY_A4_ON_THI_PTTKTT_CO_THUONG.md)**
   - **Mặt 1:** Khung định nghĩa $O, \Omega, \Theta$, câu thần chú chứng minh tập con/bằng nhau, chuỗi phân lớp Big-O, và 3 phương pháp giải phương trình đệ quy (Truy hồi, PT đặc trưng, Hàm sinh).
   - **Mặt 2:** Khung chuẩn 4 bước Quy hoạch động (5 bài toán DP cốt lõi), thuật toán Tham lam Ba lô phân số, và khung mã giả Quay lui (Mã đi tuần, Hoán vị, N-Queens).

1. **[Câu 1 - Ký hiệu tiệm cận và Phân lớp độ phức tạp Big-O](file:///Users/thangdo/www/thuong-cho-tam-than-co-han/bai_tap/Đề%20thi%20mẫu/Ôn%20Luyện/Cau1_Ky_Hieu_Tiem_Can_Va_Phan_Lop_Do_Phuc_Tap.md)**
   - **Dạng 1A:** Chứng minh định nghĩa toán học $O, \Omega, \Theta$ (Định nghĩa chặt chẽ, không dùng lim, không dùng định lý).
   - **Dạng 1B:** Phân lớp & sắp xếp các hàm theo Big-O nhỏ nhất tăng dần (Quy tắc chuỗi phân lớp chuẩn cô Thương).
   - **Tập bài tập tự luyện + Lời giải chi tiết.**

2. **[Câu 2 - Phân tích thuật toán và Giải phương trình đệ quy](file:///Users/thangdo/www/thuong-cho-tam-than-co-han/bai_tap/Đề%20thi%20mẫu/Ôn%20Luyện/Cau2_Phan_Tich_Thuat_Toan_Va_Phuong_Trinh_De_Quy.md)**
   - **Dạng 2A:** Phân tích thuật toán lặp (Input/Output, đếm phép toán cơ bản, lập tổng $\sum$, tính $O$).
   - **Dạng 2B:** Thành lập phương trình đệ quy (Hanoi Tower, MergeSort, QuickSort, chia để trị).
   - **Dạng 2C:** Giải phương trình đệ quy bằng 3 phương pháp (Truy hồi thế ngược Backward Substitution, Phương trình đặc trưng, Hàm sinh Generating Functions). *Tuyệt đối không dùng Master Theorem*.

3. **[Câu 3 - Quy hoạch động (Dynamic Programming)](file:///Users/thangdo/www/thuong-cho-tam-than-co-han/bai_tap/Đề%20thi%20mẫu/Ôn%20Luyện/Cau3_Quy_Hoach_Dong.md)**
   - **Dạng 3A:** Đặt dấu ngoặc biểu thức số thực tối ưu (Đề 2025: $A = 1+2\times 3+4$).
   - **Dạng 3B:** Nhân chuỗi ma trận (Matrix Chain Multiplication - MCM) - Bảng chi phí & Bảng vết ngoặc.
   - **Dạng 3C:** Bài toán Cái túi 0/1 (0/1 Knapsack) & Tổ hợp $C_n^k$ theo Bottom-Up.
   - **Quy trình 4 bước chuẩn cô Thương:** Bài toán con $\rightarrow$ Công thức truy hồi $\rightarrow$ Thứ tự điền bảng $\rightarrow$ Truy vết kết quả.

4. **[Câu 4 - Liệt kê hoán vị: Quay lui (Backtracking) vs Giảm để trị (Decrease-and-Conquer)](file:///Users/thangdo/www/thuong-cho-tam-than-co-han/bai_tap/Đề%20thi%20mẫu/Ôn%20Luyện/Cau4_Liet_Ke_Hoan_Vi_Va_Giam_De_Tri_Quay_Lui.md)**
   - Thuật toán Quay lui với mảng đánh dấu `used[]`.
   - Thuật toán Giảm để trị (Chèn phần tử thứ $n$ vào tất cả các vị trí của hoán vị cấp $n-1$ / Johnson-Trotter).
   - So sánh chi tiết độ phức tạp thời gian và không gian trạng thái.

5. **[Câu 5 - Bài toán Mã đi tuần (Knight's Tour) và Nhánh cận / Quay lui](file:///Users/thangdo/www/thuong-cho-tam-than-co-han/bai_tap/Đề%20thi%20mẫu/Ôn%20Luyện/Cau5_Ma_Di_Tuan_Va_Quay_Lui.md)**
   - Mô hình hóa bàn cờ $n \times n$ và 8 bước nhảy hợp lệ của quân mã.
   - Thuật toán Quay lui (Backtracking) tìm hành trình.
   - Heuristic Warnsdorff (chọn ô kế tiếp có số nước đi tiếp theo ít nhất).

6. **[CHUYÊN ĐỀ ĐẶC BIỆT: TỔNG HỢP 10 DẠNG BÀI TẬP QUAY LUI KINH ĐIỂN & WECODE](file:///Users/thangdo/www/thuong-cho-tam-than-co-han/bai_tap/Đề%20thi%20mẫu/Ôn%20Luyện/Chuyen_De_Thuat_Toan_Quay_Lui_Backtracking.md)**
   - Khung mã giả chuẩn cô Thương & Nguyên lý Thử - Sai (Trial-and-Error).
   - Tuyển tập 10 bài toán: N-Queens, Mã đi tuần, Sinh hoán vị, Sudoku 9x9, Khôi phục địa chỉ IP, Tách chuỗi đối xứng (Palindrome Partition), Tìm từ trong ô chữ (Word Search), Tính điểm môn học (Subset Sum), Tô màu đồ thị (Graph Coloring), Giải Dò mìn (Minesweeper).
   - Bảng tổng hợp so sánh độ phức tạp thời gian/bộ nhớ và kỹ thuật cắt tỉa cho 10 bài toán.

7. **[Câu 6 - Ba lô phân số (Fractional Knapsack) và Thuật toán Tham lam (Greedy)](file:///Users/thangdo/www/thuong-cho-tam-than-co-han/bai_tap/Đề%20thi%20mẫu/Ôn%20Luyện/Cau6_Ba_Lo_Phan_So_Va_Tham_Lam_Greedy.md)**
   - Mô hình hóa bài toán tối ưu tuyến tính liên tục.
   - Thuật toán Tham lam theo đơn giá $p_i / w_i$ giảm dần.
   - Lời giải chi tiết bài toán mẫu trong đề 2025: $n=3, M=20, w=(18,15,10), p=(25,24,15)$.

7. **[Đề thi mẫu 2025 - Đáp án và Lời giải Chi tiết 100%](file:///Users/thangdo/www/thuong-cho-tam-than-co-han/bai_tap/Đề%20thi%20mẫu/Ôn%20Luyện/De_Thi_Mau_2025_Loi_Giai_Chi_Tiet.md)**
   - Lời giải hoàn chỉnh từng bước của toàn bộ 6 câu trong đề thi HK1 (2025-2026).
