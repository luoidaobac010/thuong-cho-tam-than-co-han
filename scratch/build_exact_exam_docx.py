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

def add_underline_lines(doc, num_lines=3, space_after=18):
    for _ in range(num_lines):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(space_after / 2)
        p.paragraph_format.space_after = Pt(space_after / 2)
        pPr = p._p.get_or_add_pPr()
        pBdr = parse_xml(f'''
            <w:pBdr {nsdecls("w")}>
                <w:bottom w:val="single" w:sz="6" w:space="1" w:color="333333"/>
            </w:pBdr>
        ''')
        pPr.append(pBdr)

def build_exact_docx():
    doc = Document()
    
    # Page setup
    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)
        
        # Add footer "Trang X / 10 – Đề"
        footer = s.footer
        f_p = footer.paragraphs[0]
        f_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        f_run = f_p.add_run("Trang 1 / 10 – Đề")
        f_run.font.name = "Times New Roman"
        f_run.font.size = Pt(11)
        f_run.font.color.rgb = RGBColor(70, 70, 70)

    # Styles
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    font.color.rgb = RGBColor(0, 0, 0)
    
    # --- PAGE 1 ---
    # Header Table
    h_table = doc.add_table(rows=1, cols=2)
    h_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    h_table.autofit = False
    
    c_left = h_table.cell(0, 0)
    c_left.width = Inches(3.2)
    p_l = c_left.paragraphs[0]
    p_l.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_l.add_run("TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN\nTRUNG TÂM PHÁT TRIỂN CNTT\n\nĐề: ............")
    r.font.bold = True
    r.font.size = Pt(11.5)
    
    c_right = h_table.cell(0, 1)
    c_right.width = Inches(3.4)
    p_r = c_right.paragraphs[0]
    p_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_r.add_run("ĐỀ THI CUỐI HỌC KỲ III (2025-2026)\nMÔN: CS112 - PHÂN TÍCH VÀ THIẾT KẾ THUẬT TOÁN\n")
    r.font.bold = True
    r.font.size = Pt(11.5)
    r_time = p_r.add_run("Thời gian: 90 phút")
    r_time.font.italic = True
    r_time.font.size = Pt(11)
    
    p_space = doc.add_paragraph()
    p_space.paragraph_format.space_before = Pt(4)
    p_space.paragraph_format.space_after = Pt(2)
    
    # Sub-header: (Sinh viên chỉ được phép sử dụng 01 tờ giấy A4 viết tay)
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(4)
    r_sub = p_sub.add_run("(Sinh viên chỉ được phép sử dụng 01 tờ giấy A4 viết tay)")
    r_sub.font.bold = True
    r_sub.font.italic = True
    r_sub.font.size = Pt(11)
    
    # Highlight Box: Bài làm có dấu hiệu gian lận...
    p_warn = doc.add_paragraph()
    p_warn.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_warn.paragraph_format.space_after = Pt(10)
    r_warn = p_warn.add_run("Bài làm có dấu hiệu gian lận như sao chép lẫn nhau, sử dụng công cụ AI, dùng điện thoại tra cứu, ... sẽ bị 0 điểm và hủy kết quả học phần")
    r_warn.font.bold = True
    r_warn.font.italic = True
    r_warn.font.size = Pt(11)
    r_warn.font.color.rgb = RGBColor(185, 28, 28)
    
    # Student Info Table
    info_table = doc.add_table(rows=1, cols=3)
    info_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    info_table.autofit = False
    
    c1 = info_table.cell(0, 0)
    c1.width = Inches(3.6)
    set_cell_border(c1, top=dict(val="single", sz=6), bottom=dict(val="single", sz=6), left=dict(val="single", sz=6), right=dict(val="single", sz=6))
    set_cell_margins(c1, top=100, bottom=100, left=120, right=120)
    p1 = c1.paragraphs[0]
    p1.paragraph_format.space_after = Pt(3)
    p1.add_run("HỌ VÀ TÊN SV: ....................................................\n\n"
               "MSSV: .....................................................................\n\n"
               "STT: .......................................................................\n\n"
               "PHÒNG THI: ..........................................................")
    
    c2 = info_table.cell(0, 1)
    c2.width = Inches(1.5)
    set_cell_border(c2, top=dict(val="single", sz=6), bottom=dict(val="single", sz=6), left=dict(val="single", sz=6), right=dict(val="single", sz=6))
    set_cell_margins(c2, top=100, bottom=100, left=80, right=80)
    p2 = c2.paragraphs[0]
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p2.add_run("CÁN BỘ COI THI")
    r.font.bold = True
    
    c3 = info_table.cell(0, 2)
    c3.width = Inches(1.5)
    set_cell_border(c3, top=dict(val="single", sz=6), bottom=dict(val="single", sz=6), left=dict(val="single", sz=6), right=dict(val="single", sz=6))
    set_cell_margins(c3, top=100, bottom=100, left=80, right=80)
    p3 = c3.paragraphs[0]
    p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p3.add_run("ĐIỂM SỐ")
    r.font.bold = True
    
    doc.add_paragraph().paragraph_format.space_after = Pt(14)
    
    # Câu 1b Box
    q1_table = doc.add_table(rows=1, cols=1)
    q1_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_q1 = q1_table.cell(0, 0)
    c_q1.width = Inches(6.6)
    set_cell_border(c_q1, top=dict(val="single", sz=6), bottom=dict(val="single", sz=6), left=dict(val="single", sz=6), right=dict(val="single", sz=6))
    set_cell_margins(c_q1, 80, 80, 120, 120)
    p_q1 = c_q1.paragraphs[0]
    p_q1.paragraph_format.space_after = Pt(0)
    r = p_q1.add_run("(1.25 điểm) Sắp xếp các hàm theo thứ tự tăng dần của “Big-O nhỏ nhất”. Phân lớp các hàm bên dưới vào các “Big-O nhỏ nhất”, có giải thích ngắn gọn cách xác định:")
    r.font.size = Pt(11.5)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(10)
    
    # Big-O Table (4 columns)
    bigo_table = doc.add_table(rows=4, cols=4)
    bigo_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx in range(4):
        for c_idx in range(4):
            cell = bigo_table.cell(r_idx, c_idx)
            cell.width = Inches(1.65)
            set_cell_border(cell, top=dict(val="single", sz=6), bottom=dict(val="single", sz=6), left=dict(val="single", sz=6), right=dict(val="single", sz=6))
            set_cell_margins(cell, 100, 100, 80, 80)
            if r_idx == 0 and c_idx == 0:
                p_bo = cell.paragraphs[0]
                p_bo.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_bo.add_run("= === O")
            else:
                p_bo = cell.paragraphs[0]
                p_bo.paragraph_format.space_before = Pt(16)
                
    # --- PAGE 2 ---
    doc.add_page_break()
    
    # Code frame for Question 2
    code_box = doc.add_table(rows=1, cols=1)
    code_box.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_cb = code_box.cell(0, 0)
    c_cb.width = Inches(6.6)
    set_cell_border(c_cb, top=dict(val="single", sz=6), bottom=dict(val="single", sz=6), left=dict(val="single", sz=6), right=dict(val="single", sz=6))
    set_cell_margins(c_cb, 100, 100, 120, 120)
    p_cb = c_cb.paragraphs[0]
    p_cb.paragraph_format.space_after = Pt(0)
    r_code = p_cb.add_run(
        "Algorithm func(a, n)\n"
        "1.  s = 0\n"
        "2.  for i = 1 to n do\n"
        "3.      for j = i to n do\n"
        "4.          s = s + a[i, j]\n"
        "5.  return s"
    )
    r_code.font.name = "Courier New"
    r_code.font.size = Pt(10.5)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(10)
    
    p_q2_1 = doc.add_paragraph()
    p_q2_1.paragraph_format.space_after = Pt(4)
    p_q2_1.add_run("Lời gọi hàm func (a,n) sẽ trả về (hay in ra màn hình) kết quả là thông tin gì?")
    
    add_underline_lines(doc, num_lines=3, space_after=18)
    
    p_q2_2 = doc.add_paragraph()
    p_q2_2.paragraph_format.space_after = Pt(4)
    p_q2_2.add_run("Hãy đếm.... Trình bày cách suy ra công thức theo n, từ đó suy ra độ phức tạp tính toán của giải thuật.")
    
    add_underline_lines(doc, num_lines=8, space_after=20)
    
    # --- PAGE 3 ---
    doc.add_page_break()
    
    p_c_title = doc.add_paragraph()
    p_c_title.paragraph_format.space_after = Pt(4)
    r_c = p_c_title.add_run("c. (1.5 điểm)")
    r_c.font.bold = True
    
    # Equation 3 columns table
    eq_table = doc.add_table(rows=2, cols=3)
    eq_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Phương trình 1", "Phương trình 2", "Phương trình 3"]
    for i, h in enumerate(headers):
        cell_h = eq_table.cell(0, i)
        cell_h.width = Inches(2.2)
        set_cell_border(cell_h, top=dict(val="single", sz=6), bottom=dict(val="single", sz=6), left=dict(val="single", sz=6), right=dict(val="single", sz=6))
        set_cell_margins(cell_h, 80, 80, 80, 80)
        p = cell_h.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.bold = True
        
        cell_b = eq_table.cell(1, i)
        cell_b.width = Inches(2.2)
        set_cell_border(cell_b, top=dict(val="single", sz=6), bottom=dict(val="single", sz=6), left=dict(val="single", sz=6), right=dict(val="single", sz=6))
        set_cell_margins(cell_b, 80, 80, 80, 80)
        p_b = cell_b.paragraphs[0]
        p_b.paragraph_format.space_after = Pt(0)
        if i == 0:
            p_b.add_run("T(n) = 2T(n/2) + n\n(Phương pháp thế)")
        elif i == 1:
            p_b.add_run("T(n) = 5T(n-1) - 6T(n-2)\n(Phương trình đặc trưng)")
        else:
            p_b.add_run("T(n) = T(n-1) + n\n(Hàm sinh / Truy hồi)")

    doc.add_paragraph().paragraph_format.space_after = Pt(10)
    add_underline_lines(doc, num_lines=4, space_after=18)
    
    # PHẦN 2: TỰ LUẬN (6 điểm)
    p_p2 = doc.add_paragraph()
    p_p2.paragraph_format.space_before = Pt(10)
    p_p2.paragraph_format.space_after = Pt(3)
    r = p_p2.add_run("PHẦN 2: TỰ LUẬN (6 điểm)")
    r.font.bold = True
    r.font.size = Pt(13)
    
    p_luuy = doc.add_paragraph()
    p_luuy.paragraph_format.space_after = Pt(2)
    r = p_luuy.add_run("Lưu ý về bài làm:")
    r.font.italic = True
    
    p_l1 = doc.add_paragraph()
    p_l1.paragraph_format.space_after = Pt(2)
    r = p_l1.add_run("- Trường hợp không xây dựng được thuật toán, sinh viên trình bày ý tưởng giải để được xem xét cho điểm.")
    r.font.italic = True
    
    p_l2 = doc.add_paragraph()
    p_l2.paragraph_format.space_after = Pt(4)
    r = p_l2.add_run("- Thuật toán cần được trình bày dưới dạng mã giả và có chú thích rõ ràng để người đọc dễ hiểu")
    r.font.italic = True
    
    p_q3 = doc.add_paragraph()
    p_q3.paragraph_format.space_before = Pt(4)
    p_q3.paragraph_format.space_after = Pt(4)
    r1 = p_q3.add_run("Câu 3 (2 điểm) Phân tích bài toán. ")
    r1.font.bold = True
    r2 = p_q3.add_run("Sinh viên chọn làm 1 trong 2 bài toán sau")
    
    add_underline_lines(doc, num_lines=4, space_after=18)
    
    # --- PAGES 4 to 9 ---
    for pg in range(4, 10):
        doc.add_page_break()
        p_pg_header = doc.add_paragraph()
        p_pg_header.paragraph_format.space_after = Pt(8)
        if pg == 4:
            r = p_pg_header.add_run("Câu 4 (2 điểm) Thiết kế thuật toán (Trình bày Mã giả & Đánh giá độ phức tạp):")
            r.font.bold = True
        elif pg == 5:
            r = p_pg_header.add_run("Câu 5 (2 điểm) Thiết kế thuật toán Quy hoạch động (Dynamic Programming - MCM / Tổ hợp):")
            r.font.bold = True
        elif pg in [6, 7]:
            r = p_pg_header.add_run("Phần tiếp theo bài làm của sinh viên:")
            r.font.italic = True
        else: # 8, 9
            r = p_pg_header.add_run("TRANG GIẤY DỰ PHÒNG (Dành cho sinh viên làm lại bài khi bị hủy / sai sót ở các phần trên):")
            r.font.bold = True
            r.font.italic = True
            r.font.color.rgb = RGBColor(100, 100, 100)
            
        add_underline_lines(doc, num_lines=16, space_after=22)

    target_path = "/Users/thangdo/www/thuong-cho-tam-than-co-han/bai_tap/Đề thi mẫu/CS112.DE_THI_CK.HK3.2025-2026.docx"
    doc.save(target_path)
    print(f"✓ Saved exact DOCX to {target_path}")

if __name__ == "__main__":
    build_exact_docx()
