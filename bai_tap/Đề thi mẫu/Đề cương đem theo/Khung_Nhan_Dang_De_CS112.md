# Khung nhận dạng đề CS112 (bản 2, đã đối chiếu nguồn)

Cách dùng: đọc đề, gạch chân **cụm từ yêu cầu**, tra bảng để ra dạng bài, rồi làm theo sườn.
Nhận dạng theo câu chữ trong đề, không theo số thứ tự câu, vì bố cục đề đổi giữa các kỳ.

Ký hiệu dẫn chứng: `b9:61` là `data/buoi9_clean.md` dòng 61 (transcript buổi 9).

Kiểm lại khung sau khi sửa: từ gốc repo chạy `.venv/bin/python "bai_tap/Đề thi mẫu/Đề cương đem theo/verify_khung.py" "bai_tap/Đề thi mẫu/Đề cương đem theo/Khung_Nhan_Dang_De_CS112.md" .` (exit 0 là mọi check qua).

## 0. Nguồn và mức tin cậy

| Nguồn | Tin cậy | Ghi chú |
|---|---|---|
| Đề thật HK1 2025-2026 (`bai_tap/Đề thi mẫu/2025/DethiCK...pdf`) | Cao | Đề thật duy nhất có nội dung đầy đủ |
| Lời cô mô tả cấu trúc đề kỳ này (b9:3-61) | Cao, nhưng còn "dự kiến" | b9:31, b9:51 ("Đề thì chưa có này chỉ là cấu trúc") |
| Ghi chú của cô trong HW02 (ảnh trang 23-25) | Cao | Bài 6 và 7 "thi có thể hỏi", Bài 8 "câu này từng thi" |
| File `CS112.DE_THI_CK.HK3.2025-2026.*` | Trung bình | Do script `scratch/build_exact_exam_docx.py` dựng lại. Nhãn "Câu 5 = QHĐ" là suy đoán của script |
| 3 đề mẫu trong `Đề mẫu/` | Thấp | AI soạn, chỉ dùng để luyện tay |
| `mock_exam_pttktt.md` | Thấp | AI soạn. Có câu bắt dùng định lý Thợ (Master), trái với lời cô là không thi (b9:61) |
| `Ôn Luyện/De_Thi_Mau_2025_Loi_Giai_Chi_Tiet.*` và `Ôn Luyện/Cau1_Ky_Hieu_Tiem_Can_...*` (cả .md, .docx, .pdf) | Đã sửa Câu 1b ngày 27/9 | Bản cũ chép nhầm f₁ và f₅ của đề HK1 nên ra thứ tự sai. Đã sửa theo đề gốc, có ô "Đính chính" trong file. Các câu còn lại của file lời giải HK1 (1a, 2, 3, 4, 5, 6b) mình đã soát, khớp đáp án. Câu 3b có thêm ô "Lưu ý" về trường hợp số âm |

**Không thi:** định lý Master (b9:61) và thuật toán Fourier-Motzkin, transcript ghi là "for maskin" (b9:63) và "for moskin" (b6:13), tức thuật toán khử dần từng biến trong hệ bất phương trình dạy ở buổi 6 (b6:11-27). Còn lại "đọc nhiêu là thi nhiêu" (b9:61).

## 1. Mẹo chung trong phòng thi (có căn cứ)

- Chỉ 1 tờ A4 viết tay (b9:1), dùng cả 2 mặt (b9:3).
- Đề ghi 12 điểm, thực tế chấm tới 14-15 điểm. Ý nào không biết thì bỏ qua (b9:15, b9:49). Cô nói làm tốt khoảng nửa đề là có thể được 9-10 (b9:57).
- Khi nói về phần tự luận, cô nói câu đang chiếu được chia nhiều ý, "mấy cái câu C này là câu bonus", làm tốt 2 ý trên đã đủ điểm câu đó (b9:53-55). Transcript không cho biết đó là câu nào, nên đừng mặc định ý c ở mọi câu đều là bonus.
- Làm bài trên đề, chỗ trống ít: nháp ra ngoài rồi mới viết vào (b9:35). Thiếu chỗ thì kẻ đôi trang, viết 2 cột (b9:29).
- Không viết được mã giả thì viết ý tưởng, vẫn có điểm (b9:39). Không vẽ lưu đồ (b9:41).
- Đề mô tả mơ hồ thì ghi rõ giả định của mình rồi làm tiếp (b9:45).
- Phần đệ quy năm nào cũng có, phần không đệ quy lúc có lúc không (b1:499).
- Quay lui và QHĐ lúc nào cũng có (b7:153, b7:493, b9:67). Tham lam có thi (b9:441). Cuối buổi 9 cô nói tham lam cần nói lại một chút, và có thể mở bài WeCode tham lam kiểu "phân công việc", "tô màu đồ thị" giống môn Trí tuệ nhân tạo (b9:461).

