# CHUYÊN ĐỀ 1: KÝ HIỆU TIỆM CẬN, VÒNG LẶP & ĐỆ QUY
*(Tài liệu ôn tập Phần 1 - Đề thi CS112)*

---

## DẠNG 1: CHỨNG MINH KÝ HIỆU TIỆM CẬN (O, $\Omega$, $\Theta$)
*Lưu ý: Phải dùng định nghĩa ($c, n_0$), KHÔNG DÙNG ĐỊNH LÝ GIỚI HẠN (Lim).*

**Bài 1.1:** Cho hàm $f(n) = 5n^3 + 2n^2 + 10$. Chứng minh $f(n) \in O(n^3)$.
**Bài 1.2:** Cho hàm $f(n) = n^2 \log n + n^3$. Chứng minh $f(n) \in \Omega(n^3)$.
**Bài 1.3:** Cho hàm $f(n) = \frac{1}{2} n^2 - 3n$. Chứng minh $f(n) \in \Theta(n^2)$.

---

## DẠNG 2: SẮP XẾP BẬC TĂNG TRƯỞNG
*Lưu ý: Nêu rõ quy tắc hoặc phân lớp $\Theta$ trước khi sắp xếp.*

**Bài 2.1:** Sắp xếp các hàm sau theo thứ tự tăng dần của Big-O (nhỏ nhất):
$$2^{\log_2 n}, \quad (n-1)!, \quad 10n^3 + n^2, \quad \log_2(n^5), \quad n \sqrt{n}, \quad 4^n$$
**Bài 2.2:** Có 2 thuật toán $A$ và $B$ có độ phức tạp lần lượt là $O(n^2 \log n)$ và $O(n \sqrt{n} \log^2 n)$. Hỏi khi $n$ rất lớn, thuật toán nào chạy nhanh hơn? Tại sao?

---

## DẠNG 3: ĐẾM SỐ PHÉP TOÁN VÀ ĐÁNH GIÁ ĐỘ PHỨC TẠP
*Yêu cầu: Đếm chính xác số lần thực thi của biến đếm và suy ra công thức tổng quát $O()$.*

**Bài 3.1:**
```cpp
int count = 0;
for (int i = 1; i <= n; i++) {
    for (int j = 1; j <= i; j++) {
        for (int k = 1; k <= 100; k++) {
            count++;
        }
    }
}
```

**Bài 3.2:**
```cpp
int count = 0;
for (int i = n; i > 0; i = i / 2) {
    for (int j = 1; j <= n; j = j * 3) {
        count++;
    }
}
```

---

## DẠNG 4: THÀNH LẬP VÀ GIẢI PHƯƠNG TRÌNH ĐỆ QUY
*Yêu cầu: Viết $T(n)$ và dùng Định lý Master (hoặc phân tích cây đệ quy) để giải.*

**Bài 4.1:** Tìm độ phức tạp của thuật toán Binary Search (Tìm kiếm nhị phân).
```cpp
int BinarySearch(int A[], int left, int right, int x) {
    if (left > right) return -1;
    int mid = (left + right) / 2;
    if (A[mid] == x) return mid;
    if (A[mid] > x) return BinarySearch(A, left, mid - 1, x);
    return BinarySearch(A, mid + 1, right, x);
}
```

**Bài 4.2:** Cho thuật toán Nhân ma trận Strassen với hệ thức truy hồi $T(n) = 7T(n/2) + O(n^2)$. 
Giải phương trình trên bằng định lý Master để tìm độ phức tạp của giải thuật.
