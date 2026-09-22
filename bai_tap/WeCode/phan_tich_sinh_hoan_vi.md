# Phân Tích Bài Toán: Sinh Hoán Vị (Dùng Quay Lui)

## 1. Xác định bài toán (I/O)
*   **Dữ liệu vào (Input):** Số nguyên dương n (1 <= n <= 9).
*   **Dữ liệu ra (Output):** Danh sách tất cả n! (n giai thừa) hoán vị của tập hợp gồm n số nguyên dương đầu tiên {1, 2, 3, ..., n}. Mỗi hoán vị được in trên một dòng, các phần tử cách nhau bởi khoảng trắng.

## 2. Ý tưởng cốt lõi (Sử dụng Quay Lui - Backtracking)
Hoán vị của n phần tử là một cách sắp xếp có thứ tự của n phần tử đó. Một cấu hình (một hoán vị) có thể được biểu diễn dưới dạng một mảng (vector) 1 chiều: 
S = (S1, S2, ..., Sn)

Với các điều kiện ràng buộc (Constraints):
1.  S[i] thuộc {1, 2, ..., n} (Mỗi vị trí lấy giá trị từ 1 đến n).
2.  S[i] khác S[j] với mọi i khác j (Các phần tử trong hoán vị không được trùng lặp nhau).

Để liệt kê tất cả các hoán vị, ta sử dụng **Thuật toán Quay lui (Backtracking)** để xây dựng dần cấu hình S. Tại mỗi bước i (từ 1 đến n), ta sẽ cố gắng thử điền một giá trị cho S[i]. 

Thuật toán hoạt động như một quá trình duyệt trên **Cây không gian trạng thái (State-space tree)**, trong đó nhánh cây đại diện cho việc chọn giá trị, và ta sẽ cắt tỉa (pruning) những nhánh không thỏa mãn điều kiện (bị trùng số).

## 3. Phân tích các thành phần theo "Mô Hình 1"

Để giải bài này, ta ánh xạ vào Mô hình chung 1 mà giảng viên yêu cầu:

**a. Tập ứng cử viên (khả năng j mà S[i] có thể chọn):**
*   Tại vị trí i, phần tử S[i] có thể nhận bất kỳ giá trị nào từ 1 đến n. 
*   Vòng lặp duyệt khả năng: `for j in range(1, n + 1)`

**b. Điều kiện chấp nhận khả năng (Hàm Pruning):**
*   Vì các phần tử trong hoán vị không được trùng nhau, giá trị j chỉ được chấp nhận nếu **j chưa từng được chọn ở các vị trí trước đó** (từ S[1] đến S[i-1]).
*   *Cách cài đặt:* Ta dùng một mảng đánh dấu `used[]` kiểu boolean. `used[j] = True` nghĩa là số j đã bị lấy mất, `False` nghĩa là số j còn rảnh. Khả năng j được chấp nhận khi `used[j] == False`.

**c. Xác định S[i] và Ghi nhận trạng thái:**
*   Nếu j hợp lệ, ta gán S[i] = j.
*   Lập tức ghi nhận sự thay đổi: Đánh dấu số j đã được sử dụng (`used[j] = True`).

**d. Điều kiện dừng / Đi tiếp:**
*   Nếu i < n: Cấu hình chưa đủ n phần tử, ta gọi đệ quy `Try(i + 1)` để đi tìm phần tử tiếp theo.
*   Nếu i == n: Cấu hình đã đủ n phần tử. Đây là một nghiệm hợp lệ -> **Xuất lời giải**.

**e. Trả lại trạng thái cũ (Backtrack):**
*   Đây là bước **cực kỳ quan trọng** tạo nên tên gọi của thuật toán. Sau khi gọi đệ quy `Try(i + 1)` xong (hoặc in xong hoán vị), hàm sẽ quay lui về vị trí i. Ta cần "nhả" số j ra để vòng lặp tiếp tục thử số j+1 khác. 
*   Lệnh thực thi: `used[j] = False`.

---

## 4. Tóm tắt luồng chạy bằng ví dụ n = 3 (Góc nhìn trực quan)

Với n = 3, ta có tập hợp {1, 2, 3}. Tổng số lượng hoán vị là 3! = 6 trường hợp ứng với 6 dòng kết quả.
Ta có thể hình dung mảng S gồm 3 phần tử S[1], S[2], S[3] tương ứng với 3 biến (a, b, c). Thuật toán sẽ lần lượt thử các trường hợp và lặp lại quá trình chọn:

*   **Bước 1:** Chọn a = 1 (Tương ứng S[1] = 1). Các số còn lại có thể chọn: 2, 3.
*   **Bước 2:** Chọn b = 2 (Tương ứng S[2] = 2). Số còn lại có thể chọn: 3.
*   **Bước 3:** Bắt buộc c = 3 (Tương ứng S[3] = 3). 
    -> **Ta được hoán vị đầu tiên: 1 2 3**.
    
*   **Bước 4 (Quay lui b):** Bây giờ giữ nguyên a = 1, nhưng ta lùi lại không chọn b = 2 nữa mà "nhả" ra để chọn khả năng khác cho b. Khả năng duy nhất còn lại là b = 3.
*   **Bước 5:** Khi a = 1, b = 3 thì số duy nhất còn sót lại cho c là 2.
    -> **Ta được hoán vị thứ hai: 1 3 2**.

*   **Bước 6 (Quay lui a):** Lúc này nhánh a = 1 đã thử hết mọi cách cho b và c. Thuật toán sẽ quay lùi hẳn về đầu để đổi a. Ta chọn a = 2. Các số còn lại lúc này là 1 và 3.
*   **Bước 7:** Tương tự, nếu b = 1 thì c = 3 -> **2 1 3**.
*   **Bước 8:** Quay lui b, đổi b = 3 thì c = 1 -> **2 3 1**.

Và thuật toán cứ tiếp tục như thế cho đến khi a = 3 và duyệt hết toàn bộ 6 trường hợp. Quá trình "nhả ra để chọn lại" này trong code chính là dòng lệnh `used[j] = False` ở cuối hàm `Try()`.