## 2. Phần phân tích

### 2.1 Tiệm cận

| Cụm từ trong đề | Dạng | Sườn |
|---|---|---|
| "Dùng định nghĩa ... chứng minh", "using the definitions", "true or false", "đúng hay sai", "đúng/sai" + hàm cụ thể | A1. f cụ thể ∈ O/Ω/Θ | Chép định nghĩa đủ ∃c>0, ∃n₀, ∀n≥n₀. Chặn, chọn c và n₀ cụ thể, kết luận "theo định nghĩa của Big O ta có điều cần chứng minh" (cách cô trình bày ở b4:213-215) |
| "Nếu ... ∈ ... thì ...", "If ... ∈ ... then", "⟺" | A2. Tính chất tổng quát | Viết giả thiết thành (c₁, n₁), (c₂, n₂). Hai giả thiết độc lập nên hằng số phải khác tên, dùng chung một chữ c là sai (b4:413). Nối bất đẳng thức, lấy n₀ = max(n₁, n₂). Bắc cầu hoặc tích thì c = c₁c₂. Tổng T₁ + T₂ ∈ O(max(f, g)) thì c = c₁ + c₂, vì f và g đều ≤ max(f, g) (cô chữa ở b4:417-429, dạng này "đã từng xuất hiện rất nhiều lần", b4:407). Chiều ⟺ dùng 1/c |
| "O(f(n)) = O(g(n))" | A3. Hai tập bằng nhau (đã ra ở HK1) | Chứng minh 2 chiều ⊆. Mỗi chiều: "xét h **bất kỳ** ∈ O(f)" rồi suy ra h ∈ O(g) |
| "∉", "phản chứng" | A4. Chứng minh sai | Giả sử có c, n₀. Biến đổi về "biểu thức theo n ≤ c". Vế trái không bị chặn nên mâu thuẫn |
| "Prove ... or disprove", "counterexample", "chứng minh hoặc bác bỏ", "phản ví dụ" | A5. Mệnh đề tổng quát có thể sai (HW02 Bài 3, 4) | Thử trước vài cặp hàm quen (n, n², 2ⁿ, hàm dao động). Nếu sai thì đưa **phản ví dụ cụ thể**. Vd "với mọi t, g thì t ∈ O(g) hoặc t ∈ Ω(g)" sai với t = n, g = n^(1+sin n) |
| "Phân lớp ... Big-O nhỏ nhất ... sắp xếp", "Sắp xếp các hàm", "phân lớp (group)", "độ phức tạp tăng dần", "order of growth", "indicate the class", "simplest g(n)", "Θ(g(n)) đơn giản nhất" | B. Phân lớp | Xem 2.1.B |
| "largest size n ... solved in time t", "kích thước lớn nhất ... trong thời gian" | C. Bảng thời gian chạy (HW02 Bài 6) | Giải f(n) ≤ t (đổi ra µs) tìm n lớn nhất |
| "O, o, Ω, ω, Θ ... yes/no", "O, o, Ω, ω, or Θ", "yes or no" | D. Bảng quan hệ (HW02 Bài 7) | Xem 2.1.D |
| "Hypothesize ... efficiency class", "empirical", "đoán lớp hiệu quả" | E. Đoán lớp từ số liệu (HW02 Bài 8, từng thi) | Xem 2.1.E |

**A. Bẫy hạng tử âm.** Chặn trên thì bỏ hạng tử âm ở vế f. Nếu hạng tử âm nằm ở vế bị so sánh (vd g = n² − 80n) thì chọn c lớn hơn hệ số, chuyển vế, xét dấu để tìm n₀. Ví dụ cô chữa: 7n² ≤ 8(n² − 80n) ⟺ n ≥ 640, chọn c = 8, n₀ = 640 (b4:223-231).

**A. Về lim.** Đề HK1 chỉ ghi "Dùng định nghĩa". Bản dựng HK3 có ghi "không dùng định lý, không dùng lim", nhưng file đó do script dựng lại, không phải đề thật. Không tìm thấy câu cô cấm lim trong 9 buổi. Cách an toàn: câu chứng minh thì luôn đưa ra c và n₀ cụ thể. Ở câu phân lớp, lim là công cụ cô có dạy (b5:103-111).

**B. Phân lớp.** Chiến lược cô dạy khi đề có nhiều hàm (b4:317-349):
1. Tách nhóm nhỏ (đa thức trở xuống) và nhóm lớn (hàm mũ trở lên) trước (b4:321).
2. Trong nhóm lớn, đổi hết về cùng một cơ số rồi so số mũ (b4:339). Vd n = 3^(log₃ n).
3. Cơ số của log không quan trọng, log₂, log₃ cùng một lớp (b4:345).
4. Giải thích từng hàm. Chỉ ghi thứ tự mà sai là không có điểm, có lập luận đúng thì vẫn được điểm phần đó (b4:325).

