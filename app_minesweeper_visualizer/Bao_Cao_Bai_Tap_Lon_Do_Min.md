# BÁO CÁO BÀI TẬP LỚN: TRỰC QUAN HÓA THUẬT TOÁN GIẢI BÀI TOÁN DÒ MÌN (MINESWEEPER SOLVER)
**Môn học:** Phân Tích & Thiết Kế Thuật Toán (CS112)  
**Giảng viên hướng dẫn:** Cô Huỳnh Thị Thanh Thương  
**Sinh viên thực hiện:** Đỗ Quốc Thắng - MSSV: 26410111  
**Ngày nộp bài:** 04/10/2026  
**Mã nguồn Web App Visualizer:** `app_minesweeper_visualizer/index.html`  
**Video Demo:** [Link Video Google Drive / YouTube]  

---

## 1. MÔ HÌNH BÀI TOÁN (MATHEMATICAL MODEL & FORMULATION)

### 1.1. Bối cảnh & Phát biểu bài toán
Trong bài toán Dò Mìn (biến thể WeCode), người chơi được cung cấp một bảng kích thước $N \times M$ trong đó mỗi ô $(i, j)$ chứa một số nguyên là tổng số mìn nằm tại 4 ô kề cạnh theo hình chữ thập (không tính ô chéo và chính nó). Bài toán đặt ra là: **Hãy khôi phục lại vị trí của tất cả các quả mìn trong toàn bộ bảng từ ma trận gợi ý ban đầu.**

### 1.2. Xác định Input và Output chuẩn toán học (Đặc biệt chú trọng)
* **Input:**
  - Hai số nguyên dương $N, M \in \mathbb{N}^*$ ($1 \le N, M \le 10$).
  - Ma trận số nguyên $A = (a_{ij})_{N \times M}$ với $a_{ij} \in \{0, 1, 2, 3, 4\}$, trong đó $a_{ij}$ là số lượng mìn ở 4 ô kề cạnh (hình chữ thập: trên, dưới, trái, phải) của ô $(i, j)$.
* **Output:**
  - Ma trận nhị phân $B = (b_{ij})_{N \times M}$ với $b_{ij} \in \{0, 1\}$ (với $1$ là ô có mìn, $0$ là ô an toàn) thỏa mãn hệ ràng buộc:
    $$\forall i, j: \sum_{\substack{|r-i| + |c-j| = 1 \\ 0 \le r < N, 0 \le c < M}} b_{rc} = a_{ij}$$
  - Trường hợp không tồn tại ma trận thỏa mãn, trả về thông báo vô nghiệm.

---

## 2. THIẾT KẾ THUẬT TOÁN & MÃ GIẢ (ALGORITHM DESIGN & PSEUDOCODE)

### 2.1. Phân tích không gian trạng thái & Kỹ thuật Tối ưu Nhánh Cận
- **Phương pháp duyệt thô (Naive Brute-force):** Duyệt mọi cấu hình nhị phân cho $N \times M$ ô. Độ phức tạp là $O(2^{N \times M})$. Khi $N=10, M=10$, số trạng thái là $2^{100} \approx 1.26 \times 10^{30}$ (không thể chạy kịp thời gian quy định).
- **Ý tưởng tối ưu bằng Kỹ thuật Lan truyền Hàng (Row Propagation & Diagonal Pruning):**
  1. Nếu ta đã cố định hàng đầu tiên $B[0][0..M-1]$ ($2^M$ trạng thái), giá trị các ô ở hàng $1, 2, \dots, N-1$ sẽ **hoàn toàn được xác định duy nhất** theo công thức truy hồi:
     $$b_{r, c} = a_{r-1, c} - \sum \text{các ô lân cận đã biết của } (r-1, c)$$
  2. **Cắt tỉa nhánh sớm (Diagonal Constraint Checking):** Trong quá trình đệ quy thử từng cột $c$ của hàng 0, ta có thể tính ngay và kiểm tra tính hợp lệ của đường chéo phụ $(r, c-r)$. Nếu xuất hiện $b_{r, c-r} \notin \{0, 1\}$, ta **cắt tỉa (prune)** nhánh ngay lập tức mà không cần duyệt tiếp các cột sau.

Độ phức tạp sau khi tối ưu giảm xuống còn **$O(2^M \cdot N \cdot M)$**, dễ dàng vượt qua 100% test cases trên WeCode trong dưới $0.1$ giây.

### 2.2. Mã giả (Pseudocode) chuẩn form

```text
Algorithm: Solve_Minesweeper(N, M, A)
Input: Kích thước N, M và ma trận số gợi ý A[N][M]
Output: Ma trận nhị phân B[N][M] hoặc thông báo Vô nghiệm

Function Backtrack(c):
    if found == True then return
    
    if c == M then:
        if Check_And_Fill_Remaining_Rows(A, B) == True then:
            found = True
        return
        
    [lo, hi] ← Compute_Bound(A, B, c)
    if lo > hi then return // Cắt tỉa
    
    for val from lo to hi do:
        B[0][c] ← val
        ok ← True
        
        // Kiểm tra và lan truyền dọc theo đường chéo
        for r from 1 to min(c, N - 1) do:
            col ← c - r
            rv ← A[r-1][col] - Sum_Known_Neighbors(B, r-1, col)
            if rv < 0 or rv > 1 then:
                ok ← False
                break
            else:
                B[r][col] ← rv
                
        if ok == True then:
            Backtrack(c + 1)
```

