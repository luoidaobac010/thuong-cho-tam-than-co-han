import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

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

def build_perfect_docx():
    doc = Document()
    
    # Page setup
    for s in doc.sections:
        s.top_margin = Inches(0.7)
        s.bottom_margin = Inches(0.7)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)
        
        # Footer
        footer = s.footer
        f_p = footer.paragraphs[0]
        f_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        f_run = f_p.add_run("Trang 1 / 10 – Đề")
        f_run.font.name = "Times New Roman"
        f_run.font.size = Pt(11)
        f_run.font.color.rgb = RGBColor(80, 80, 80)

    # Styles
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    font.color.rgb = RGBColor(0, 0, 0)
    
    # --- PAGE 1 ---
    h_table = doc.add_table(rows=1, cols=2)
    h_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    h_table.autofit = False
    
    c_left = h_table.cell(0, 0)
    c_left.width = Inches(3.2)
    p_l = c_left.paragraphs[0]
    p_l.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p_l.add_run("TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN\n")
    r1.font.bold = True
    r1.font.size = Pt(11.5)
    r2 = p_l.add_run("TRUNG TÂM PHÁT TRIỂN CNTT\n\n")
    r2.font.bold = True
    r2.font.underline = True
    r2.font.size = Pt(11.5)
    r3 = p_l.add_run("Đề")
    r3.font.bold = True
    r3.font.size = Pt(12)
    
    c_right = h_table.cell(0, 1)
    c_right.width = Inches(3.4)
    p_r = c_right.paragraphs[0]
    p_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_r1 = p_r.add_run("ĐỀ THI CUỐI HỌC KỲ III (2025-2026)\n")
    r_r1.font.bold = True
    r_r1.font.size = Pt(11.5)
    r_r2 = p_r.add_run("MÔN: CS112 - PHÂN TÍCH VÀ THIẾT KẾ THUẬT TOÁN\n")
    r_r2.font.bold = True
    r_r2.font.size = Pt(11)
    r_r3 = p_r.add_run("Thời gian: 90 phút")
    r_r3.font.italic = True
    r_r3.font.size = Pt(11)
    
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(2)
    p_sp.paragraph_format.space_after = Pt(2)
    
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(2)
    r_sub = p_sub.add_run("(Sinh viên chỉ được phép sử dụng 01 tờ giấy A4 viết tay)")
    r_sub.font.bold = True
    r_sub.font.italic = True
    r_sub.font.size = Pt(11)
    
    p_warn = doc.add_paragraph()
    p_warn.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_warn.paragraph_format.space_after = Pt(8)
    r_warn = p_warn.add_run("Bài làm có dấu hiệu gian lận như sao chép lẫn nhau, sử dụng công cụ AI, dùng điện thoại tra cứu, ... sẽ bị 0 điểm và hủy kết quả học phần")
    r_warn.font.bold = True
    r_warn.font.italic = True
    r_warn.font.size = Pt(10.5)
    r_warn.font.color.rgb = RGBColor(220, 38, 38)
    
    info_table = doc.add_table(rows=1, cols=3)
    info_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    info_table.autofit = False
    
    c1 = info_table.cell(0, 0)
    c1.width = Inches(3.6)
    set_cell_border(c1, top=dict(val="single", sz=6), bottom=dict(val="single", sz=6), left=dict(val="single", sz=6), right=dict(val="single", sz=6))
    set_cell_margins(c1, top=80, bottom=80, left=100, right=100)
    p1 = c1.paragraphs[0]
    p1.paragraph_format.space_after = Pt(2)
    p1.add_run("HỌ VÀ TÊN SV: ....................................................\n\n"
               "MSSV: .....................................................................\n\n"
               "STT: .......................................................................\n\n"
               "PHÒNG THI: ..........................................................")
    
    c2 = info_table.cell(0, 1)
    c2.width = Inches(1.5)
    set_cell_border(c2, top=dict(val="single", sz=6), bottom=dict(val="single", sz=6), left=dict(val="single", sz=6), right=dict(val="single", sz=6))
    set_cell_margins(c2, top=80, bottom=80, left=60, right=60)
    p2 = c2.paragraphs[0]
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p2.add_run("CÁN BỘ COI THI")
    r.font.bold = True
    r.font.size = Pt(11)
    
    c3 = info_table.cell(0, 2)
    c3.width = Inches(1.5)
    set_cell_border(c3, top=dict(val="single", sz=6), bottom=dict(val="single", sz=6), left=dict(val="single", sz=6), right=dict(val="single", sz=6))
    set_cell_margins(c3, top=80, bottom=80, left=60, right=60)
    p3 = c3.paragraphs[0]
    p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p3.add_run("ĐIỂM SỐ")
    r.font.bold = True
    r.font.size = Pt(11)
    
    p_luuy_h = doc.add_paragraph()
    p_luuy_h.paragraph_format.space_before = Pt(8)
    p_luuy_h.paragraph_format.space_after = Pt(2)
    r_lh = p_luuy_h.add_run("Lưu ý:")
    r_lh.font.bold = True
    r_lh.font.underline = True
    
    p_luuy1 = doc.add_paragraph()
    p_luuy1.paragraph_format.space_after = Pt(2)
    p_luuy1.add_run("-   Làm bài trên đề. Có 2 trang dự phòng. Nên ghi rõ “Tiếp Câu 2 ở trang dự phòng” để người chấm dễ theo dõi.")
    
    p_luuy2 = doc.add_paragraph()
    p_luuy2.paragraph_format.space_after = Pt(6)
    p_luuy2.add_run("-   Tổng điểm của tất cả câu hỏi trong đề là 12 điểm. Trường hợp Tổng điểm thi nhiều hơn 10 điểm thì điểm bài thi sẽ tính là 10 điểm.")
    
    # PHẦN 1
    p_p1 = doc.add_paragraph()
    p_p1.paragraph_format.space_before = Pt(8)
    p_p1.paragraph_format.space_after = Pt(4)
    r_p1 = p_p1.add_run("PHẦN 1: CÂU TRẢ LỜI NGẮN (6 điểm)")
    r_p1.font.bold = True
    r_p1.font.size = Pt(12)
    pPr = p_p1._p.get_or_add_pPr()
    pBdr = parse_xml(f'''
        <w:pBdr {nsdecls("w")}>
            <w:bottom w:val="single" w:sz="10" w:space="2" w:color="3B82F6"/>
        </w:pBdr>
    ''')
    pPr.append(pBdr)
    
    # Câu 1
    p_c1 = doc.add_paragraph()
    p_c1.paragraph_format.space_before = Pt(6)
    p_c1.paragraph_format.space_after = Pt(3)
    r_c1_t = p_c1.add_run("Câu 1 (3 điểm) Ký hiệu tiệm cận\n")
    r_c1_t.font.bold = True
    p_c1.add_run("a. (0.75 điểm) Hãy dùng định nghĩa của các ký hiệu tiệm cận (không dùng định lý, không dùng lim) để chứng minh các nhận định sau:")
    
    p_cm1 = doc.add_paragraph()
    p_cm1.paragraph_format.space_before = Pt(3)
    p_cm1.paragraph_format.space_after = Pt(2)
    p_cm1.add_run("    •   Chứng minh (0.75 điểm):")
    add_underline_lines(doc, num_lines=3, space_after=18)
    
    p_cm2 = doc.add_paragraph()
    p_cm2.paragraph_format.space_before = Pt(4)
    p_cm2.paragraph_format.space_after = Pt(2)
    p_cm2.add_run("    •   Chứng minh (1 điểm):")
    add_underline_lines(doc, num_lines=2, space_after=18)
    
    q1b_table = doc.add_table(rows=1, cols=1)
    q1b_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_q1b = q1b_table.cell(0, 0)
    c_q1b.width = Inches(6.6)
    set_cell_border(c_q1b, top=dict(val="single", sz=6), bottom=dict(val="single", sz=6), left=dict(val="single", sz=6), right=dict(val="single", sz=6))
    set_cell_margins(c_q1b, 80, 80, 100, 100)
    p_q1b = c_q1b.paragraphs[0]
    p_q1b.paragraph_format.space_after = Pt(0)
    p_q1b.add_run("(1.25 điểm) Sắp xếp các hàm theo thứ tự tăng dần của “Big-O nhỏ nhất”. Phân lớp các hàm bên dưới vào các “Big-O nhỏ nhất”, có giải thích ngắn gọn cách xác định:")
    
    # --- PAGE 2 ---
    doc.add_page_break()
    
    bo_table = doc.add_table(rows=5, cols=4)
    bo_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx in range(4):
        for c_idx in range(4):
            cell = bo_table.cell(r_idx, c_idx)
            cell.width = Inches(1.65)
            set_cell_border(cell, top=dict(val="single", sz=6), bottom=dict(val="single", sz=6), left=dict(val="single", sz=6), right=dict(val="single", sz=6))
            set_cell_margins(cell, 80, 80, 60, 60)
            if r_idx == 0 and c_idx == 1:
                p_c = cell.paragraphs[0]
                p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_c.add_run("= === O")
            else:
                p_c = cell.paragraphs[0]
                p_c.paragraph_format.space_before = Pt(16)
                
    cell_bot = bo_table.cell(4, 0)
    cell_bot.merge(bo_table.cell(4, 3))
    set_cell_border(cell_bot, top=dict(val="single", sz=6), bottom=dict(val="single", sz=6), left=dict(val="single", sz=6), right=dict(val="single", sz=6))
    set_cell_margins(cell_bot, 80, 80, 100, 100)
    p_bot = cell_bot.paragraphs[0]
    p_bot.add_run("Kết luận: Thứ tự các hàm (từ nhỏ đến lớn) là ....................................................................................................")

    # Câu 2 (3 điểm) Phân tích thuật toán
    p_c2 = doc.add_paragraph()
    p_c2.paragraph_format.space_before = Pt(12)
    p_c2.paragraph_format.space_after = Pt(3)
    r_c2 = p_c2.add_run("Câu 2 (3 điểm) Phân tích thuật toán\n")
    r_c2.font.bold = True
    p_c2.add_run("a. (0.75 điểm) Hãy phân tích độ phức tạp của giải thuật sau, bằng cách trả lời 02 câu hỏi bên dưới:")
    
    # 2a Empty Code Box (Exact to Cô Thương's screen)
    code_table = doc.add_table(rows=1, cols=1)
    code_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_cd = code_table.cell(0, 0)
    c_cd.width = Inches(6.6)
    set_cell_border(c_cd, top=dict(val="single", sz=6), bottom=dict(val="single", sz=6), left=dict(val="single", sz=6), right=dict(val="single", sz=6))
    set_cell_margins(c_cd, 120, 120, 100, 100)
    p_cd = c_cd.paragraphs[0]
    p_cd.paragraph_format.space_after = Pt(0)
    # Empty lines inside box
    for _ in range(4):
        p_cd.add_run("\n")
    
    p_q2_a1 = doc.add_paragraph()
    p_q2_a1.paragraph_format.space_before = Pt(8)
    p_q2_a1.paragraph_format.space_after = Pt(2)
    p_q2_a1.add_run("Lời gọi hàm func (a,n) sẽ trả về (hay in ra màn hình) kết quả là thông tin gì?")
    add_underline_lines(doc, num_lines=2, space_after=18)
    
    p_q2_a2 = doc.add_paragraph()
    p_q2_a2.paragraph_format.space_before = Pt(6)
    p_q2_a2.paragraph_format.space_after = Pt(2)
    p_q2_a2.add_run("Hãy đếm.... Trình bày cách suy ra công thức theo n, từ đó suy ra độ phức tạp tính toán của giải thuật.")
    add_underline_lines(doc, num_lines=3, space_after=18)

    # 2b (0.75 điểm)
    p_c2_b = doc.add_paragraph()
    p_c2_b.paragraph_format.space_before = Pt(8)
    p_c2_b.paragraph_format.space_after = Pt(3)
    p_c2_b.add_run("b. (0.75 điểm) Thành lập phương trình đệ quy (hay còn gọi là hệ thức truy hồi) của các giải thuật sau, kèm giải thích ngắn gọn cách thành lập.")
    
    code_table_b = doc.add_table(rows=1, cols=1)
    code_table_b.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_cd_b = code_table_b.cell(0, 0)
    c_cd_b.width = Inches(6.6)
    set_cell_border(c_cd_b, top=dict(val="single", sz=6), bottom=dict(val="single", sz=6), left=dict(val="single", sz=6), right=dict(val="single", sz=6))
    set_cell_margins(c_cd_b, 100, 100, 100, 100)
    p_cd_b = c_cd_b.paragraphs[0]
    p_cd_b.paragraph_format.space_after = Pt(0)
    r_cd_b = p_cd_b.add_run("Cho giải thuật\n....\n\n")
    r_cd_b.font.name = "Times New Roman"
    r_cd_b.font.size = Pt(11)
    
    add_underline_lines(doc, num_lines=2, space_after=18)

    # --- PAGE 3 ---
    doc.add_page_break()
    add_underline_lines(doc, num_lines=4, space_after=18)
    
    # 2c (1.5 điểm) - Empty table body (Exact to Cô Thương's screen)
    p_c_t = doc.add_paragraph()
    p_c_t.paragraph_format.space_before = Pt(6)
    p_c_t.paragraph_format.space_after = Pt(3)
    r_ct = p_c_t.add_run("c. (1.5 điểm)")
    r_ct.font.bold = True
    
    eq_t = doc.add_table(rows=2, cols=3)
    eq_t.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Phương trình 1", "Phương trình 2", "Phương trình 3"]
    for i, h in enumerate(headers):
        c_h = eq_t.cell(0, i)
        c_h.width = Inches(2.2)
        set_cell_border(c_h, top=dict(val="single", sz=6), bottom=dict(val="single", sz=6), left=dict(val="single", sz=6), right=dict(val="single", sz=6))
        set_cell_margins(c_h, 80, 80, 60, 60)
        p = c_h.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.bold = True
        
        # Empty row 2
        c_b = eq_t.cell(1, i)
        c_b.width = Inches(2.2)
        set_cell_border(c_b, top=dict(val="single", sz=6), bottom=dict(val="single", sz=6), left=dict(val="single", sz=6), right=dict(val="single", sz=6))
        set_cell_margins(c_b, 100, 100, 60, 60)
        p_b = c_b.paragraphs[0]
        p_b.paragraph_format.space_before = Pt(18)

    add_underline_lines(doc, num_lines=5, space_after=18)
    
    # PHẦN 2: TỰ LUẬN (6 điểm)
    p_p2 = doc.add_paragraph()
    p_p2.paragraph_format.space_before = Pt(12)
    p_p2.paragraph_format.space_after = Pt(3)
    r_p2 = p_p2.add_run("PHẦN 2: TỰ LUẬN (6 điểm)")
    r_p2.font.bold = True
    r_p2.font.size = Pt(12)
    pPr = p_p2._p.get_or_add_pPr()
    pBdr = parse_xml(f'''
        <w:pBdr {nsdecls("w")}>
            <w:bottom w:val="single" w:sz="10" w:space="2" w:color="3B82F6"/>
        </w:pBdr>
    ''')
    pPr.append(pBdr)
    
    p_luuy_tl = doc.add_paragraph()
    p_luuy_tl.paragraph_format.space_before = Pt(4)
    p_luuy_tl.paragraph_format.space_after = Pt(2)
    r_ltl = p_luuy_tl.add_run("Lưu ý về bài làm:")
    r_ltl.font.italic = True
    
    p_tl1 = doc.add_paragraph()
    p_tl1.paragraph_format.space_after = Pt(2)
    r = p_tl1.add_run("-   Trường hợp không xây dựng được thuật toán, sinh viên trình bày ý tưởng giải để được xem xét cho điểm.")
    r.font.italic = True
    
    p_tl2 = doc.add_paragraph()
    p_tl2.paragraph_format.space_after = Pt(4)
    r = p_tl2.add_run("-   Thuật toán cần được trình bày dưới dạng mã giả và có chú thích rõ ràng để người đọc dễ hiểu")
    r.font.italic = True
    
    p_c3_t = doc.add_paragraph()
    p_c3_t.paragraph_format.space_before = Pt(4)
    p_c3_t.paragraph_format.space_after = Pt(4)
    r1 = p_c3_t.add_run("Câu 3 (2 điểm) Phân tích bài toán. ")
    r1.font.bold = True
    r2 = p_c3_t.add_run("Sinh viên chọn làm 1 trong 2 bài toán sau")
    
    add_underline_lines(doc, num_lines=6, space_after=20)
    
    # --- PAGES 4 to 9 ---
    for pg in range(4, 10):
        doc.add_page_break()
        p_pg_header = doc.add_paragraph()
        p_pg_header.paragraph_format.space_after = Pt(6)
        if pg == 4:
            r = p_pg_header.add_run("Câu 4 (2 điểm) Thiết kế thuật toán (Trình bày Mã giả & Đánh giá độ phức tạp):")
            r.font.bold = True
        elif pg == 5:
            r = p_pg_header.add_run("Câu 5 (2 điểm) Thiết kế thuật toán Quy hoạch động (Dynamic Programming - MCM / Tổ hợp):")
            r.font.bold = True
        elif pg in [6, 7]:
            r = p_pg_header.add_run("Phần tiếp theo bài làm của sinh viên:")
            r.font.italic = True
        else:
            r = p_pg_header.add_run("TRANG GIẤY DỰ PHÒNG (Dành cho sinh viên làm lại bài khi bị hủy / sai sót ở các phần trên):")
            r.font.bold = True
            r.font.italic = True
            r.font.color.rgb = RGBColor(100, 100, 100)
            
        add_underline_lines(doc, num_lines=16, space_after=22)

    target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "bai_tap", "Đề thi mẫu", "CS112.DE_THI_CK.HK3.2025-2026.docx")
    doc.save(target_path)
    print(f"✓ Saved exact DOCX to {target_path}")

if __name__ == "__main__":
    build_perfect_docx()