Sau đó đưa mỗi hàm về dạng chuẩn, gộp hàm cùng lớp, xếp theo chuỗi
1 ≺ lg lg n ≺ lg n ≺ lgᵏ n ≺ n^ε ≺ n ≺ n lg n ≺ nᵏ ≺ aⁿ ≺ n! ≺ nⁿ.

| Gặp | Biến đổi |
|---|---|
| Tổng nhiều hạng tử | Giữ hạng tử lớn nhất, bỏ hệ số (b4:327). Vd 0.001n⁴ + 3n³ + 1 = Θ(n⁴) |
| a^(n+k), a^(n−k) | = aᵏ·aⁿ, cùng lớp với aⁿ. Vd 2^(n+1) + 3^(n−1) = Θ(3ⁿ) |
| lg(xᵏ) | = k·lg x. Vd lg((n+100)¹⁰) = 10·lg(n+100) = Θ(lg n) |
| a^(log_b n) | = n^(log_b a). Vd 4^(lg n) = n², 3^(lg n) = n^1.585. Đọc kỹ: "4 log n" (nhân) khác "4^(log n)" (mũ) |
| 2^(k·lg n) | = nᵏ |
| n^(c·lgᵏn) | = 2^(c·lg^(k+1) n). Lớn hơn mọi đa thức nhưng nhỏ hơn a^(√n) |
| lg(nⁿ), lg(n!) | Θ(n lg n) |
| Σi, Σi², ΣΣ i·j | n(n+1)/2, n(n+1)(2n+1)/6, [n(n+1)/2]², tức Θ(n²), Θ(n³), Θ(n⁴) |
| √(aᵇ), 3^(n/2) | a^(b/2), (√3)ⁿ ≈ 1.73ⁿ nhỏ hơn 2ⁿ. Hai hàm mũ khác cơ số thì khác lớp |
| Khó so (n^(lg n), n^√n với aⁿ) | Lấy lg hai vế rồi so: lg²n, √n·lg n với n |

**Hàm hóc hay gặp** (HW02 Bài 1 nhóm 2, tức CLRS 3-3): n^(1/lg n) = 2 nên Θ(1). (√2)^(lg n) = √n. 2^(lg n) = n, 4^(lg n) = n². n^(lg lg n) = (lg n)^(lg n). lg* n là số lần lấy lg tới khi ≤ 1, tăng cực chậm, lg*(lg n) = lg* n − 1. 2^(√(2 lg n)) lớn hơn mọi lgᵏn nhưng nhỏ hơn mọi n^ε. (lg n)! lớn hơn mọi đa thức nhưng nhỏ hơn n^(lg lg n).

Đề viết mơ hồ như "5 lg(n+100)^10" thì ghi rõ mình đọc theo cách nào (b9:45): 5·lg((n+100)¹⁰) = Θ(lg n), hoặc 5·(lg(n+100))¹⁰ = Θ(lg¹⁰ n). Cách nào cũng nhỏ hơn ∛n.

Bẫy: **đừng thế số để so**, cô nói cách này không có độ tin cậy (b4:319). Vd n·lg⁴n nhỏ hơn n^(4/3) về tiệm cận, nhưng chỉ thật sự nhỏ hơn khi n > khoảng 3·10²². Tương tự, 50·lg n còn lớn hơn ln²n cho tới n ≈ 2^104. Dùng quy tắc lgᵏn ≺ n^ε với mọi ε > 0.
Cô dặn: hàm dễ thì ghi thẳng lớp, hàm khó thì ghi bước biến đổi (b9:21). Nhớ viết dòng **kết luận thứ tự**, SV hay sót (b9:23).

**C. Hàng "1 giây" để tự kiểm** (t = 10⁶ µs): lg n: 2^(10⁶), √n: 10¹², n: 10⁶, n lg n: 62746, n²: 1000, n³: 100, 2ⁿ: 19, n!: 9.

**D. Định nghĩa cần chép** (CLRS, tài liệu [2] của cô):
- f ∈ o(g) ⟺ ∀c>0, ∃n₀, ∀n≥n₀: 0 ≤ f(n) < c·g(n).
- f ∈ ω(g) ⟺ ∀c>0, ∃n₀, ∀n≥n₀: 0 ≤ c·g(n) < f(n).
- Mẹo điền: A = Θ(B) thì O, Ω, Θ là yes, o, ω là no. A = o(B) thì chỉ O, o là yes. A = ω(B) thì chỉ Ω, ω là yes. Hàm dao động như n^(sin n) (sin n chạy giữa −1 và 1) thì không so sánh được, cả 5 ô là no.
- Đáp án 6 cặp của CLRS 3-2 (thứ tự O, o, Ω, ω, Θ). a: yes yes no no no. b: yes yes no no no. c: cả 5 no. d: no no yes yes no. e và f: yes no yes no yes. Mình kiểm bằng code 2 cặp e (n^(lg c) = c^(lg n)) và f (lg(n!) và lg(nⁿ) cùng Θ(n lg n)).