---

## 3. THIẾT KẾ ỨNG DỤNG TRỰC QUAN HÓA (VISUALIZER WEB APPLICATION)

### 3.1. Kiến trúc & Công nghệ
- **Giao diện:** HTML5, Modern Vanilla CSS (Chủ đề Cyber-Retro Dark Mode, thiết kế theo tiêu chuẩn công thái học giao diện).
- **Core Engine:** JavaScript ES6 Generator (`function*`) cho phép thực thi thuật toán theo cơ chế `yield`, giúp tạm dừng, chạy từng bước (Step-by-step), điều chỉnh tốc độ linh hoạt mà không gây đóng băng (freeze) UI trình duyệt.

### 3.2. Các tính năng nổi bật
1. **Interactive Dual-Board:** Hiển thị song song bảng gợi ý $A$ và bảng trạng thái mìn $B$.
2. **Animation trạng thái tế bào:** 
   - 🔵 *Đang thử nghiệm giá trị (Testing)*
   - 🔴 *Cắt tỉa nhánh do mâu thuẫn (Pruned / Conflict Animation)*
   - 💣 *Xác nhận đặt mìn (Confirmed Mine)*
   - 🟢 *Xác nhận ô an toàn (Confirmed Safe)*
3. **Bộ đo lường (Telemetry & Live Log):** Đo trực tiếp số lần Backtrack, số nhánh đã bị loại bỏ, và highlight dòng mã giả tương ứng đang chạy.

---

## 4. NHẬT KÝ ỨNG DỤNG AI (AI USAGE REPORT - YÊU CẦU BẮT BUỘC)

Nhằm thực hiện đúng tinh thần nghiên cứu và tận dụng công nghệ AI theo định hướng của Giảng viên, toàn bộ quá trình phát triển dự án được phối hợp cùng AI (ChatGPT / Claude / Gemini) với các bước cụ thể:

### 4.1. Nhật ký Prompting & Phân công công việc

| Giai đoạn | Công cụ AI | Mục tiêu & Câu Prompt chính | Kết quả & Đánh giá |
|:---|:---|:---|:---|
| **1. Khảo sát thuật toán** | ChatGPT (GPT-4o) | *"Phân tích bài toán tái tạo ma trận Dò Mìn từ ma trận số lân cận. Hãy đề xuất giải thuật tối ưu hơn Brute-force $2^{N \times M}$."* | AI đề xuất ý tưởng chỉ cần duyệt hàng 0 vì các hàng sau bị phụ thuộc tuyến tính. |
| **2. Tinh chỉnh WeCode (Python)** | Claude 3.7 Sonnet | *"Viết mã nguồn Python giải bài toán trên WeCode với thời gian chạy tối ưu nhất, xử lý các trường hợp biên $N=1, M=1$."* | Sinh ra mã nguồn [giai_do_min_wecode.py](../bai_tap/WeCode/giai_do_min_wecode.py). Sinh viên trực tiếp kiểm tra và submit đạt điểm tối đa trên hệ thống WeCode. |
| **3. Thiết kế Visualizer** | Antigravity AI | *"Xây dựng giao diện web Single-Page hiện đại, trực quan hóa thuật toán bằng JS Generator để xem từng bước thử đặt mìn và tỉa nhánh."* | Hoàn thiện file `app_minesweeper_visualizer/index.html`. |

### 4.2. Khắc phục lỗi và can thiệp thủ công của Sinh viên
- **Lỗi AI thường gặp:** Khi AI sinh code kiểm tra tính hợp lệ của hàng cuối cùng ($N-1$), AI ban đầu quên mất việc hàng cuối cùng cũng phải thỏa mãn chính xác tổng số mìn của $A[N-1][c]$ (chỉ kiểm tra các ô bên trong mà bỏ qua điều kiện biên hàng đáy).
- **Can thiệp:** Sinh viên đã phát hiện điểm thiếu sót này qua test case và bổ sung thêm hàm `check_and_fill()` duyệt lại toàn bộ hàng cuối trước khi công nhận kết quả.

---

## 5. KẾT LUẬN & HƯỚNG DẪN CHẠY DEMO

1. Mở trực tiếp file `app_minesweeper_visualizer/index.html` trên bất kỳ trình duyệt web nào (Chrome, Edge, Firefox).
2. Chọn một Test Case mẫu hoặc tự nhập kích thước / số gợi ý.
3. Nhấn **"▶ Bắt Đầu Giải"** để xem thuật toán chạy tự động hoặc **"⏭ Từng Bước"** để quan sát chi tiết từng lần cắt tỉa nhánh vi phạm.
