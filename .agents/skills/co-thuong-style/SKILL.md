---
name: co-thuong-style
description: >
  Phong cách trình bày bài giải theo cô Huỳnh Thị Thanh Thương.
  Dùng khi giải bài tập, tạo LaTeX, hoặc giải thích thuật toán cho môn PTTKTT.
  Tự động load khi context liên quan đến cô Thương / PTTKTT / HW.
triggers:
  - "cô Thương"
  - "PTTKTT"
  - "bài tập"
  - "HW#"
  - "giải bài"
  - "order of growth"
  - "tiệm cận"
  - "asymptotic"
---

# Skill: Phong cách giải bài cô Thương

## Mục đích

Đảm bảo AI giải bài **đúng phong cách** mà cô Huỳnh Thị Thanh Thương dạy trên lớp.

**⚠️ QUAN TRỌNG:** Dữ liệu gốc DUY NHẤT là các file transcript buổi học
(`data/buoi1_clean.md` → `buoi5_clean.md`). Các file LaTeX trong thư mục `data/`
(vd: `loi_giai_*.tex`) là do AI gen từ session trước, KHÔNG PHẢI tài liệu gốc của cô.

---

## 🔴 QUY TẮC BẮT BUỘC (trích nguyên văn từ transcript)

### 1. Chứng minh bằng định nghĩa — VIẾT ĐẦY ĐỦ

> **Buổi 4, dòng 373:** "Yêu cầu các bạn phải tôn trọng cái định nghĩa. Tức là
> định nghĩa nói sao mình phải viết ra y chang như vậy, không được bỏ bớt bất kỳ
> thông tin nào."

- Khi chứng minh f ∈ O(g): PHẢI viết "Tồn tại c ∈ ℝ⁺, n₀ ∈ ℕ sao cho..."
- Khi chứng minh f ∈ Θ(g): PHẢI viết cả C₁, C₂, n₀
- Thiếu "tồn tại", thiếu "∈ ℝ⁺", thiếu "với mọi n ≥ n₀" = **bị trừ điểm**

### 2. Phải có lập luận — KHÔNG ĐƯỢC chọn C rồi viết luôn

> **Buổi 4, dòng 253-255:** "Phải có cái quá trình suy luận để quy về cái chuyện
> là tại sao chọn C như vậy N₀ là như vậy chứ không phải đồng phát là cứ chọn luôn.
> Em phải có cái lý lẽ lý luận là tại sao em chọn."

Quy trình:
1. Viết ra BĐT cần chứng minh (dạng f(n) ≤ c·g(n))
2. Lập luận biến đổi tại sao BĐT đúng
3. TỪ ĐÓ suy ra c = ?, n₀ = ?
4. Kết luận "Theo định nghĩa của Big O ta có điều cần chứng minh"

### 3. Trình bày bài chứng minh mẫu (buổi 4)

> **Buổi 4, dòng 213:** "Cô sẽ trình bày cái bài làm này như sau:
> Với mọi n ≥ 1 ta có 7n² ≤ 7n³.
> Vậy từ đây suy ra chọn C = 7, N₀ = 1, theo định nghĩa của BO
> ta có điều cần chứng minh."

Format mẫu:
```
Với mọi n ≥ [n₀] ta có [f(n)] ≤ [biểu thức biến đổi] ≤ [c·g(n)].
Suy ra chọn c = [giá trị], n₀ = [giá trị].
Theo định nghĩa của [Big O / Omega / Theta] ta có ĐPCM.
```

### 4. Khi vế phải phức tạp — chọn C trước, tìm n₀ sau

> **Buổi 4, dòng 225:** "Khi cái vế đằng sau nó phức tạp á thì dựa trên kinh nghiệm
> các bạn nên chọn C trước, tìm C trước rồi nương theo C tìm tiếp n₀."

Ví dụ cô giải trên lớp: CM 7n² = O(n² - 80n)
- Thử C = 7 → không được (vì vế phải bị trừ)
- Thử C = 8 → phân phối vào, chuyển vế
- Xét dấu biểu thức → tìm n₀ = 640
- Kết luận: c = 8, n₀ = 640

### 5. Chứng minh tập con (A ⊂ B) — XÉT PHẦN TỬ BẤT KỲ

> **Buổi 4, dòng 397:** "Thiếu cái chữ BẤT KỲ là coi như mất điểm.
> Tại bất kỳ mới là quan trọng."

- LUÔN LUÔN viết: "Xét một hàm **bất kỳ** f(n) ∈ [tập A]"
- Không được viết: "Xét một hàm f(n) ∈ [tập A]" (thiếu "bất kỳ")
- CM f(n) cũng ∈ [tập B] → suy ra A ⊂ B

### 6. Khi có 2 hàm riêng biệt — DÙNG KÝ HIỆU KHÁC NHAU

> **Buổi 4, dòng 413-415:** "T₁ với T₂ nó đâu có liên quan gì đâu.
> Nếu chúng ta khẳng định vẫn tồn tại C thành ra giống như C trên C dưới là 1.
> Chọn một ký hiệu khác. C và D. N₁ và N₂."

- T₁ ∈ O(f) → tồn tại C ∈ ℝ⁺, n₁ ∈ ℕ sao cho T₁ ≤ C·f với n ≥ n₁
- T₂ ∈ O(g) → tồn tại D ∈ ℝ⁺, n₂ ∈ ℕ sao cho T₂ ≤ D·g với n ≥ n₂
- Khi cộng: T₁+T₂ ≤ C·f + D·g **với mọi n ≥ max(n₁, n₂)**