**E. Đoán lớp từ số liệu.** Tính count/n, count/(n lg n), count/n². Tỉ số nào gần hằng số thì lấy lớp đó. Hoặc xem tỉ số khi n nhân đôi: khoảng 2 là n, hơi trên 2 là n lg n, khoảng 4 là n². Với số liệu HW02 Bài 8, count/(n lg n) ≈ 1.0-1.2 gần như không đổi, nên khớp n lg n.

### 2.2 Phân tích thuật toán

| Cụm từ trong đề | Làm gì |
|---|---|
| Thuật toán không đệ quy (khung 5 bước của Levitin, b1:187-195) | 1. Kích thước input. 2. Phép toán cơ bản. 3. Xét tốt/xấu/trung bình nếu phụ thuộc dữ liệu (cô thường bỏ bước này, b1:191). 4. Lập tổng Σ. 5. Rút gọn ra công thức và bậc |
| "trả về ... thông tin gì", "trả về (hay in ra màn hình)", "chức năng", "What does ... compute" | Chạy tay với n = 3 hoặc 4. Nói cụ thể, vd "số cặp i<j có a[i] = a[j]", không viết chung chung "duyệt mảng" |
| Nhiều đoạn code | Nối tiếp nhau: quy tắc cộng, lấy max. Lồng nhau: quy tắc nhân (b5:127-157) |
| "Đếm số phép", "Hãy đếm", "basic operation", "how many times", "Xây dựng công thức", "công thức tính độ phức tạp" | Mỗi vòng lặp là một Σ, cận lấy đúng theo code, rút gọn, thử lại với n = 2, 3. Nói ra cách đếm (b9:25) |
| Đếm phép so sánh trong vòng lặp | Cách cô đếm: vòng for chạy n lần có n+1 lần so sánh điều kiện (b1:211, b1:223). Nếu đề chỉ hỏi bậc thì không cần chính xác (b5:153-155) |
| "Thành lập phương trình đệ quy", "Thiết lập phương trình", "phương trình truy hồi", "hệ thức truy hồi", "recurrence relation", "Set up a recurrence" | T(cơ sở) = số phép ở nhánh dừng. T(n) = (số bài toán con) × T(kích thước con) + chi phí khác. Chi phí khác gồm chi phí phân chia (trước lời gọi) và chi phí tổng hợp (sau lời gọi) (b2:111, b2:185-187). Mỗi số hạng kèm 1 câu giải thích (b3:131). Nếu đề ghi "đếm chính xác, không dùng hằng số c1, c2" (như HK1 Câu 2a) thì chi phí khác phải là con số cụ thể, vd "+1" cho 1 lần transfer |
| "Sử dụng 02 phương pháp ... để giải", "bằng 2 phương pháp" | 1 phương trình giải bằng 2 cách chỉ định (đã ra ở HK1: Truy hồi và Hàm sinh) |
| "chọn giải 01 trong 03" | Dạng dự kiến kỳ này, mỗi phương trình chỉ định sẵn phương pháp (b9:31-33) |
| "trường hợp xấu nhất / tốt nhất" | Chỉ phân tích theo trường hợp khi đề hỏi. Cô thường bỏ bước này (b1:191) |
| "Compute the following sums", "Tính các tổng", "sums" | Dùng mục "Tổng cần nhớ" ngay dưới. Nếu hỏi bậc của tổng thì tính ra công thức rồi phân lớp như 2.1.B |

Phân biệt 2 chữ "truy hồi": "phương trình truy hồi", "hệ thức truy hồi" là chính phương trình đệ quy, đề bảo **thành lập** nó (b2:177). Còn "phương pháp truy hồi", "giải bằng truy hồi" là cách **giải** bằng thế ngược (b3:53).

**Tổng cần nhớ** (chủ đề có trong slide "Những công thức đáng nhớ", HW02 trang 3-8, công thức dưới đây mình kiểm bằng code): cấp số cộng Σ_{i=1}^{n} i = n(n+1)/2. Cấp số nhân Σ_{i=0}^{k} aⁱ = (a^(k+1) − 1)/(a − 1). Đổi cận Σ_{i=l}^{u} 1 = u − l + 1. Tổng lồng thì tính từ trong ra. Σ 1/(i(i+1)) = n/(n+1) (tách thành 1/i − 1/(i+1)).

**Chọn phương pháp giải phương trình đệ quy**

Đề thường ghi sẵn tên phương pháp. Gặp tên nào thì làm theo hàng tương ứng ở bảng sau:

