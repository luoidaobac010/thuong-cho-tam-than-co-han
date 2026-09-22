import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def set_cell_border(cell, **kwargs):
    """
    kwargs: top, bottom, left, right
    values: dict(sz=12, val='single', color='003366', space='0')
    """
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}/>')
    for border_name, border_props in kwargs.items():
        node = parse_xml(f'<w:{border_name} {nsdecls("w")} '
                         f'w:val="{border_props.get("val", "single")}" '
                         f'w:sz="{border_props.get("sz", 4)}" '
                         f'w:space="{border_props.get("space", 0)}" '
                         f'w:color="{border_props.get("color", "auto")}"/>')
        tcBorders.append(node)
    tcPr.append(tcBorders)

def add_answer_box(doc, lines=6, placeholder="Phần làm bài của sinh viên:"):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "F9FAFB")
    set_cell_border(cell, 
                    top=dict(val="single", sz=4, color="D1D5DB"),
                    bottom=dict(val="single", sz=4, color="D1D5DB"),
                    left=dict(val="single", sz=12, color="3B82F6"),
                    right=dict(val="single", sz=4, color="D1D5DB"))
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(f"✎ {placeholder}")
    run.font.size = Pt(9.5)
    run.font.italic = True
    run.font.color.rgb = RGBColor(107, 114, 128)
    
    for _ in range(lines):
        p_line = cell.add_paragraph()
        p_line.paragraph_format.space_after = Pt(12)
        r = p_line.add_run("....................................................................................................................................................................")
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(209, 213, 219)
        
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def create_document():
    doc = Document()
    
    # Page setup - Margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.7)
        section.bottom_margin = Inches(0.7)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)
        
    # Set default styles
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(11)
    font.color.rgb = RGBColor(30, 41, 59)
    
    # --- HEADER TABLE ---
    header_table = doc.add_table(rows=1, cols=2)
    header_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    header_table.autofit = False
    
    cell_left = header_table.cell(0, 0)
    cell_left.width = Inches(3.2)
    p_left = cell_left.paragraphs[0]
    p_left.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_left.add_run("ĐẠI HỌC QUỐC GIA TP.HCM\n")
    r.font.bold = True
    r.font.size = Pt(10)
    r = p_left.add_run("TRƯỜNG ĐH KHOA HỌC TỰ NHIÊN / UIT\n")
    r.font.bold = True
    r.font.size = Pt(10)
    r = p_left.add_run("KHOA CÔNG NGHỆ THÔNG TIN\n------------------")
    r.font.size = Pt(9.5)
    
    cell_right = header_table.cell(0, 1)
    cell_right.width = Inches(3.3)
    p_right = cell_right.paragraphs[0]
    p_right.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_right.add_run("ĐỀ THI CUỐI KỲ & SƯỜN CẤU TRÚC ĐỀ\n")
    r.font.bold = True
    r.font.size = Pt(10.5)
    r.font.color.rgb = RGBColor(185, 28, 28)
    r = p_right.add_run("Môn: PHÂN TÍCH VÀ THIẾT KẾ THUẬT TOÁN\n")
    r.font.bold = True
    r.font.size = Pt(10)
    r = p_right.add_run("GV phụ trách: ThS. Huỳnh Thị Thanh Thương\n(Trích xuất từ file Word chia sẻ tại Buổi học 9)")
    r.font.italic = True
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(75, 85, 99)
    
    p_sep = doc.add_paragraph()
    p_sep.paragraph_format.space_before = Pt(4)
    p_sep.paragraph_format.space_after = Pt(8)
    
    # --- META INFO BOX ---
    info_table = doc.add_table(rows=1, cols=1)
    info_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_info = info_table.cell(0, 0)
    cell_info.width = Inches(6.5)
    set_cell_background(cell_info, "EFF6FF")
    set_cell_border(cell_info, 
                    top=dict(val="single", sz=6, color="3B82F6"),
                    bottom=dict(val="single", sz=6, color="3B82F6"),
                    left=dict(val="single", sz=6, color="3B82F6"),
                    right=dict(val="single", sz=6, color="3B82F6"))
    set_cell_margins(cell_info, top=100, bottom=100, left=150, right=150)
    
    p_info = cell_info.paragraphs[0]
    p_info.paragraph_format.space_after = Pt(2)
    p_info.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p_info.add_run("• Thời gian làm bài: ")
    r.font.bold = True
    p_info.add_run("90 phút.   ")
    r = p_info.add_run("• Hình thức thi: ")
    r.font.bold = True
    p_info.add_run("Tự luận (Sinh viên làm bài trực tiếp trên đề thi).   \n")
    r = p_info.add_run("• Cấu trúc điểm: ")
    r.font.bold = True
    p_info.add_run("Đề gồm 2 phần: Phân tích (6.0 điểm) + Thiết kế (6.0 điểm) = ")
    r = p_info.add_run("12.0 ĐIỂM")
    r.font.bold = True
    r.font.color.rgb = RGBColor(185, 28, 28)
    p_info.add_run(" (Thang điểm chấm có thể mở rộng/bonus lên tới 14 - 15 điểm).")
    
    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    
    # --- WARNING / LƯU Ý SỐNG CÒN ---
    warn_table = doc.add_table(rows=1, cols=1)
    warn_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_warn = warn_table.cell(0, 0)
    cell_warn.width = Inches(6.5)
    set_cell_background(cell_warn, "FEF2F2")
    set_cell_border(cell_warn, 
                    top=dict(val="single", sz=10, color="EF4444"),
                    bottom=dict(val="single", sz=10, color="EF4444"),
                    left=dict(val="single", sz=18, color="DC2626"),
                    right=dict(val="single", sz=10, color="EF4444"))
    set_cell_margins(cell_warn, top=120, bottom=120, left=160, right=160)
    
    p_warn_title = cell_warn.paragraphs[0]
    p_warn_title.paragraph_format.space_after = Pt(4)
    r = p_warn_title.add_run("🚨 QUY CHẾ VÀ LƯU Ý SỐNG CÒN TRONG PHÒNG THI (CÔ THƯƠNG QUÁN TRIỆT)")
    r.font.bold = True
    r.font.size = Pt(10.5)
    r.font.color.rgb = RGBColor(185, 28, 28)
    
    p_w1 = cell_warn.add_paragraph()
    p_w1.paragraph_format.space_after = Pt(3)
    r = p_w1.add_run("1. Tài liệu cho phép: ")
    r.font.bold = True
    p_w1.add_run("Sinh viên chỉ được mang vào phòng thi ")
    r = p_w1.add_run("DUY NHẤT 01 TỜ GIẤY A4 VIẾT TAY")
    r.font.bold = True
    r.font.underline = True
    p_w1.add_run(" (sử dụng 2 mặt trước và sau). Tuyệt đối không mang giấy in photo hay nhiều hơn 1 tờ.")
    
    p_w2 = cell_warn.add_paragraph()
    p_w2.paragraph_format.space_after = Pt(3)
    r = p_w2.add_run("2. Kỷ luật thi & Gian lận: ")
    r.font.bold = True
    p_w2.add_run("Cô chấm bài trực tiếp và hậu kiểm từng bài. Tuyệt đối cấm sử dụng điện thoại, AI giải đề hay trốn ra toilet tra cứu. Nếu phát hiện vi phạm: ")
    r = p_w2.add_run("0 ĐIỂM TOÀN BỘ BÀI THI & 0 ĐIỂM TOÀN BỘ MÔN HỌC (RỚT MÔN, KHÔNG CỨU VỚT).")
    r.font.bold = True
    r.font.color.rgb = RGBColor(185, 28, 28)
    
    p_w3 = cell_warn.add_paragraph()
    p_w3.paragraph_format.space_after = Pt(3)
    r = p_w3.add_run("3. Quy định Mã giả (Pseudo-code): ")
    r.font.bold = True
    p_w3.add_run("Môn học là Thiết kế thuật toán, KHÔNG ép buộc cú pháp C++/Python/Java chuẩn. Chỉ cần viết Mã giả có đánh số bước (Bước 1, Bước 2,...), chú thích biến và cấu trúc dữ liệu rõ ràng. ")
    r = p_w3.add_run("Không vẽ lưu đồ (flowchart).")
    r.font.italic = True
    
    p_w4 = cell_warn.add_paragraph()
    p_w4.paragraph_format.space_after = Pt(2)
    r = p_w4.add_run("4. Nội dung giảm tải (Không thi): ")
    r.font.bold = True
    p_w4.add_run("Bỏ ")
    r = p_w4.add_run("Định lý Thợ (Master Theorem)")
    r.font.bold = True
    p_w4.add_run(" và bỏ bài toán giải tối ưu bằng ")
    r = p_w4.add_run("Thuật toán Ford-Fulkerson (tìm luồng cực đại)")
    r.font.bold = True
    p_w4.add_run(" do tính toán dài mất nhiều thời gian.")
    
    doc.add_paragraph().paragraph_format.space_after = Pt(8)
    
    # --- PHẦN I ---
    p_part1 = doc.add_paragraph()
    p_part1.paragraph_format.space_before = Pt(12)
    p_part1.paragraph_format.space_after = Pt(4)
    r = p_part1.add_run("PHẦN I: PHÂN TÍCH THUẬT TOÁN (6.0 ĐIỂM)")
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = RGBColor(30, 58, 138)
    
    # Câu 1
    p_c1 = doc.add_paragraph()
    p_c1.paragraph_format.space_after = Pt(3)
    r = p_c1.add_run("Câu 1: Ký hiệu tiệm cận (2.0 điểm)\n")
    r.font.bold = True
    r.font.size = Pt(11.5)
    
    p_c1_a = doc.add_paragraph()
    p_c1_a.paragraph_format.space_after = Pt(2)
    r = p_c1_a.add_run("a) (1.0 điểm) ")
    r.font.bold = True
    p_c1_a.add_run("Chứng minh tính đúng/sai của các khẳng định sau bằng định nghĩa toán học của ký hiệu tiệm cận:\n")
    p_c1_a.add_run("   • Khẳng định 1 (0.5đ): ")
    r_k1 = p_c1_a.add_run("3n² + 5n + 10 = O(n²)")
    r_k1.font.bold = True
    p_c1_a.add_run("\n   • Khẳng định 2 (0.5đ): ")
    r_k2 = p_c1_a.add_run("n! = Ω(2ⁿ)  (hoặc chứng minh một đẳng thức tiệm cận với Θ/Ω)")
    r_k2.font.bold = True
    add_answer_box(doc, lines=6, placeholder="Trình bày chứng minh: tìm các hằng số c > 0, n0 > 0 thỏa định nghĩa:")
    
    p_c1_b = doc.add_paragraph()
    p_c1_b.paragraph_format.space_after = Pt(2)
    r = p_c1_b.add_run("b) (1.0 điểm) ")
    r.font.bold = True
    p_c1_b.add_run("Cho danh sách các hàm số độ phức tạp sau đây:\n")
    r_funcs = p_c1_b.add_run("   f₁(n) = n·log(n),   f₂(n) = 10000,   f₃(n) = 2ⁿ,   f₄(n) = n²,   f₅(n) = √n,   f₆(n) = n!,   f₇(n) = n^(log n)\n")
    r_funcs.font.bold = True
    p_c1_b.add_run("Yêu cầu: Hãy phân lớp (group) các hàm số và sắp xếp theo thứ tự độ phức tạp thời gian tăng dần (dùng ký hiệu O lớn). Phải giải thích/biến đổi ngắn gọn tại sao hàm thuộc nhóm đó.")
    add_answer_box(doc, lines=5, placeholder="Bảng phân lớp, các bước biến đổi trung gian và kết luận thứ tự sắp xếp chốt:")

    # Câu 2
    p_c2 = doc.add_paragraph()
    p_c2.paragraph_format.space_before = Pt(8)
    p_c2.paragraph_format.space_after = Pt(3)
    r = p_c2.add_run("Câu 2: Phân tích thuật toán & Đếm phép toán (3.0 điểm)\n")
    r.font.bold = True
    r.font.size = Pt(11.5)
    
    p_c2_a = doc.add_paragraph()
    p_c2_a.paragraph_format.space_after = Pt(2)
    r = p_c2_a.add_run("a) Phân tích thuật toán không đệ quy (1.0 điểm): ")
    r.font.bold = True
    p_c2_a.add_run("Cho đoạn mã lặp sau đây:\n")
    
    # Code block
    code_table = doc.add_table(rows=1, cols=1)
    code_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_cell = code_table.cell(0,0)
    c_cell.width = Inches(6.5)
    set_cell_background(c_cell, "F3F4F6")
    set_cell_margins(c_cell, 80, 80, 120, 120)
    p_code = c_cell.paragraphs[0]
    p_code.paragraph_format.space_after = Pt(0)
    r_code = p_code.add_run(
        "Algorithm ProcessMatrix(A[1..n, 1..n])\n"
        "1.  count = 0\n"
        "2.  for i = 1 to n do\n"
        "3.      for j = i to n do\n"
        "4.          if A[i, j] > 0 then\n"
        "5.              count = count + A[i, j]\n"
        "6.  return count"
    )
    r_code.font.name = "Courier New"
    r_code.font.size = Pt(9.5)
    
    p_c2_a_req = doc.add_paragraph()
    p_c2_a_req.paragraph_format.space_before = Pt(4)
    p_c2_a_req.paragraph_format.space_after = Pt(2)
    p_c2_a_req.add_run("   1. Xác định Input, Output và Chức năng của thuật toán trên.\n"
                       "   2. Đếm chính xác số phép so sánh (hoặc phép gán) thực hiện theo n (trình bày cách suy luận công thức tổng ∑).\n"
                       "   3. Kết luận độ phức tạp thời gian theo O lớn.")
    add_answer_box(doc, lines=5, placeholder="Trình bày Input, Output, Chức năng, phương pháp đếm tổng quát và độ phức tạp:")

    p_c2_b = doc.add_paragraph()
    p_c2_b.paragraph_format.space_after = Pt(2)
    r = p_c2_b.add_run("b) Phân tích thuật toán đệ quy (1.0 điểm): ")
    r.font.bold = True
    p_c2_b.add_run("Cho giải thuật đệ quy sau:\n")
    
    code_table_b = doc.add_table(rows=1, cols=1)
    code_table_b.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_cell_b = code_table_b.cell(0,0)
    c_cell_b.width = Inches(6.5)
    set_cell_background(c_cell_b, "F3F4F6")
    set_cell_margins(c_cell_b, 80, 80, 120, 120)
    p_code_b = c_cell_b.paragraphs[0]
    p_code_b.paragraph_format.space_after = Pt(0)
    r_code_b = p_code_b.add_run(
        "Algorithm RecursiveCount(A[1..n])\n"
        "1.  if n == 1 return A[1]\n"
        "2.  mid = n / 2\n"
        "3.  left_sum = RecursiveCount(A[1..mid])\n"
        "4.  right_sum = RecursiveCount(A[mid+1..n])\n"
        "5.  return left_sum + right_sum"
    )
    r_code_b.font.name = "Courier New"
    r_code_b.font.size = Pt(9.5)
    
    p_c2_b_req = doc.add_paragraph()
    p_c2_b_req.paragraph_format.space_before = Pt(4)
    p_c2_b_req.paragraph_format.space_after = Pt(2)
    p_c2_b_req.add_run("Yêu cầu: Thiết lập phương trình truy hồi T(n) và giải thích ngắn gọn cơ sở thành lập phương trình.")
    add_answer_box(doc, lines=4, placeholder="Phương trình truy hồi T(n) và giải thích:")

    p_c2_c = doc.add_paragraph()
    p_c2_c.paragraph_format.space_after = Pt(2)
    r = p_c2_c.add_run("c) Giải phương trình đệ quy (1.0 điểm): ")
    r.font.bold = True
    p_c2_c.add_run("Sinh viên được chọn ")
    r_ch = p_c2_c.add_run("1 TRONG 3")
    r_ch.font.bold = True
    p_c2_c.add_run(" phương trình đệ quy sau đây để giải (sử dụng phương pháp đã chỉ định tương ứng):\n"
                   "   • Phương trình 1: T(n) = 2T(n/2) + n, với T(1) = 1 (Giải bằng Phương pháp thế / Truy hồi lặp).\n"
                   "   • Phương trình 2: T(n) = 5T(n-1) - 6T(n-2), với T(0) = 1, T(1) = 4 (Giải bằng Phương trình đặc trưng).\n"
                   "   • Phương trình 3: T(n) = T(n-1) + n, với T(0) = 0 (Giải bằng Hàm sinh / Biến đổi đại số).")
    add_answer_box(doc, lines=6, placeholder="Chọn phương trình số ... và trình bày các bước giải chi tiết:")

    # --- PHẦN II ---
    p_part2 = doc.add_paragraph()
    p_part2.paragraph_format.space_before = Pt(14)
    p_part2.paragraph_format.space_after = Pt(4)
    r = p_part2.add_run("PHẦN II: THIẾT KẾ THUẬT TOÁN (6.0 ĐIỂM)")
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = RGBColor(30, 58, 138)
    
    p_p2_note = doc.add_paragraph()
    p_p2_note.paragraph_format.space_after = Pt(4)
    r = p_p2_note.add_run("★ Lưu ý chấm thi của Cô Thương: ")
    r.font.bold = True
    r.font.color.rgb = RGBColor(4, 120, 87)
    p_p2_note.add_run("Trong trường hợp sinh viên chưa xây dựng được mã giả hoàn chỉnh, hãy trình bày ")
    r_idea = p_p2_note.add_run("Ý tưởng / Chiến lược thiết kế")
    r_idea.font.bold = True
    p_p2_note.add_run(" một cách mạch lạc, có ví dụ minh họa để vẫn nhận được điểm phần ý tưởng.")

    # Câu 3
    p_c3 = doc.add_paragraph()
    p_c3.paragraph_format.space_after = Pt(2)
    r = p_c3.add_run("Câu 3: Phân tích bài toán & Ý tưởng thiết kế (2.0 điểm)\n")
    r.font.bold = True
    r.font.size = Pt(11.5)
    p_c3.add_run("Sinh viên chọn ")
    r_sel3 = p_c3.add_run("1 TRONG 2 BÀI TOÁN")
    r_sel3.font.bold = True
    p_c3.add_run(" sau đây để phân tích:\n"
                 "   • Bài toán 3.1: Cho dãy n số nguyên A[1..n]. Tìm đoạn con liên tiếp có tổng lớn nhất bằng chiến lược Chia để trị (Divide and Conquer).\n"
                 "   • Bài toán 3.2: Bài toán Lựa chọn công việc (Activity Selection Problem) - Cho n công việc với thời gian bắt đầu si và kết thúc fi. Tìm tập công việc tương thích tối đa bằng chiến lược Tham lam (Greedy).")
    
    p_c3_req = doc.add_paragraph()
    p_c3_req.paragraph_format.space_after = Pt(2)
    p_c3_req.add_run("Yêu cầu cần trình bày:\n"
                     "   1. Xác định Input, Output và 1 ví dụ cụ thể do đề cho (hoặc tự cho ví dụ).\n"
                     "   2. Trình bày ý tưởng / chiến lược giải thuật (Chưa cần viết mã giả).\n"
                     "   3. Minh họa ý tưởng chạy từng bước trên ví dụ cụ thể.")
    add_answer_box(doc, lines=6, placeholder="Phân tích Input/Output, chiến lược và minh họa ý tưởng:")

    # Câu 4
    p_c4 = doc.add_paragraph()
    p_c4.paragraph_format.space_before = Pt(8)
    p_c4.paragraph_format.space_after = Pt(2)
    r = p_c4.add_run("Câu 4: Triển khai Mã giả thuật toán & Đánh giá (2.0 điểm)\n")
    r.font.bold = True
    r.font.size = Pt(11.5)
    p_c4.add_run("Cho bài toán: Thiết kế thuật toán tìm cặp điểm gần nhất (Closest Pair of Points) trên mặt phẳng 2D sử dụng kỹ thuật Chia để trị (hoặc bài toán Quay lui sinh dãy nhị phân/hoán vị có ràng buộc).\n"
                 "Yêu cầu:\n"
                 "   1. Viết Mã giả (Pseudo-code) có đánh số thứ tự từng bước (Bước 1, Bước 2,...).\n"
                 "   2. Giải thích rõ ràng các biến, mảng hoặc cấu trúc dữ liệu được sử dụng.\n"
                 "   3. Đánh giá độ phức tạp thời gian (Time Complexity) và không gian (Space Complexity).")
    add_answer_box(doc, lines=7, placeholder="Viết mã giả có đánh số bước và phân tích độ phức tạp:")

    # Câu 5
    p_c5 = doc.add_paragraph()
    p_c5.paragraph_format.space_before = Pt(8)
    p_c5.paragraph_format.space_after = Pt(2)
    r = p_c5.add_run("Câu 5: Thiết kế thuật toán Quy hoạch động (Dynamic Programming) (2.0 điểm - TRỌNG TÂM)\n")
    r.font.bold = True
    r.font.size = Pt(11.5)
    r.font.color.rgb = RGBColor(185, 28, 28)
    p_c5.add_run("Sinh viên chọn ")
    r_sel5 = p_c5.add_run("1 TRONG 2 BÀI TOÁN QUY HOẠCH ĐỘNG")
    r_sel5.font.bold = True
    p_c5.add_run(" sau đây:\n"
                 "   • Bài toán 5.1: Nhân chuỗi ma trận (Matrix Chain Multiplication - MCM) - Tìm thứ tự đặt dấu ngoặc tối ưu cho tích A₁ × A₂ × ... × An để số phép nhân vô hướng là nhỏ nhất.\n"
                 "   • Bài toán 5.2: Tính tổ hợp chập k của n (C(n, k)) hoặc Bài toán Cái túi 0/1 (0-1 Knapsack Problem) bằng tiếp cận Bottom-Up.")
    
    p_c5_req = doc.add_paragraph()
    p_c5_req.paragraph_format.space_after = Pt(2)
    p_c5_req.add_run("Yêu cầu các bước bắt buộc:\n"
                     "   1. Phân tích 2 tính chất nền tảng: Cấu trúc con tối ưu (Optimal Substructure) và Bài toán con gối nhau (Overlapping Subproblems).\n"
                     "   2. Xác định Bài toán cơ sở (Base cases / Điều kiện dừng).\n"
                     "   3. Thiết lập Phương trình Quy hoạch động (Phương trình truy hồi) và giải thích các biến số.\n"
                     "   4. Xác định kích thước bảng và Thứ tự điền bảng (Bottom-Up: điền theo hàng, cột hay đường chéo song song đường chéo chính).\n"
                     "   5. Thực hiện việc điền bảng tính toán trên một ví dụ cụ thể do đề cho.\n"
                     "   6. (Bonus) Nêu giải thuật truy vết (Traceback) để tìm nghiệm tối ưu.")
    add_answer_box(doc, lines=8, placeholder="Trình bày đầy đủ 5 bước Quy hoạch động (Cơ sở, Phương trình, Bảng DP, Điền bảng, Truy vết):")

    # --- TRANG DỰ PHÒNG ---
    doc.add_page_break()
    p_backup_title = doc.add_paragraph()
    p_backup_title.paragraph_format.space_before = Pt(14)
    p_backup_title.paragraph_format.space_after = Pt(4)
    r = p_backup_title.add_run("TRANG GIẤY DỰ PHÒNG (DÀNH CHO SINH VIÊN LÀM LẠI BÀI KHI BỊ HỦY / SAI SÓT)")
    r.font.bold = True
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(107, 114, 128)
    
    p_backup_sub = doc.add_paragraph()
    p_backup_sub.paragraph_format.space_after = Pt(8)
    r = p_backup_sub.add_run("(Ghi rõ làm lại cho Câu số mấy và gạch chéo phần bài làm bị hủy ở phía trên)")
    r.font.italic = True
    r.font.size = Pt(10)
    
    for _ in range(22):
        p_l = doc.add_paragraph()
        p_l.paragraph_format.space_after = Pt(14)
        r = p_l.add_run("..................................................................................................................................................................................................")
        r.font.color.rgb = RGBColor(209, 213, 219)
        r.font.size = Pt(9)

    out_docx = "/Users/thangdo/www/thuong-cho-tam-than-co-han/bai_tap/Đề thi mẫu/De_Thi_Va_Cau_Truc_PTTKTT_Co_Thuong_Buoi_9.docx"
    doc.save(out_docx)
    print(f"✓ Saved DOCX to: {out_docx}")

if __name__ == "__main__":
    create_document()