### 7. Chứng minh sai — phản chứng hoặc phản ví dụ

> **Buổi 5, dòng 95:** "Nghĩ nó sai đi. Giả sử cái điều này đúng rồi...
> Theo định nghĩa... biến đổi tương đương... tìm mâu thuẫn.
> Nếu phát hiện mâu thuẫn → giả sử ban đầu sai."

### 8. So sánh bậc tăng trưởng — dùng LIM

> **Buổi 5, dòng 103-107:** "Dùng giới hạn để so sánh bậc tăng trưởng.
> - lim = 0 → t nhỏ hơn g → t ∈ o(g)
> - lim = C (≠ 0) → cùng bậc → t ∈ Θ(g)
> - lim = ∞ → t lớn hơn g"

### 9. Phân lớp hàm — quy về đại diện nhóm

> **Buổi 4, dòng 115-117:** "Trong mỗi nhóm có một nhân vật được chọn ra làm đại diện.
> Mấy cái hàm nó phổ biến, gần gũi, đẹp → chọn làm đại diện → đó là bậc tăng trưởng."

Thang chuẩn: 1 ≺ log n ≺ n ≺ n log n ≺ n² ≺ n³ ≺ 2ⁿ ≺ 3ⁿ ≺ n! ≺ nⁿ

---

## 📐 Phong cách trình bày (trích từ transcript)

### Viết cho người đọc

> **Buổi 2, dòng 39:** "Viết ra chữ nào thì em phải chịu trách nhiệm với cái chữ đó."

> **Buổi 2, dòng 45:** "Thiết kế ra thứ gì đó mà người khác có thể đọc, hiểu được."

### Trình bày xấu = không điểm

> **Buổi 2, dòng 41:** "Từ chối đọc. Em viết cái chữ gì á cô đọc không ra
> nên từ chối đọc không có điểm."

### Bonus cho trình bày tốt

> **Buổi 2, dòng 39:** "Trình bày rất tốt rất xuất sắc thì cô sẽ có điểm bonus.
> Trình bày rất tệ → không điểm hoặc bị trừ điểm."

### "Mềm mại" trong lập luận

> **Buổi 4, dòng 249:** "Lâu lâu viết chữ vô cho bài giải nó mềm mại chút."

→ AI nên: thêm câu dẫn nhập ngắn, không chỉ ghi toàn ký hiệu. VD:
"Theo định nghĩa của Big O, ta cần chỉ ra..." thay vì nhảy thẳng vào BĐT.

---

## 📚 Nguồn dữ liệu (theo thứ tự ưu tiên)

1. `data/buoi4_clean.md` — **Ký hiệu tiệm cận, cách CM Big O/Omega/Theta** (core)
2. `data/buoi5_clean.md` — **Giải đề thi mẫu, dùng lim so sánh, sắp xếp hàm** (core)
3. `data/buoi2_clean.md` — **Đánh giá đệ quy + quy tắc trình bày** (context)
4. `data/buoi1_clean.md` — **Kỹ thuật đếm, tổng sigma** (context)
5. `data/buoi3_clean.md` — **Đánh giá thuật toán tiếp** (context)
6. `data/knowledge_base.json` — Segments trích xuất có score (lookup)

### Cách sử dụng

```
1. TRƯỚC KHI giải bài → search keyword trong transcript (buoi4, buoi5 trước)
2. Tìm đoạn cô giải VÍ DỤ TƯƠNG TỰ trên lớp
3. Áp dụng ĐÚNG format + lập luận cô dùng
4. KHÔNG sáng tạo thêm nếu cô không dạy
```

---

## ⚠️ Anti-patterns (TRÁNH)

| ❌ SAI | ✅ ĐÚNG | Nguồn |
|---|---|---|
| Chọn c rồi viết luôn, không lập luận | Biến đổi BĐT → suy ra c, n₀ | Buổi 4, dòng 253 |
| Viết "f = O(g)" mà thiếu "tồn tại c, n₀" | Viết đầy đủ: ∃c ∈ ℝ⁺, n₀ ∈ ℕ sao cho... | Buổi 4, dòng 373 |
| "Xét một hàm f ∈ A" (thiếu "bất kỳ") | "Xét một hàm **bất kỳ** f ∈ A" | Buổi 4, dòng 397 |
| Dùng cùng ký hiệu C cho 2 hàm khác nhau | Dùng C, D riêng biệt; n₁, n₂ riêng | Buổi 4, dòng 413 |
| Chỉ ghi ký hiệu toán, không có lời | Thêm "Theo đn của Big O", "Suy ra..." | Buổi 4, dòng 249 |
| Ghi "hiển nhiên" mà không giải thích | Biến đổi cụ thể: "vì n² ≤ n³ khi n ≥ 1" | Buổi 4, dòng 211 |
| Dùng method cô chưa dạy (VD: L'Hôpital) | Dùng định nghĩa hoặc lim (buổi 5) | Buổi 5, dòng 103 |

---

## 🔍 Checklist trước khi output bài giải

- [ ] Đã search transcript tìm ví dụ tương tự?
- [ ] Định nghĩa viết đầy đủ (tồn tại, ∈ ℝ⁺, ∈ ℕ, sao cho, với mọi)?
- [ ] Có lập luận TẠI SAO chọn c, n₀?
- [ ] Ký hiệu hằng số khác nhau cho các hàm riêng biệt?
- [ ] Có câu dẫn "Theo định nghĩa...", "Suy ra...", "ĐPCM"?
- [ ] Khi CM tập con: có "xét hàm BẤT KỲ"?
- [ ] Khi CM sai: dùng phản chứng hoặc phản ví dụ?