| Cụm từ trong đề | Làm theo hàng |
|---|---|
| "Giải bằng Truy hồi", "phương pháp truy hồi", "Truy hồi (Backward Substitution)", "thế ngược", "Backward Substitution" | Truy hồi (thế ngược) |
| "Phương trình đặc trưng", "characteristic equation" | Phương trình đặc trưng |
| "Hàm sinh", "Generating Function" | Hàm sinh |
| "Đoán nghiệm", "substitution method", "guess" | Đoán nghiệm + quy nạp |
| "Giải phương trình", "Giải hệ thức", "kết luận độ phức tạp" (không ghi phương pháp) | Tự chọn theo cột "Dạng" ở bảng dưới, rồi thử lại với n = 1, 2 |
| "định lý Thợ", "Master Theorem" | Master: theo lời cô không thi (b9:61). Đề thật mà vẫn hỏi thì giải bằng truy hồi và ghi chú lý do |

| Dạng | Phương pháp | Sườn |
|---|---|---|
| Vế phải có 1 số hạng T, vd T(n) = aT(n−1) + f(n), T(n) = aT(n/b) + f(n) | Truy hồi (thế ngược) | Thế 3 lần, tìm dạng tổng quát ở bước k, cho n−k = cơ sở (hoặc n = 2ᵏ, n = 3ᵏ tùy phép chia), tính Σ. Không dùng được khi vế phải có nhiều T (b3:53). Vd T(n) = 4T(n/3) + n, T(1) = 1, đặt n = 3ᵏ ra T = 4·4ᵏ − 3·3ᵏ, tức Θ(n^(log₃ 4)) (HW02 Bài 9) |
| Nhiều số hạng T(n−k) | Phương trình đặc trưng (b3:175) | Nghiệm đơn: A·r₁ⁿ + B·r₂ⁿ. Nghiệm kép: (A + Bn)·rⁿ. Vế phải khác 0: thêm nghiệm riêng, nếu trùng nghiệm đặc trưng bội m thì nhân thêm nᵐ. Giải hệ bằng điều kiện đầu. Vd T(n) = 4T(n−1) − 5T(n−2) + 2T(n−3), T(0), T(1), T(2) = 0, 1, 2: phương trình (r−1)²(r−2) = 0 có nghiệm kép r = 1 và r = 2. Giải hệ ra hệ số của 2ⁿ bằng 0, nên T(n) = n (HW02 Bài 9). Hệ số bằng 0 là bình thường, không phải giải sai |
| Đề chỉ định hàm sinh | Hàm sinh | Đặt G(x) = Σ Tₙxⁿ, nhân xⁿ, lấy tổng, rút G(x), tách phân thức. Dùng 1/(1−ax) = Σ aⁿxⁿ và 1/(1−x)² = Σ (n+1)xⁿ. Vd T(n) = 7T(n−1) − 12T(n−2), T(0) = 1, T(1) = 2 ra T(n) = 2·3ⁿ − 4ⁿ (HW02 Bài 9) |
| Đề chỉ định đoán nghiệm | Đoán nghiệm + quy nạp (b2:255-339) | Đoán dạng, vd T(n) ≤ an² + b. Bước cơ sở. Giả thiết quy nạp: T(k) ≤ f(k) với mọi k < n. Suy ra cho n. Chọn a, b ở cuối. Vd (HW02 Bài 9) T(n) = 3T(n/2) + n², cô gợi ý đoán an² + b: quy nạp cần a ≥ 4 và b ≤ 0, chọn a = 4, b = 0. T(n) = T(n/2) + T(n/4) + n, gợi ý O(n): đoán T(n) ≤ cn, cần c ≥ 4 |

Luôn thử lại nghiệm với n = 1, 2. Ví dụ tự chấm: Hà Nội T(1) = 1, T(n) = 2T(n−1) + 1 cho T(n) = 2ⁿ − 1. Bằng hàm sinh: G(x) = x/((1−x)(1−2x)) = 1/(1−2x) − 1/(1−x).

## 3. Phần thiết kế

### 3.1 Nhận dạng chiến lược

Trong đề thật duy nhất có trong repo, đa số câu ghi thẳng tên phương pháp (HK1: Câu 2b "Truy hồi và Hàm sinh", Câu 3 "Quy hoạch động", Câu 4 "Quay lui và Giảm để trị", Câu 6 "Tham lam"). Khi đó bỏ qua bảng dưới, làm theo sườn ở 3.2. Chỉ cần tự nhận dạng khi đề không ghi (HK1 Câu 5 Mã đi tuần) hoặc ở câu "phân tích bài toán" tự chọn.

