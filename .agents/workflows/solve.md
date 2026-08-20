---
name: solve
description: Giải bài tập PDF theo phong cách cô Thương. Chỉ cần đường dẫn file PDF.
version: 1.0.0
requires_skills: co-thuong-style
---

# /solve — Giải bài tập tự động

$ARGUMENTS — Đường dẫn tới file PDF bài tập (bắt buộc)

---

## Purpose

Tự động giải bài tập từ file PDF, theo **đúng phong cách cô Huỳnh Thị Thanh Thương** đã dạy trên lớp. Output là file LaTeX (`_solved.tex`) nằm cùng thư mục với file PDF gốc.

---

## Pipeline (PHẢI TUÂN THỦ ĐÚNG THỨ TỰ)

### Phase 1: Extract — Đọc đề bài từ PDF

1. **Render PDF thành ảnh** để đọc chính xác:
   ```python
   # Chạy script render
   python "<project_root>/.agents/skills/solve-homework/scripts/render_pdf.py" "<pdf_path>"
   ```
   Script sẽ tạo thư mục `_pages/` cùng cấp chứa ảnh từng trang.

2. **Đọc từng ảnh** bằng `view_file` để hiểu đề bài. Ghi nhận:
   - Số lượng bài tập
   - Yêu cầu cụ thể từng bài (CM, sắp xếp, tính toán, nhận định đúng/sai...)
   - Các hàm, ký hiệu, công thức trong đề

### Phase 2: Search — Tìm bài cô đã giải

3. **Search trong transcript** (buổi 1-5) để tìm bài tương tự cô đã giải trên lớp:
   ```
   grep_search: keywords từ đề bài → data/buoi*_clean.md
   ```
   Ưu tiên search: buổi 4 (ký hiệu tiệm cận) → buổi 5 (sửa bài + đề thi) → buổi 2,3 (đệ quy, vòng lặp) → buổi 1 (tổng sigma)

4. **Đọc đoạn transcript** tìm được để hiểu CÁCH cô giải — không chỉ đáp án mà cả **cách lập luận, trình bày, ký hiệu**.

5. **Tham khảo knowledge_base.json** nếu cần thêm context:
   ```
   data/knowledge_base.json
   ```

### Phase 3: Solve — Giải theo style cô Thương

6. **Load skill `@co-thuong-style`** — ĐÂY LÀ BẮT BUỘC. Đọc file:
   ```
   .agents/skills/co-thuong-style/SKILL.md
   ```

7. **Giải từng bài** theo quy tắc:

   **Với bài cô ĐÃ GIẢI trên lớp (tìm thấy ở Phase 2):**
   - Follow CHÍNH XÁC cách cô trình bày trong transcript
   - Dùng đúng ký hiệu, cách chọn c/n₀, cách lập luận
   - Ghi chú `% Cô giải bài này ở buổi X, dòng Y` trong LaTeX

   **Với bài cô CHƯA GIẢI:**
   - BẮT BUỘC áp dụng phương pháp chứng minh bằng định nghĩa hình thức khi xác định lớp O/Θ/Ω: chặn dưới (tìm $c_1$), chặn trên (tìm $c_2$), chọn $n_0$ kèm biến đổi bất đẳng thức để giải thích tại sao chọn được các hằng số đó. KHÔNG ĐƯỢC chỉ đưa ra kết quả (như Hạng chi phối) rồi kết luận luôn.
   - Dùng style và notation nhất quán với các bài cô đã giải
   - Ghi chú `% Bài này cô chưa giải trên lớp, áp dụng phương pháp chung`

8. **Checklist từng bài** (từ skill):
   - [ ] Định nghĩa viết đầy đủ?
   - [ ] Có lập luận khi chọn c, n₀?
   - [ ] Ký hiệu hằng số khác nhau cho hàm riêng biệt?
   - [ ] Có câu dẫn "Theo định nghĩa...", "Suy ra...", "ĐPCM"?
   - [ ] CM tập con: có "xét hàm BẤT KỲ"?
   - [ ] CM sai: dùng phản chứng?

### Phase 4: Output — Tạo file LaTeX

9. **Tạo file LaTeX** tại:
   ```
   <pdf_directory>/<pdf_filename>_solved.tex
   ```
   Ví dụ: `[HW#02] ... .pdf` → `[HW#02] ... _solved.tex`

10. **LaTeX template** phải bao gồm:
    - Preamble với tiếng Việt (fontspec, polyglossia)
    - tcolorbox cho `resultbox` (kết quả, màu xanh) và `notebox` (ghi chú, màu vàng)
    - Mỗi bài tách section rõ ràng
    - Mỗi câu con tách subsection

11. **Thông báo kết quả:**
    ```
    ✅ Đã tạo file giải: <output_path>
    📋 Tổng số bài: X (cô giải: Y, tự giải: Z)
    📖 Upload lên Overleaf để compile
    ```

---

## Output Format

Sau khi hoàn tất, tạo artifact tóm tắt:

```markdown
## ✅ Giải bài tập hoàn tất

### File đầu ra
- 📄 `<tên file>_solved.tex`

### Mapping transcript
| Bài | Cô giải? | Buổi/Dòng | Phương pháp |
|-----|----------|-----------|-------------|
| 1   | ✅        | B4/267    | Phân lớp    |
| 2   | ❌        | —         | Định nghĩa  |
| ... | ...      | ...       | ...         |

### Lưu ý
- Bài X: [ghi chú cụ thể nếu có]
```

---

## Ví dụ sử dụng

```
/solve D:\Study\Cô Thương\...\[HW#02] Độ phức tạp....pdf
/solve D:\Study\Cô Thương\...\[HW#03] Đệ quy.pdf
```

---

## Key Rules

1. **KHÔNG sáng tạo** — Follow transcript, không tự chế phương pháp cô chưa dạy
2. **Transcript là nguồn sự thật DUY NHẤT** — Các file .tex trong `data/` là AI gen, KHÔNG phải của cô
3. **Viết đầy đủ** — Thiếu ∃, ∈ ℝ⁺, ∀n ≥ n₀ = bị trừ điểm
4. **Lập luận rồi mới kết luận** — Không "chọn c rồi viết luôn"
5. **Hỏi user khi không chắc** — Nếu bài quá khác so với transcript, hỏi trước khi giải
6. **KHÔNG văn vẻ kiểu AI (AI Slop)** — Tuyệt đối không dùng các từ như "Lập luận:", "Giải thích:", "Dựa vào định nghĩa...". Chỉ dùng biểu thức toán học cực kỳ ngắn gọn (VD: `Ta có: lg* n = 1 + lg*(lg n) \Rightarrow ...`). Tối giản chữ, tối đa công thức.
