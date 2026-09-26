# Thuong-cho-tam-than-co-han-de-vuot-qua-mon-thuat toán :3

> Hệ thống AI tái tạo hành vi giải bài tập thuật toán theo phong cách **GV Huỳnh Thị Thanh Thương** — Môn Phân tích & Thiết kế Thuật toán.

Dự án này sử dụng mô hình ngôn ngữ lớn (Google Gemini) kết hợp với kỹ thuật **Few-shot Prompting** và **Persona Prompting** để tạo ra các lời giải bài tập thuật toán bằng LaTeX, mô phỏng chính xác giọng điệu, cách lập luận và format trình bày của Cô Thương.

---

## 🏗 Kiến trúc hệ thống (Architecture)

Hệ thống được thiết kế theo mô hình **Pipeline 3 lớp (3-Tier Pipeline)**, tập trung vào việc tiền xử lý dữ liệu để làm ngữ cảnh (context) cho LLM thay vì sử dụng RAG/Vector DB phức tạp do lượng dữ liệu hiện tại (5 buổi học) là tương đối nhỏ gọn.

### 1. Lớp Dữ liệu (Data Layer) - `data/`
Chịu trách nhiệm thu thập và cấu trúc hóa "hành vi" và "phong cách" của giảng viên:
- **`download_subtitles.py`**: Tự động đồng bộ hóa với [Playlist YouTube bài giảng](https://youtube.com/playlist?list=PLapjV_I0Y4vU&si=3h00kxl1mFBHzblm). Script tải các auto-generated subtitle (`.vtt`), sau đó tự động clean timestamp, tag HTML để chuyển thành text thuần (`_clean.md`).
- **`build_knowledge_base.py`**: Quét toàn bộ transcript (`.md`) và các bài mẫu LaTeX (`.tex`), chấm điểm mức độ liên quan (relevance score) dựa trên keyword để trích xuất các **Teaching Segments** (đoạn cô giảng/giải bài) và **LaTeX Examples**.
- **`knowledge_base.json`**: Đầu ra của lớp dữ liệu. Một cơ sở dữ liệu tĩnh được LLM load trực tiếp vào RAM mỗi khi chạy.

### 2. Lớp Cốt lõi AI (AI Core Layer) - `core/`
Chịu trách nhiệm điều phối LLM và định hình kết quả đầu ra:
- **`persona.py` (Bộ não)**: Chứa System Prompt cực kỳ chi tiết. Ép LLM xưng hô bình dân, lập luận từng bước (đưa về chuẩn → phân lớp → so sánh), cách cho điểm (0.25/0.5), và tuân thủ các công thức/mẹo mà cô hay dùng.
- **`latex_template.py` (Khuôn đúc)**: Chứa Preamble cứng của LaTeX. Đảm bảo file `.tex` sinh ra luôn có đúng package, đúng định nghĩa màu sắc (`mainblue`), hộp kết quả (`resultbox`), và hộp lưu ý (`notebox`).
- **`solver.py` (Động cơ)**: Đọc đề bài → Query Knowledge Base lấy ví dụ mẫu (Few-shot) → Ghép vào Persona → Gọi Gemini API → Parse kết quả LLM → Bọc vào LaTeX Template.

### 3. Lớp Giao diện (Interface Layer) - `solve.py`
Cung cấp CLI (Command Line Interface) cho người dùng cuối tương tác với hệ thống. Cho phép giải bài tập đơn lẻ, giải qua file, hoặc chạy chế độ tương tác (interactive).

---

## 🚀 Các lệnh cần biết (Commands)

### 1. Cài đặt và cấu hình ban đầu
Mặc định solver gọi model qua **Antigravity CLI (`agy`)**, đăng nhập bằng tài khoản Google, không cần API key:

```bash
# 1. Cài agy và đăng nhập (chạy agy 1 lần, làm theo hướng dẫn login)
brew install --cask antigravity-cli
agy

# 2. (Tuỳ chọn) chọn model, xem danh sách bằng: agy models
python solve.py --setup
```

Muốn dùng Gemini API key thay cho agy (fallback):
```bash
pip install -r requirements.txt
python solve.py --provider gemini --api-key <KEY> -p "..."
# hoặc: export COTHUONG_PROVIDER=gemini GEMINI_API_KEY=<KEY>
```
*(API Key lấy tại [Google AI Studio](https://aistudio.google.com/apikey))*

### 2. Cập nhật dữ liệu (Data Pipeline)
Khi playlist trên YouTube có video buổi học mới, bạn cần chạy 2 lệnh sau để hệ thống "học" thêm kiến thức mới:

```bash
# 1. Tải subtitle cho các video mới (bỏ qua video đã tải)
python -m data.download_subtitles

# 2. Build lại file knowledge_base.json để cập nhật vào não LLM
python -m data.build_knowledge_base
```

### 3. Giải bài tập

#### Cách 1: `/solve` — Giải tự động từ file PDF (Khuyến nghị)

Mở Antigravity IDE (hoặc bất kỳ AI IDE nào hỗ trợ `.agents/workflows/`) và gõ:

```
/solve D:\Study\Cô Thương\...\[HW#02] Độ phức tạp....pdf
```

Chỉ cần **1 đường dẫn PDF**, hệ thống tự động chạy pipeline 4 bước:

| Bước | Hành động | Chi tiết |
|------|----------|----------|
| **1. Extract** | Render PDF → ảnh PNG | Đọc đề bài chính xác từ ảnh |
| **2. Search** | Tìm transcript buổi 1-9 | Xác định bài nào cô đã giải trên lớp |
| **3. Solve** | Giải theo `@co-thuong-style` | Đúng ký hiệu, cách lập luận, format cô dạy |
| **4. Output** | Tạo file `_solved.tex` | Cùng thư mục với PDF gốc |

> ⚠️ Workflow này dựa trên transcript thực tế từ buổi giảng của cô, không phải AI đoán mò.

> ℹ️ `/solve` chạy trong IDE (hoặc `agy` interactive) để duyệt từng lệnh. Chạy headless `agy -p "/solve ..."` sẽ **không ra kết quả**: workflow cần chạy lệnh shell, headless tự từ chối nếu chưa cấp quyền `command(...)` trong `~/.gemini/antigravity-cli/settings.json`. Không nên dùng `--dangerously-skip-permissions` trên repo thật.

#### Cách 2: CLI truyền thống (`solve.py`)

**Giải nhanh một bài từ Terminal:**
```bash
python solve.py --problem "Sắp xếp các hàm sau theo bậc tăng trưởng: n², 2^n, n·log(n), n!" --output bai_giai.tex --pdf
```
*(Lưu `bai_giai.tex`, thêm `--pdf` để biên dịch luôn ra `bai_giai.pdf` bằng [tectonic](https://tectonic-typesetting.github.io): `brew install tectonic`. Lần đầu tectonic tải package mất vài phút.)*

**Giải thẳng file PDF đề (không cần người trông, chỉ provider agy):**
```bash
python solve.py --input-pdf "bai_tap/Đề thi mẫu/Đề mẫu/CS112_De_Thi_Mau_So_01.pdf" -o de01.tex --pdf
python solve.py --input-pdf "bai_tap/[HW#02] ....pdf" --pages 17-26 -o hw02.tex --pdf   # chỉ trang bài tập
```
*(Render từng trang thành ảnh cho agy đọc trong thư mục tạm, không cấp quyền shell. Timeout mặc định 20m, đổi bằng `--timeout 30m`. Cần `pymupdf` trong requirements. LaTeX do model sinh đôi khi vẫn lỗi cú pháp, lúc đó `.tex` vẫn được lưu để sửa tay.)*

**Chạy test** (offline, không tốn quota): `python3 -m unittest discover -s tests -t .`

**Giải bài từ một file text chứa đề dài:**
```bash
python solve.py --problem-file de_bai.txt --output bai_giai.tex
```

**Bật chế độ chat tương tác (Interactive Mode):**
```bash
# Thích hợp khi bạn muốn giải liên tục nhiều bài mà không cần gõ lệnh dài
python solve.py --interactive
```

**Sử dụng model LLM khác (ví dụ cần thông minh hơn):**
```bash
python solve.py --model gemini-2.5-pro --problem "..."
```

---

## 📁 Cây thư mục

```
thuong-cho-tam-than-co-han/
├── .agents/                                # AI Agent system
│   ├── skills/
│   │   ├── co-thuong-style/SKILL.md        # Quy tắc trình bày của cô (từ transcript)
│   │   └── solve-homework/                 # Pipeline giải bài tập
│   │       ├── SKILL.md
│   │       └── scripts/render_pdf.py       # Render PDF → PNG
│   ├── workflows/
│   │   └── solve.md                        # /solve command
│   └── rules/                              # Luật routing, code, protocol
├── data/
│   ├── buoi1.vi.vtt, buoi1_clean.md, ...   # Raw data (subtitle, transcript)
│   ├── loi_giai_so_sanh_thuat_toan.tex     # Mẫu LaTeX
│   ├── download_subtitles.py
│   ├── build_knowledge_base.py
│   └── knowledge_base.json                 # DB đã parse
├── bai_tap/                                # Đề bài PDF + lời giải _solved.tex
├── core/
│   ├── config.py
│   ├── persona.py
│   ├── latex_template.py
│   └── solver.py
├── solve.py                                # CLI
├── config.json                             # Sinh ra sau khi chạy --setup (gitignored)
├── requirements.txt
└── README.md
```