| Cụm từ trong đề | Chiến lược | Bài cô đã dạy hoặc đã thi |
|---|---|---|
| "Phân tích bài toán", "Xác định rõ Input", "chưa cần viết mã giả" | Phân tích bài toán (chọn 1 trong 2) | Sườn "Phân tích bài toán, mô hình hóa" ở 3.2 |
| "Mô hình hóa bài toán", "thiết kế cấu trúc dữ liệu" | Mô hình hóa | Sườn "Phân tích bài toán, mô hình hóa" ở 3.2 (HK1 Câu 5, 6) |
| "Quay lui", "Backtracking", "liệt kê tất cả", "tìm tất cả", "tất cả các", "mọi cấu hình", "Điền ... sao cho", "có tồn tại ... hay không" | Quay lui. Hai dấu hiệu cô dạy (b7:31-41): (1) cần vét cạn, "có cái chữ tất cả tức là có nhu cầu vét cạn" (b7:33). (2) Lời giải là một bộ nhiều thành phần, xây dần từng bước, mỗi bước có vài lựa chọn và ràng buộc (điền từng ô, đi từng ô, chèn dấu từng vị trí) | Hoán vị, dãy nhị phân, tách chuỗi đối xứng, tất cả đường đi giữa 2 đỉnh của đồ thị (b6:297-359), cây khung nhỏ nhất bằng quay lui có lưu T_min (b7:43-149), Mã đi tuần (HK1). WeCode: khôi phục IP ("khôi phục tất cả các địa chỉ"), Sudoku ("điền ... sao cho"), dò mìn, tìm từ trong ô chữ ("có tồn tại ... hay không", đi qua ô kề, mỗi ô dùng 1 lần), tính điểm môn học ("liệt kê tất cả các bộ điểm") |
| "Quy hoạch động", "Dynamic Programming", "DP[i][j]", "điền bảng", "dãy con tăng", "dấu ngoặc", "chuỗi ma trận", "tổ hợp chập" | QHĐ | Fibonacci (b8:119), LIS (từng thi, b8:307), C(n,k) top-down và bottom-up (b9:177-199), đặt ngoặc +× (HK1), nhân chuỗi ma trận (b9:443) |
| "Tham lam", "Greedy", "có thể chia nhỏ", "được chia nhỏ (tách ra)", "lấy một phần xᵢ", "phân số" | Tham lam | Ba lô phân số (HK1 Câu 6). Cô có nhắc bài tham lam kiểu "phân công việc", "tô màu đồ thị" (b9:461), đề cụ thể chưa rõ |
| "Chia để trị", "Divide and Conquer", "chia đôi", từ 2 bài toán con trở lên (b7:401) | Chia để trị | MergeSort (b7:259-263), vạch thước (b8:47-67), sắp hạng các điểm trong mặt phẳng khi đề cấm brute force (đề thi cũ cô chữa: sort theo hoành độ, chia 2 tập, giải đệ quy từng tập, b7:299-401) |
| "Giảm để trị", "Decrease and Conquer", "bỏ bớt một phần tử", chỉ 1 bài toán con | Giảm để trị | Hoán vị bằng cách chèn phần tử mới vào mọi vị trí của các hoán vị cũ (b7:421-437, cách chèn ở b7:447-449). Phân biệt với chia để trị: b8:137 |
| "theo 02 cách ... so sánh", "dùng một cách giải khác" | 2 chiến lược | HK1 Câu 4, đề cũ ở b7:497 |
| "hàm mục tiêu", "ràng buộc", "phương án sản xuất", 2 biến | Tối ưu bằng hình học (b5:407-451) | Bài radio (số liệu ở b5:349-383): max 30x₁ + 20x₂ với x₁ ≤ 60, x₂ ≤ 75, 10x₁ + 8x₂ ≤ 800. Tối ưu tại giao điểm đường 1 và đường 3 (b5:451), mình tính ra (60, 25), lãi 2300 |

Ưu tiên thấp (không thấy trong transcript, chỉ có trong đề AI soạn): cặp điểm gần nhất, đoạn con tổng lớn nhất, N-Queens, cái túi 0/1 dạng QHĐ.

**Khi đề không ghi tên chiến lược** thì bảng cụm từ ở trên dễ hụt (đo trên câu hỏi đề cũ cô đọc trong transcript, khung chỉ bắt đúng khoảng một nửa). Khi đó dùng dấu hiệu của cô thay cho cụm từ:
- QHĐ: bài toán tối ưu (lớn nhất, nhỏ nhất, dài nhất, ít nhất), hoặc có công thức truy hồi như Fibonacci (b8:115-119). Giải bằng đệ quy thấy bài con bị giải lặp là dấu hiệu mạnh (b9:77-85). Đề thi QHĐ của cô hay cho trên mảng (b8:293).
- Quay lui: đề đòi tất cả các lời giải, hoặc lời giải xây từng bước mà mỗi bước phải thử nhiều lựa chọn (tìm đường đi, cây khung, cách chia chuỗi) (b7:31-41, b6:303-309, b7:43-149).
- Chia để trị: chia bài thành từ 2 bài con cùng dạng. Giảm để trị: chỉ còn 1 bài con (b8:137).
- Biến thể của bài đã học vẫn là QHĐ cùng khung. Vd đề cũ "dãy con dài nhất mà 2 phần tử liền kề hơn kém nhau 1 đơn vị" (b8:389-393): giữ nguyên LIS, đổi điều kiện a_j < a_i thành |a_i − a_j| = 1. Cô nói làm được câu này mới có cơ hội qua môn (b8:391).
Cẩn thận chữ "tất cả": dấu hiệu quay lui là đề đòi **tất cả các lời giải** (tất cả các cách chia, các địa chỉ, các hành trình). Còn "tính tất cả các giá trị DP[i][j]" (HK1 Câu 3) là điền bảng QHĐ, không phải quay lui. Đề đã ghi tên phương pháp thì theo tên đó.
Bẫy ba lô 0/1: tham lam theo đơn giá sai. Ví dụ M = 50, (w, p) = (10, 60), (20, 100), (30, 120): tham lam được 160, tối ưu là 220.

