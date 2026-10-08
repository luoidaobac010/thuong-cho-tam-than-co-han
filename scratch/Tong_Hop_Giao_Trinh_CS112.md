# BẢN TÓM TẮT GIÁO TRÌNH TỰ HỌC CS112 TRONG 7 NGÀY
*(Tổng hợp các ý chính từ Giao_Trinh_Tu_Hoc_7_Ngay_CS112_DAY_DU.pdf)*

## NGÀY 1: KÝ HIỆU TIỆM CẬN
Trọng tâm: So sánh và chứng minh độ phức tạp thuật toán.
1. **Bốn dạng bài chứng minh chính:**
   *   Chứng minh hàm cụ thể thuộc $O, \Omega, \Theta$ (tìm $c, n_0$).
   *   Chứng minh phản chứng (giả sử sai, tìm mâu thuẫn để chứng minh không thuộc $O$).
   *   Chứng minh tính chất tổng quát (hằng số phải khác tên, dùng $n \ge \max(n_1, n_2)$).
   *   Chứng minh 2 tập hợp bằng nhau (Xét chiều thuận và chiều đảo, mỗi chiều bắt đầu bằng "xét một hàm bất kỳ").
2. **Sắp xếp bậc tăng trưởng:**
   *   Sử dụng thang chuẩn: $1 \prec \log n \prec \sqrt{n} \prec n \prec n \log n \prec n^2 \prec 2^n \prec n! \prec n^n$
   *   Đưa tất cả các hàm lạ về dạng chuẩn (dùng $\log$, đổi cơ số). Chia nhóm để dễ so sánh.

## NGÀY 2: PHÂN TÍCH THUẬT TOÁN LẶP
Trọng tâm: Chuyển vòng lặp thành công thức tính tổng ($\Sigma$).
1. **Khung 5 bước Levitin:** Kích thước đầu vào $\to$ Chọn phép toán cơ bản $\to$ Xét tốt/xấu (nếu cần) $\to$ Lập tổng $\Sigma \to$ Rút gọn và kết luận bậc.
2. **Nguyên tắc đọc code:** 
   *   Mỗi vòng `for` là một dấu $\Sigma$. 
   *   Hai đoạn nối tiếp: dùng **Quy tắc cộng** (lấy $\max$).
   *   Hai đoạn lồng nhau: dùng **Quy tắc nhân**.
3. **Nhận dạng nhanh vòng lặp:**
   *   Vòng lặp chia đôi (`i*=2`, `i/=2`) $\to \Theta(\log n)$.
   *   Vòng lặp phụ thuộc (Tam giác) $\to \Theta(n^2)$.

## NGÀY 3: PHƯƠNG TRÌNH ĐỆ QUY
Trọng tâm: Lập và giải phương trình độ phức tạp cho đệ quy.
1. **Lập phương trình:** Phải đủ 3 ý: Số lời gọi đệ quy $\times$ kích thước bài con + Chi phí khác (phân chia và tổng hợp). Kèm điều kiện dừng (thường là hằng số 1).
2. **Bốn phương pháp giải:**
   *   **Truy hồi (thế ngược):** Thế 3 lần, tìm quy luật ở bước thứ $k$, thế $k$ cho chạm cơ sở rồi tính tổng.
   *   **Phương trình đặc trưng:** Giải phương trình đại số, xét nghiệm đơn/kép. Nếu vế phải khác $0$ thì thêm nghiệm riêng. Dùng hệ phương trình $T(0), T(1)$ để tìm hằng số $A, B$.
   *   **Hàm sinh:** Nhân 2 vế cho $x^n$ và lấy tổng, rút gọn hàm $G(x)$ thành phân thức, rồi tách phân thức để đọc lại hệ số dựa trên 5 hàm sinh cơ bản.
   *   **Đoán nghiệm + quy nạp:** Đoán dạng nghiệm $T(n) \le cn$, kiểm tra cơ sở, thế quy nạp và tìm điều kiện cho $c$. (Không thi định lý Master).

## NGÀY 4: QUAY LUI, CHIA / GIẢM / BIẾN ĐỔI ĐỂ TRỊ
Trọng tâm: Các chiến lược thiết kế thuật toán cốt lõi.
1. **Quay lui (Backtracking):** 
   *   **Dấu hiệu:** Yêu cầu vét cạn "tất cả" + Lời giải xây dần từng bước.
   *   **Mô hình hóa (4 ý):** Biểu diễn lời giải $X$, tập ứng viên $S_i$, ràng buộc (IsValid), điều kiện nghiệm.
   *   Đặc trưng mã giả là phải có bước **Hoàn tác (Undo)** sau khi thử đệ quy.
2. **Phân biệt 3 chiến lược "Để trị":**
   *   **Chia để trị:** Cắt bài gốc thành **$\ge 2$ bài con** (cùng loại) $\to$ Trị $\to$ Tổng hợp (vd: MergeSort).
   *   **Giảm để trị:** Cắt bài gốc thành **đúng 1 bài con** (vd: Binary Search, Insertion Sort).
   *   **Biến đổi để trị:** Chuyển bài toán sang dạng hoàn toàn khác (vd: HeapSort - đổi mảng thành cây).

## NGÀY 5: QUY HOẠCH ĐỘNG (DP)
Trọng tâm: Kỹ thuật đổi không gian (bảng nhớ) lấy thời gian.
1. **Hai đặc trưng bắt buộc:** (1) Cấu trúc con tối ưu (giải pháp tổng thể chứa giải pháp con). (2) Bài toán con trùng lặp (nhiều nhánh đệ quy tính lại 1 bài).
2. **Quy trình 6 bước:**
   *   Chọn bảng (1 chiều / 2 chiều) & Kích thước.
   *   **Xác định ô lưu gì:** Cực kỳ quan trọng, phải là 1 giá trị tính toán (max/min/độ dài).
   *   Xác định cơ sở và lập Phương trình truy hồi.
   *   Thứ tự điền bảng.
   *   Vị trí lấy đáp án.
   *   Truy vết (nếu cần lấy nghiệm cụ thể).
3. **Các bài kinh điển:** Ba lô 0/1 (bảng K[đồ][sức chứa]), LIS, LCS, Nhân chuỗi ma trận, Đặt dấu ngoặc.

## NGÀY 6: THAM LAM (GREEDY)
Trọng tâm: Từng bước tối ưu cục bộ, mong ra tối ưu toàn cục.
1. **Cách làm:** Lựa chọn một tiêu chí (ví dụ: đơn giá lớn nhất, kết thúc sớm nhất). Sắp xếp theo tiêu chí đó, và duyệt một lần để lấy kết quả. 
2. **Chứng minh & Phản ví dụ:** Thường dùng *Lập luận trao đổi* để chứng minh tối ưu. Hoặc tìm một bộ dữ liệu để chứng minh tiêu chí đó dẫn đến sai lệch.
3. **Lưu ý:** Bài "Ba lô 0/1" không giải được bằng tham lam (phải dùng DP). Nhưng bài "Ba lô phân số" thì tham lam theo đơn giá là chính xác.