### 3.2 Sườn từng dạng

| Cụm từ yêu cầu trình bày | Làm theo sườn |
|---|---|
| "Xác định Input", "Input và Output", "Input / Output", "Minh họa ý tưởng" | Phân tích bài toán, mô hình hóa |
| "Mã giả", "Pseudo-code", "đánh số bước", "Space Complexity", "độ phức tạp ... không gian" | Mã giả và cấu trúc dữ liệu |
| "Bài toán cơ sở", "Base case", "Truy vết", "Traceback", "Bottom-Up", "Cấu trúc con tối ưu", "optimal substructure" | Mục tương ứng trong sườn QHĐ, khi câu thuộc bài QHĐ. "Bài toán cơ sở" và "bottom-up" cũng dùng cho giảm để trị (b7:417-437), nên xem đề đang hỏi chiến lược nào |

**Phân tích bài toán, mô hình hóa** (b5:265-267, b5:369, b5:397, b9:41-45)
1. Input (kiểu, kích thước), Output (chỉ giá trị hay cả nghiệm), ràng buộc, ví dụ.
2. Bài tối ưu: biến quyết định, hàm mục tiêu, thế nào là phương án chấp nhận được.
3. Nêu tên chiến lược kèm 1 câu lý do. Chưa cần mã giả nếu đề ghi vậy.
4. Minh họa từng bước trên ví dụ.

**Mã giả và cấu trúc dữ liệu** (b9:45-47, b7:105-111)
- Ghi tên chiến lược, đánh số bước.
- Mỗi biến hoặc mảng ghi kiểu, kích thước, ý nghĩa giá trị. Vd "B[1..m] là mảng nhị phân, B[k] = 1 nghĩa là cạnh k đã chọn".
- Độ phức tạp thời gian và không gian.

**Quay lui** (b6:157-209, b7:153-235)
- Mô hình 1: Try(i) chọn giá trị cho thành phần thứ i. Với mỗi ứng viên hợp lệ: ghi nhận, nếu đủ n thành phần thì xuất nghiệm, ngược lại gọi Try(i+1), cuối cùng hoàn tác.
- Mô hình 2: nghiệm là dãy nhị phân chọn hoặc không chọn. Vd tách chuỗi đối xứng: 1 nghĩa là cắt tại vị trí đó.
- Đọc kỹ đề hỏi "tất cả" (xuất rồi quay lui tiếp) hay "một" (thấy là dừng).
- Bài tối ưu giải bằng quay lui: giữ biến "lời giải tốt nhất hiện hành" (vd T_min). Mỗi khi có lời giải hoàn chỉnh thì so sánh và cập nhật. Đề không ghi "tất cả" thì chỉ cần một lời giải tối ưu (b7:137-149).
- Độ phức tạp: số nút cây trạng thái nhân chi phí mỗi nút.

**Hai cách cho cùng một bài** (HK1 Câu 4, hoán vị)
- Quay lui: thời gian O(n·n!), bộ nhớ O(n) không kể output.
- Giảm để trị (chèn aₙ vào mọi vị trí của các hoán vị n−1 phần tử): tổng công Σ k·k! = (n+1)! − 1, tức Θ(n·n!), nhưng phải lưu hết các hoán vị nên bộ nhớ O(n·n!).

**Tham lam** (HK1 Câu 6)
1. Mô hình hóa: biến xᵢ, hàm mục tiêu, ràng buộc. Vd ba lô phân số: max Σ pᵢxᵢ với Σ wᵢxᵢ ≤ M, 0 ≤ xᵢ ≤ 1.
2. Tiêu chí chọn: vd đơn giá pᵢ/wᵢ giảm dần. Nói rõ vì sao chọn tiêu chí đó.
3. Mã giả: sắp xếp theo tiêu chí, duyệt, lấy trọn nếu còn chỗ, không đủ chỗ thì lấy một phần rồi dừng.
4. Độ phức tạp: O(n log n) do bước sắp xếp.
5. Chạy tay trên dữ liệu đề cho, ghi từng bước và sức chứa còn lại.

**Chia để trị và Giảm để trị** (b7:259-263, b7:401, b7:421-437, b8:47-67)
- Chia để trị: nếu bài đủ nhỏ thì giải trực tiếp. Ngược lại chia (thường chia đôi theo left, right), gọi đệ quy từ 2 bài con trở lên, rồi tổng hợp kết quả.
- Giảm để trị: bỏ bớt 1 phần tử (thường phần tử cuối vì mảng xử lý phần tử cuối dễ hơn, b7:431), giải bài con duy nhất, rồi mở rộng lời giải. Viết được bằng đệ quy top-down hoặc vòng lặp bottom-up (b7:417-421).
- Độ phức tạp: lập T(n) rồi giải bằng truy hồi.

**Tối ưu 2 biến bằng hình học** (b5:417-451, b6:7-11, b6:21)
1. Mỗi ràng buộc bỏ dấu ≤ thành = rồi vẽ đường thẳng, chọn nửa mặt phẳng đúng. Giao các nửa mặt phẳng được miền chấp nhận được.
2. Vẽ đường mức của hàm mục tiêu, tịnh tiến ra xa. Điểm cuối cùng còn chạm miền là nghiệm tối ưu (b5:441).
3. Giải hệ 2 phương trình của 2 đường thẳng qua điểm đó, thế vào hàm mục tiêu.
4. Cách này chủ yếu dùng khi có 2 biến (b6:21). Thuật toán Fourier-Motzkin cho nhiều biến thì không thi (b9:63).

**QHĐ** (b9:77-85, b9:177-199, b9:247, b9:317, b9:465)
1. Cấu trúc con tối ưu: lời giải tối ưu của bài cha chứa lời giải tối ưu của bài con.
2. Bài toán con trùng lặp (overlapping): vẽ cây đệ quy top-down, chỉ ra bài con bị giải lặp.
3. Bảng: kích thước, ý nghĩa mỗi ô.
4. Trường hợp cơ sở và phương trình QHĐ. Làm được phần này là được nhiều điểm (b9:317).
5. Thứ tự điền: bottom-up điền hết bảng. Top-down có ghi nhớ chỉ điền các ô cần tới, ô được ghi khi lời gọi đệ quy trả về (b9:195). Vd C(3,2) top-down điền lần lượt C(1,0), C(1,1), C(2,1), C(2,2), C(3,2).
6. Điền bảng tay trên ví dụ của đề, ghi phép tính của vài ô.
7. Truy vết: lưu k tốt nhất ở mỗi ô rồi lần ngược.

Bẫy đặt ngoặc +×: số không âm thì chỉ cần lưu max. Có số âm phải lưu cả min lẫn max. Ví dụ 2 × −1 × −3 + 3 × −4: max đúng là 30 = 2 × (−1 × (−3 + 3 × −4)), nhưng DP chỉ lưu max ra 0.

## 4. Đáp số đề thật HK1 để tự chấm (đã chạy kiểm bằng code)

- **Câu 1b:** f₁ < f₄ < f₂ < f₃ < f₅ < f₆ < f₇. Đề gốc là f₁ = 4·lg n + lg lg n = Θ(lg n) và f₅ = n^(5·lg²n) (xem ảnh đề), không phải 4^(lg n) và n⁵·lg²n. Các hàm còn lại: f₂ = n^(4/3), f₃ = Θ(n⁴), f₄ = n·lg⁴n, f₆ = 3^(√n/2), f₇ = √n·3^(n/2). Cô chữa ra đúng thứ tự này ở b4:317-349.
- **Câu 2:** T(1) = 1, T(n) = 2T(n−1) + 1. Nghiệm T(n) = 2ⁿ − 1, độ phức tạp Θ(2ⁿ).
- **Câu 3:** bảng DP. Hàng i = 0: 1, 3, 9, 21. Hàng 1: 2, 6, 14. Hàng 2: 3, 7. Hàng 3: 4. Giá trị lớn nhất 21 = (1+2) × (3+4).
  DP[1][3] = max(2 × (3+4), (2×3) + 4) = max(14, 10) = 14.
- **Câu 6b:** đơn giá p/w là 1.389, 1.6, 1.5, xếp theo thứ tự đồ 2, 3, 1. Lấy trọn đồ 2 (15 kg, giá trị 24), còn 5 kg lấy 1/2 đồ 3 (giá trị 7.5). Tổng 31.5.

## 5. Còn mở

- Buổi ôn hẹn tối thứ bảy 26/9 (b9:461). Lúc 01:04 ngày 27/9 giờ VN, playlist vẫn chỉ có 9 video. Khi có video buổi 10 thì cần đối chiếu: đề chính thức có ghi "không dùng lim" không, câu giải phương trình dạng nào, phần tham lam thi bài nào.
- Transcript chỉ có lời nói, không có màn hình đề cô chiếu ở buổi 9.
