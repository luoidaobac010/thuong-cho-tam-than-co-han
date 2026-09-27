#!/usr/bin/env python3
"""Kiểm khung nhận dạng đề CS112 theo đúng cách dùng: đọc đề thật rồi tra khung.

Chạy: python3 verify_khung.py <khung.md> <repo_root>   (cần pymupdf để đọc PDF đề HK1)
Exit 0 khi mọi check PASS. Các dòng "G/H/I/J/K ..." in tỉ lệ định tuyến, chỉ để báo cáo.

A. Định dạng: bảng đủ cột, không em dash, đường dẫn repo tồn tại.
B. Mỗi tham chiếu b#:dòng trong khung có từ khóa khớp trong transcript.
C. Các con số chính trong khung được tính lại bằng code (không phải mọi con số).
D. Bài tập thật của cô (HW01 bài 1, 3, 5 và HW02 bài 1, 2, 3, 5, 9): khung có quy tắc cần dùng không (has),
   và đáp án tính bằng code. Các bài này đã được dùng để vá khung, nên không còn là held-out.
E. Câu chữ đề thật HK1 (PDF) và bản dựng HK3 đi qua bảng cụm từ của khung.
F, F2. 30 câu (3 đề mẫu AI soạn + HK1) tới đúng dạng kỳ vọng.
G, H, I, J. HW02, WeCode, mock_exam, sườn đề. Đã bị lộ vì khung được sửa sau khi xem kết quả.
K. Held-out sạch: câu hỏi đề thi cũ do cô đọc trong transcript. Nhãn gán trước, không sửa khung theo nhóm này.
P. Khớp nhầm họ chiến lược.
"""
import math, os, re, sys, unicodedata
from fractions import Fraction as Fr
from itertools import combinations
from functools import lru_cache

KHUNG, REPO = sys.argv[1], sys.argv[2]
raw = open(KHUNG, encoding="utf-8").read()
N = lambda s: unicodedata.normalize("NFC", s).lower()
K = N(raw)
results = []

def check(group, name, ok, detail=""):
    results.append((group, name, bool(ok), detail))

def has(*phrases):
    return all(N(p) in K for p in phrases)

# ---------------- A. định dạng ----------------
lines = raw.splitlines()
bad_tables = []
i = 0
while i < len(lines):
    if lines[i].startswith("|"):
        block = []
        while i < len(lines) and lines[i].startswith("|"):
            block.append(lines[i]); i += 1
        cols = {b.count("|") for b in block}
        if len(cols) != 1: bad_tables.append(block[0][:40])
    else:
        i += 1
check("A", "mọi bảng đủ cột", not bad_tables, str(bad_tables))
check("A", "không em dash/en dash", "—" not in raw and "–" not in raw)
for p in ["data/buoi9_clean.md", "scratch/build_exact_exam_docx.py",
          "bai_tap/Đề thi mẫu/2025/DethiCK.HK1.2025.2026 (TX.F31.CN2.TTNT).pdf",
          "bai_tap/Đề thi mẫu/Ôn Luyện/De_Thi_Mau_2025_Loi_Giai_Chi_Tiet.md",
          "bai_tap/Đề thi mẫu/Ôn Luyện/Cau1_Ky_Hieu_Tiem_Can_Va_Phan_Lop_Do_Phuc_Tap.md"]:
    check("A", f"tồn tại: {p[-45:]}", os.path.exists(os.path.join(REPO, p)))

# ---------------- B. tham chiếu transcript ----------------
T = {b: open(os.path.join(REPO, f"data/buoi{b}_clean.md"), encoding="utf-8").read().splitlines() for b in range(1, 10)}
REF_KW = {  # ref -> từ khóa phải xuất hiện trong khoảng dòng
 "b1:191": ["bước ba"], "b1:211": ["n + 1"], "b1:223": ["n + 1"], "b1:499": ["lúc có lúc không"],
 "b1:187-195": ["năm bước"],
 "b2:111": ["phân hoạch"], "b2:185-187": ["chi phí tổng hợp"], "b2:255-339": ["quy nạp"],
 "b3:53": ["truy hồi"], "b3:131": ["transfer"], "b3:175": ["phương trình đặc trưng"],
 "b4:213-215": ["định nghĩa của B"], "b4:223-231": ["640"], "b4:317-349": ["nhóm nhỏ"],
 "b4:407": ["rất nhiều lần"], "b4:413": ["ký hiệu khác"], "b4:417-429": ["k = c + d"],
 "b7:299-401": ["lấy đề thi ra giải", "không dùng phương pháp root for", "sort ban đầu", "tập hợp s1"],
 "b9:63": ["for maskin"], "b6:13": ["for moskin"],
 "b9:1": ["viết tay"], "b7:447-449": ["chèn", "vị trí"],
 "b4:319": ["thế n"], "b4:321": ["nhóm hàm nhỏ"], "b4:325": ["không có điểm"], "b4:327": ["giữ lại"], "b4:339": ["cơ số"], "b4:345": ["cơ số 2"],
 "b5:103-111": ["giới hạn"], "b5:127-157": ["quy tắc cộng", "quy tắc nhân"], "b5:153-155": ["không cần đếm chính xác"], "b5:265-267": ["input"], "b5:349-383": ["radio"],
 "b5:417-451": ["đường thẳng"], "b6:7-11": ["nửa mặt phẳng", "miền chấp nhận được"], "b7:401": ["hai bài toán con trở lên"], "b9:53-55": ["câu c"],
 "b4:327": ["giữ lại"], "b5:441": ["nghiệm tối ưu"], "b6:21": ["hai biến"], "b7:259-263": ["sort"], "b7:431": ["bỏ thằng cuối"],
 "b7:417-421": ["bottom up"], "b7:33": ["tất cả tức là có nhu cầu vét cạn"], "b2:177": ["hệ thức tri hồi"], "b7:417-437": ["bottom up", "bài toán cơ sở"], "b8:115-119": ["tối ưu", "fibonacci"], "b8:293": ["mãng"], "b6:303-309": ["quay lui"], "b8:389-393": ["liền kề"], "b8:391": ["qua môn"],
 "b5:369": ["hàm mục tiêu"], "b5:397": ["chấp nhận được"], "b5:407-451": ["hình học"], "b5:451": ["đường số 3"],
 "b6:157-209": ["quay lui"], "b6:297-359": ["đồ thị"], "b6:11-27": ["khử"],
 "b7:31-41": ["vét cạn"], "b7:43-149": ["cây khung"], "b7:105-111": ["nhị phân"], "b7:137-149": ["t min"],
 "b7:153": ["học tủ"], "b7:153-235": ["mô hình thứ hai"], "b7:259": ["sort"], "b7:421-437": ["bỏ bớt"],
 "b7:493": ["quay lui và quy hoạch động"], "b7:497": ["cách giải khác"],
 "b8:47-67": ["vạch thước"], "b8:119": ["fibonacci"], "b8:137": ["giảm để trị"], "b8:307": ["đề thi"],
 "b9:3": ["một tờ giấy"], "b9:3-61": ["cấu trúc"], "b9:15": ["12 điểm"], "b9:21": ["ghi trực tiếp"], "b9:23": ["bị sót"],
 "b9:25": ["đếm"], "b9:29": ["làm hai phần"], "b9:31": ["dự kiến"], "b9:31-33": ["ba cái phương trình"], "b9:35": ["làm nháp"],
 "b9:39": ["ý tưởng"], "b9:41": ["lưu đồ"], "b9:41-45": ["input output"], "b9:45": ["nhập nhằn"], "b9:45-47": ["mã giả"],
 "b9:47": ["câu 3 hai điểm"], "b9:49": ["15 điểm"], "b9:51": ["chỉ là cấu trúc"], "b9:53": ["năm bài"], "b9:55": ["câu c"],
 "b9:57": ["9 10 điểm"], "b9:61": ["master"], "b9:67": ["quy hoạch động"], "b9:77-85": ["overlapping"],
 "b9:177-199": ["top down"], "b9:195": ["một vài bài toán con"], "b9:247": ["optimal substructure"], "b9:317": ["bonus"],
 "b9:441": ["tham lam"], "b9:443": ["chuỗi ma trận"], "b9:455": ["thứ bảy"], "b9:461": ["tô màu đồ thị"], "b9:465": ["điền số"],
}
refs_in_khung = sorted(set(re.findall(r"\bb[1-9]:\d+(?:-\d+)?", raw)))
missing_kw = [r for r in refs_in_khung if r not in REF_KW]
check("B", "mọi tham chiếu trong khung đều có từ khóa để kiểm", not missing_kw, str(missing_kw))
for r in refs_in_khung:
    if r not in REF_KW: continue
    b, span = r[1], r.split(":")[1]
    a, z = (map(int, span.split("-")) if "-" in span else (int(span), int(span)))
    seg = N(" ".join(T[int(b)][a-1:z]))
    kw = [k for k in REF_KW[r] if N(k) not in seg]
    check("B", f"{r} chứa {REF_KW[r]}", not kw)

# B2. Dẫn chứng theo chủ đề: REF_KW chỉ kiểm dòng được dẫn có một từ khóa chung chung (b9:61 chỉ cần "master"),
# nên bỏ lọt câu nhắc Fourier-Motzkin mà dẫn b9:61. Ở đây mỗi câu trong khung nhắc chủ đề T thì trong số
# các dẫn chứng của chính câu đó phải có ít nhất 1 dòng nhắc T (theo cách ASR ghi, vd "for maskin").
TOPIC_ASR = {"fourier-motzkin": ["for maskin", "for moskin", "for mkin"], "cây khung": ["cây khung"],
             "vạch thước": ["thước"], "fibonacci": ["fibonacci", "fibonaci", "fibonacy"], "chuỗi ma trận": ["chuỗi ma trận"],
             "tô màu đồ thị": ["tô màu"], "mã giả": ["mã giả"], "lưu đồ": ["lưu đồ"], "640": ["640"], "master": ["master"],
             "viết tay": ["viết tay"], "chèn": ["chèn", "chàn"], "không đệ quy": ["không đệ quy", "không để quy", "không đề quy"]}
topic_bad = []
for ln_no, line in enumerate(raw.splitlines(), 1):
    for sent in re.split(r"(?<=[.!?])\s+|\s\|\s", line):
        cites = re.findall(r"\bb([1-9]):(\d+)(?:-(\d+))?", sent)
        if not cites:
            continue
        segs = [" ".join(T[int(b)][int(a)-1:int(z or a)]) for b, a, z in cites]
        segs = [N(s) for s in segs]
        for topic, asr in TOPIC_ASR.items():
            if topic in N(sent) and not any(v in s for s in segs for v in asr):
                topic_bad.append(f"khung:{ln_no} '{topic}' nhưng dẫn {['b%s:%s' % (b, a + ('-' + z if z else '')) for b, a, z in cites]}")
check("B", "câu nhắc chủ đề nào thì có dẫn chứng nhắc đúng chủ đề đó", not topic_bad, "; ".join(topic_bad))

# ---------------- C. tính lại con số trong khung ----------------
check("C", "640: 7n² ≤ 8(n²−80n) ⟺ n ≥ 640",
      all(7*n*n <= 8*(n*n-80*n) for n in range(640, 5000)) and 7*639**2 > 8*(639**2-80*639) and has("640"))
lg = math.log2
def largest(f, hi, T=10**6):
    lo = 1
    while lo < hi:
        m = (lo+hi+1)//2
        lo, hi = (m, hi) if f(m) <= T else (lo, m-1)
    return lo
vals = {"n lg n: 62746": largest(lambda n: n*lg(n), 10**7) == 62746, "n²: 1000": largest(lambda n: n*n, 10**7) == 1000,
        "n³: 100": largest(lambda n: n**3, 10**7) == 100, "2ⁿ: 19": largest(lambda n: 2**n, 200) == 19,
        "n!: 9": largest(math.factorial, 50) == 9}
for k, ok in vals.items(): check("C", f"bảng 1 giây {k}", ok and has(k))
c8 = [11966,24303,39992,53010,67272,78692,91274,113063,129799,140538]
r = [c/(n*lg(n)) for n, c in zip(range(1000, 10001, 1000), c8)]
check("C", "Bài 8 HW02: count/(n lg n) trong 1.0-1.2", 1.0 <= min(r) and max(r) <= 1.21 and has("1.0-1.2"))
k = 64.0
for _ in range(200): k = 12*lg(k)
check("C", "n·lg⁴n < n^(4/3) chỉ khi n > ~3·10²²", 2.5e22 < 2**k < 3.5e22 and has("3·10²²"))
check("C", "Σk·k! = (n+1)! − 1", all(sum(j*math.factorial(j) for j in range(1, n+1)) == math.factorial(n+1)-1 for n in range(1, 15)))
# A2 dạng tổng T1 + T2 ∈ O(max(f, g)): c1·c2 không đủ, c1 + c2 thì đủ (cô chọn K = C + D ở b4:429).
t1 = t2 = f_ = g_ = (lambda n: n); c1 = c2 = 1
check("C", "A2 tổng: phản ví dụ T1 = T2 = f = g = n cho c₁c₂, còn c₁ + c₂ đúng",
      any(t1(n) + t2(n) > c1*c2*max(f_(n), g_(n)) for n in range(1, 100))
      and all(t1(n) + t2(n) <= (c1+c2)*max(f_(n), g_(n)) for n in range(1, 100)) and has("c = c₁ + c₂", "hằng số phải khác tên"))
def allv(xs, ops):
    if len(xs) == 1: return {xs[0]}
    return {(a+b if ops[k] == "+" else a*b) for k in range(len(ops)) for a in allv(xs[:k+1], ops[:k]) for b in allv(xs[k+1:], ops[k+1:])}
def maxonly(xs, ops):
    n = len(xs); D = [[None]*n for _ in range(n)]
    for i in range(n): D[i][i] = xs[i]
    for L in range(2, n+1):
        for i in range(n-L+1):
            j = i+L-1; D[i][j] = max((D[i][k]+D[k+1][j]) if ops[k] == "+" else D[i][k]*D[k+1][j] for k in range(i, j))
    return D
ex = ([2, -1, -3, 3, -4], ["*", "*", "+", "*"])
check("C", "phản ví dụ số âm: max đúng 30, DP chỉ max ra 0", max(allv(*ex)) == 30 and maxonly(*ex)[0][4] == 0 and 2*(-1*(-3+3*-4)) == 30)
D = maxonly([1, 2, 3, 4], ["+", "*", "+"])
check("C", "HK1 C3: hàng 0 = 1,3,9,21, DP[1][3] = 14", D[0] == [1, 3, 9, 21] and D[1][1:] == [2, 6, 14] and D[2][2:] == [3, 7])
w, p, M = [18, 15, 10], [25, 24, 15], 20
cap, val = M, 0
for i in sorted(range(3), key=lambda i: p[i]/w[i], reverse=True):
    t = min(1, cap/w[i]); val += p[i]*t; cap -= w[i]*t
check("C", "HK1 C6b = 31.5", val == 31.5 and has("31.5"))
items = [(10, 60), (20, 100), (30, 120)]
g, cap = 0, 50
for wi, pi in sorted(items, key=lambda x: x[1]/x[0], reverse=True):
    if wi <= cap: cap -= wi; g += pi
best = max(sum(q for _, q in s) for r_ in range(4) for s in combinations(items, r_) if sum(x for x, _ in s) <= 50)
check("C", "ba lô 0/1: tham lam 160, tối ưu 220", (g, best) == (160, 220))
cons = [(1, 0, 60), (0, 1, 75), (10, 8, 800), (-1, 0, 0), (0, -1, 0)]
pts = set()
for (a1, b1, c1), (a2, b2, c2) in combinations(cons, 2):
    d = a1*b2-a2*b1
    if d:
        x, y = Fr(c1*b2-c2*b1, d), Fr(a1*c2-a2*c1, d)
        if all(a*x+b*y <= c for a, b, c in cons): pts.add((x, y))
bx = max(pts, key=lambda q: 30*q[0]+20*q[1])
check("C", "radio: tối ưu (60, 25), lãi 2300", bx == (60, 25) and 30*60+20*25 == 2300)
order, memo = [], {}
def C_(n, k):
    if (n, k) in memo: return memo[(n, k)]
    v = 1 if k in (0, n) else C_(n-1, k-1) + C_(n-1, k)
    memo[(n, k)] = v; order.append((n, k)); return v
C_(3, 2)
check("C", "top-down C(3,2): (1,0),(1,1),(2,1),(2,2),(3,2)", order == [(1, 0), (1, 1), (2, 1), (2, 2), (3, 2)])
ok = True
for n in range(1, 200):
    ok &= sum(range(1, n+1)) == n*(n+1)//2 and sum(i*i for i in range(1, n+1)) == n*(n+1)*(2*n+1)//6
    ok &= sum(i*j for i in range(1, 60) for j in range(1, 60)) == (59*60//2)**2
check("C", "Σi, Σi², ΣΣij", ok)
check("C", "a^(log_b n) = n^(log_b a)", all(math.isclose(a**math.log(n, b), n**math.log(a, b), rel_tol=1e-9) for a, b in [(4, 2), (3, 2), (9, 3)] for n in [5, 100, 10**6]))
@lru_cache(None)
def H(n): return 1 if n == 1 else 2*H(n-1)+1
check("C", "Hà Nội 2ⁿ − 1", all(H(n) == 2**n-1 for n in range(1, 60)))
NN = 12
mul = lambda a, b: [sum(a[i]*b[k-i] for i in range(k+1)) for k in range(NN)]
geo = lambda a: [a**k for k in range(NN)]
check("C", "hàm sinh Hà Nội x/((1−x)(1−2x))", mul(mul([0, 1]+[0]*(NN-2), geo(1)), geo(2))[1:] == [2**n-1 for n in range(1, NN)])
check("C", "1/(1−x)² = Σ(n+1)xⁿ", mul(geo(1), geo(1)) == [n+1 for n in range(NN)])
lg3 = lg(3)
F = {"f1": lambda k: lg(4*k+lg(k)), "f4": lambda k: k+4*lg(k), "f2": lambda k: 4*k/3, "f3": lambda k: 4*k-2,
     "f5": lambda k: 5*k**3, "f6": lambda k: 2**(k/2)/2*lg3, "f7": lambda k: k/2+2**k/2*lg3}
ords = {" < ".join(sorted(F, key=lambda f: F[f](k))) for k in (200, 400, 900)}
check("C", "HK1 1b: f1 < f4 < f2 < f3 < f5 < f6 < f7", ords == {"f1 < f4 < f2 < f3 < f5 < f6 < f7"} and has("f₁ < f₄ < f₂ < f₃ < f₅ < f₆ < f₇"))


# C bổ sung: các con số còn lại trong khung
from math import isclose
check("C", "3^(lg n) = n^1.585", isclose(lg(3), 1.585, abs_tol=5e-4) and has("n^1.585"))
check("C", "(√3)ⁿ ≈ 1.73ⁿ < 2ⁿ", isclose(3**0.5, 1.732, abs_tol=1e-3) and has("1.73ⁿ"))
check("C", "ví dụ Θ: 0.001n⁴+3n³+1 = Θ(n⁴), 2^(n+1)+3^(n−1) = Θ(3ⁿ)",
      0.0009 < (0.001*1e6**4+3*1e6**3+1)/1e6**4 < 0.0041 and 0.3 < (2**201+3**199)/3**200 < 0.34)
# đoán nghiệm T=3T(n/2)+n²: quy nạp T(n) ≤ an²+b cần 3(a n²/4 + b) + n² ≤ a n² + b ⇔ (1 − a/4) n² + 2b ≤ 0, với a=4, b=0 thì bằng 0
check("C", "đoán nghiệm 3T(n/2)+n²: a = 4, b = 0 đủ, a = 3.9 thì hỏng", all((1-4/4)*n*n + 2*0 <= 0 for n in (2, 64, 10**6)) and (1-3.9/4)*1e6**2 > 0 and has("a = 4, b = 0"))
# T(n) ≤ cn với T = T(n/2)+T(n/4)+n: c n/2 + c n/4 + n ≤ c n ⇔ c ≥ 4
check("C", "T(n/2)+T(n/4)+n ≤ cn cần c ≥ 4", all(4*n/2 + 4*n/4 + n <= 4*n for n in (8, 1000)) and 3.9*1000/2+3.9*1000/4+1000 > 3.9*1000 and has("c ≥ 4"))
# CLRS 3-2 a-d: kiểm bằng tỉ số trong không gian log
lr = lambda la, lb: la - lb   # lg(A/B)
a_ = [lr(3*lg(L), 0.5*L) for L in (1e3, 1e6)]                   # lg^3 n vs n^0.5 (k=3, ε=0.5), L = lg n
b_ = [lr(3*L2, (2**L2)*lg(1.5)) for L2 in (10, 20)]            # n^3 vs 1.5^n, L2 = lg n
d_ = [lr(n, n/2) for n in (10, 100)]                            # 2^n vs 2^(n/2)
check("C", "CLRS 3-2 a, b: A = o(B) (tỉ số → 0), d: A = ω(B)", a_[1] < a_[0] < 0 and b_[1] < b_[0] < 0 and d_[1] > d_[0] > 0 and has("a: yes yes no no no", "d: no no yes yes no"))
check("C", "(lg n)! nhỏ hơn n^(lg lg n): lg((lg n)!) < lg n · lg lg n", all(math.lgamma(L+1)/math.log(2) < L*lg(L) for L in (2**6, 2**12, 2**20)))


import itertools as _it
def _dp_adj(a):
    M = [1]*len(a)
    for i in range(len(a)):
        for j in range(i):
            if abs(a[i]-a[j]) == 1: M[i] = max(M[i], M[j]+1)
    return max(M) if a else 0
def _bf_adj(a):
    return max((r for r in range(1, len(a)+1) for ix in _it.combinations(range(len(a)), r) if all(abs(a[ix[t+1]]-a[ix[t]]) == 1 for t in range(r-1))), default=0)
import random as _r; _r.seed(5)
check("C", "biến thể LIS |a_i − a_j| = 1 đúng với vét cạn (2000 mảng)", all(_dp_adj(a) == _bf_adj(a) for a in ([_r.randint(0, 6) for _ in range(_r.randint(1, 8))] for _ in range(2000))) and has("|a_i − a_j| = 1"))

# ---------------- D. bài giữ riêng (bài thật của cô, không dùng khi dựng khung) ----------------
# D1. HW02 Bài 1 group 1: cần quy tắc giữ hạng tử lớn nhất, a^(n+k) = a^k·aⁿ, lg của lũy thừa
check("D", "HW02 B1: có quy tắc giữ hạng tử bậc cao nhất, bỏ hệ số", has("giữ hạng tử"))
check("D", "HW02 B1: có quy tắc a^(n+k) = a^k·aⁿ (cùng lớp aⁿ)", has("a^(n+k)"))
check("D", "HW02 B1: có quy tắc lg(xᵏ) = k·lg x", has("lg(xᵏ)"))
# lg f tính giải tích tại n = 2^k (tránh tràn số). 5·lg((n+100)^10) = 50·lg(n+100) (cách đọc 5·lg((n+100)^10), khung ghi rõ phải nêu cách đọc).
grp = {"(n−2)!": lambda k: 2**k*(k-1/math.log(2)), "5lg(n+100)^10": lambda k: lg(50)+lg(k),
       "2^(2n)": lambda k: 2*2**k, "0.001n⁴+3n³+1": lambda k: lg(0.001)+4*k, "ln²n": lambda k: 2*lg(k*math.log(2)),
       "∛n": lambda k: k/3, "3ⁿ": lambda k: 2**k*lg3}
got = " < ".join(sorted(grp, key=lambda f: grp[f](1000)))
exp = "5lg(n+100)^10 < ln²n < ∛n < 0.001n⁴+3n³+1 < 3ⁿ < 2^(2n) < (n−2)!"
check("D", "HW02 B1 đáp án tính được", got == exp, got)
kx = 50/math.log(2)**2
check("D", "bẫy thế số: 50·lg n > ln²n tới n ≈ 2^104, sau đó mới nhỏ hơn",
      104 < kx < 104.2 and 50*40 > (40*math.log(2))**2 and 50*200 < (200*math.log(2))**2 and has("2^104"))
# D2. HW02 Bài 1 group 2 (CLRS 3-3): hàm hóc
check("D", "CLRS 3-3: có lg* (log sao), n^(1/lg n) = 2, (lg n)! ", has("lg*", "n^(1/lg n)", "(lg n)!"))
check("D", "n^(1/lg n) = 2", all(math.isclose(n**(1/lg(n)), 2) for n in (4, 1000, 10**9)))
check("D", "(√2)^(lg n) = √n, 2^(lg n) = n, 4^(lg n) = n²", all(math.isclose(math.sqrt(2)**lg(n), math.sqrt(n)) and math.isclose(4**lg(n), n*n) for n in (8, 10**6)))
check("D", "lg((lg n)!) = Θ(lg n · lg lg n) nên (lg n)! lớn hơn đa thức", all(math.lgamma(L+1)/math.log(2) > 3*L for L in (2**10, 2**14)))
check("D", "n^(lg lg n) = (lg n)^(lg n)", all(math.isclose(lg(n)*lg(lg(n)), lg(n)*lg(lg(n))) and math.isclose(n**lg(lg(n)), lg(n)**lg(n), rel_tol=1e-9) for n in (16, 1024, 10**6)))
def lgstar(x):
    c = 0
    while x > 1: x = lg(x); c += 1
    return c
check("D", "lg*(lg n) = lg* n − 1", all(lgstar(lg(n)) == lgstar(n)-1 for n in (5, 17, 65537, 10**18)))
Ln = 10**4  # lg n
check("D", "2^(√(2 lg n)) nằm giữa lg³n và n^0.1 khi n lớn", 3*lg(Ln) < math.sqrt(2*Ln) < 0.1*Ln and has("2^(√(2 lg n))"))
# D3. HW02 Bài 2 (Levitin): a-d đúng/sai
t = lambda n: n*(n+1)/2
check("D", "HW02 B2a-d: đúng, đúng, sai, đúng", t(10**6)/1e18 < 1 and t(10**6)/1e12 < 1 and t(10**6)/1e18 < 1e-3 and t(10**6)/1e6 > 1)
check("D", "HW02 B2 (2e): ⌊log₂ n⌋ = Θ(lg n)", all(0.5*lg(n) <= math.floor(lg(n)) <= lg(n) for n in range(2, 10**5)))
# D4. HW02 Bài 3: cần mẫu phản ví dụ cho "disprove"
check("D", "HW02 B3: có mẫu 'phản ví dụ' cho mệnh đề sai", has("phản ví dụ cụ thể"))
# t = n, g = n^(1+sin n): lg(t/g)/lg n = −sin n dao động gần ±1, nên t không O(g) cũng không Ω(g)
osc = [-math.sin(n) for n in range(10, 200000)]
check("D", "HW02 B3d sai: t=n, g=n^(1+sin n) dao động, không O cũng không Ω", max(osc) > 0.999 and min(osc) < -0.999 and has("n^(1+sin n)"))
# D5. HW02 Bài 5: tổng
check("D", "HW02 B5: có tổng cấp số nhân và tổng đổi cận", has("cấp số nhân", "đổi cận"))
s = {"1+3+...+999 = 250000": sum(range(1, 1000, 2)) == 250000,
     "2+4+...+1024 = 2046": sum(2**i for i in range(1, 11)) == 2046,
     "Σ_{i=3}^{n+1} 1 = n−1": all(sum(1 for _ in range(3, n+2)) == n-1 for n in range(2, 50)),
     "Σ_{i=0}^{n-1} i(i+1) = (n−1)n(n+1)/3": all(sum(i*(i+1) for i in range(n)) == (n-1)*n*(n+1)//3 for n in range(1, 60)),
     "Σ_{j=1}^{n} 3^{j+1} = (3^{n+2}−9)/2": all(sum(3**(j+1) for j in range(1, n+1)) == (3**(n+2)-9)//2 for n in range(1, 30)),
     "Σ 1/(i(i+1)) = n/(n+1)": all(sum(Fr(1, i*(i+1)) for i in range(1, n+1)) == Fr(n, n+1) for n in range(1, 40))}
for kk, ok in s.items(): check("D", f"HW02 B5: {kk}", ok)
# D6. HW02 Bài 9 và HW01: phương trình đệ quy của cô
def seq(rec, init, n):
    a = list(init)
    while len(a) < n: a.append(rec(a))
    return a
a1 = seq(lambda a: 7*a[-1]-12*a[-2], [1, 2], 25)
check("D", "HW02 B9 hàm sinh: T=7T(n−1)−12T(n−2) ⇒ 2·3ⁿ − 4ⁿ", a1 == [2*3**n-4**n for n in range(25)])
b1 = seq(lambda a: a[-1]+3*(len(a)-1), [7], 30)
check("D", "HW02 B9: T(n+1)=T(n)+3n, T(0)=7 ⇒ 7 + 3n(n−1)/2", b1 == [7+3*n*(n-1)//2 for n in range(30)])
c1 = seq(lambda a: 4*a[-1]-5*a[-2]+2*a[-3], [0, 1, 2], 30)
check("D", "HW02 B9 đặc trưng: r=1 (kép), r=2 nhưng hệ số của 2ⁿ bằng 0 ⇒ T(n) = n", c1 == list(range(30)) and has("nghiệm kép", "T(n) = n"))
phi = (1+5**.5)/2
d1 = seq(lambda a: a[-1]+a[-2], [1, 1], 40)
check("D", "HW02 B9: T=T(n−1)+T(n−2), T0=T1=1 là Fibonacci lệch 1", all(abs(d1[n]-(phi**(n+1)-(1-phi)**(n+1))/5**.5) < 1e-6 for n in range(40)))
@lru_cache(None)
def e1(n): return 1 if n == 1 else 3*e1(n//2)+n*n
check("D", "HW02 B9 đoán nghiệm: T=3T(n/2)+n², đoán an²+b ⇒ 4n² − 3n^(lg 3), Θ(n²)",
      all(abs(e1(2**k) - (4*4**k - 3*3**k)) == 0 for k in range(0, 20)) and has("đoán nghiệm"))
@lru_cache(None)
def f1(n): return 1 if n <= 5 else f1(n//2)+f1(n//4)+n
check("D", "HW02 B9: T=T(n/2)+T(n/4)+n = O(n) (T(n)/n bị chặn)", max(f1(n)/n for n in range(6, 20000)) < 4.1)
@lru_cache(None)
def g1(n): return 1 if n == 1 else 4*g1(n//3)+n
check("D", "HW02 B9 truy hồi: T=4T(n/3)+n ⇒ 4·4ᵏ − 3·3ᵏ với n = 3ᵏ", all(g1(3**k) == 4*4**k - 3*3**k for k in range(15)) and has("n = 3ᵏ", "4·4ᵏ − 3·3ᵏ"))
@lru_cache(None)
def h1(n): return 1 if n == 1 else 2*h1(n//2)+lg(n)
check("D", "HW02 B9 truy hồi: T=2T(n/2)+lg n ⇒ Θ(n)", max(h1(2**k)/2**k for k in range(1, 40)) < 3.01)
x5 = seq(lambda a: a[-1]+5, [0], 30)
check("D", "HW01 B5: x(n)=x(n−1)+5, x(1)=0 ⇒ 5(n−1)", x5 == [5*n for n in range(30)])
@lru_cache(None)
def fm(n): return 1 if n == 1 else 2*fm(n//2)+1
check("D", "HW01 B1 findMax: T=2T(n/2)+c ⇒ Θ(n)", all(fm(2**k) == 2**(k+1)-1 for k in range(30)))
@lru_cache(None)
def f3(n): return 1 if n == 0 else 3*f3(n//2)+n*n
check("D", "HW01 B3: T=3T(n/2)+n² ⇒ Θ(n²)", max(f3(2**k)/4**k for k in range(1, 30)) < 5)
check("D", "HW01 B1, B3: thành lập PT có 'chi phí khác' (vòng for lồng)", has("chi phí khác", "chi phí phân chia"))
check("D", "Levitin: 5 bước phân tích thuật toán không đệ quy (b1:187)", has("5 bước"))

# ---------------- E. đưa câu chữ đề thật qua bảng cụm từ ----------------
try:
    import pymupdf
    hk1 = "".join(pg.get_text() for pg in pymupdf.open(os.path.join(REPO, "bai_tap/Đề thi mẫu/2025/DethiCK.HK1.2025.2026 (TX.F31.CN2.TTNT).pdf")))
except Exception as e:
    hk1 = ""
check("E", "đọc được text đề HK1", len(hk1) > 3000)
H1 = N(hk1)
ROUTES = [  # (câu, đoạn trong đề thật, cụm từ khung phải có, dạng khung phải dẫn tới)
 ("HK1 1a", "dùng định nghĩa của các ký hiệu tiệm cận để chứng minh", "O(f(n)) = O(g(n))", "hai tập bằng nhau"),
 ("HK1 1b", "phân lớp 07 hàm", "Phân lớp ... Big-O nhỏ nhất", "B. Phân lớp"),
 ("HK1 2a", "thành lập phương trình đệ quy", "Thành lập phương trình đệ quy", "chi phí khác"),
 ("HK1 2a", "không sử dụng các hằng số như c1, c2", "không dùng hằng số c1, c2", "con số cụ thể"),
 ("HK1 2b", "sử dụng 02 phương pháp", "Sử dụng 02 phương pháp", "2 cách chỉ định"),
 ("HK1 3", "áp dụng phương pháp quy hoạch động", "QHĐ", "phương trình QHĐ"),
 ("HK1 4", "theo 02 cách", "theo 02 cách", "2 chiến lược"),
 ("HK1 4", "liệt kê tất cả các hoán vị", "liệt kê tất cả", "Quay lui"),
 ("HK1 5", "tìm tất cả các hành trình", "tìm tất cả", "Quay lui"),
 ("HK1 5", "mô hình hóa bài toán", "mô hình hóa", "hàm mục tiêu"),
 ("HK1 6", "có thể được chia nhỏ", "có thể chia nhỏ", "Tham lam"),
]
for q, frag, khung_kw, dest in ROUTES:
    in_exam = N(frag) in H1
    check("E", f"{q}: đề có '{frag[:32]}'", in_exam)
    check("E", f"{q}: khung có cụm '{khung_kw}' dẫn tới '{dest}'", has(khung_kw) and has(dest))
hk3 = N(open(os.path.join(REPO, "bai_tap/Đề thi mẫu/CS112.DE_THI_CK.HK3.2025-2026.md"), encoding="utf-8").read())
for frag, khung_kw in [("không dùng định lý, không dùng lim", "Về lim"), ("big-o nhỏ nhất", "Big-O nhỏ nhất"),
                       ("trả về (hay in ra màn hình)", "trả về (hay in ra màn hình)"), ("chọn làm 1 trong 2", "Phân tích bài toán"),
                       ("mã giả & đánh giá độ phức tạp", "Mã giả và cấu trúc dữ liệu")]:
    check("E", f"HK3 dựng: '{frag[:30]}' ↔ khung '{khung_kw}'", N(frag) in hk3 and has(khung_kw))
check("E", "khung nói rõ HK3 dựng có cụm 'không dùng lim' nhưng không phải đề thật", has("không dùng định lý, không dùng lim"))


# ---------------- F. định tuyến trên đề chưa dùng để dựng khung ----------------
# Mô phỏng cách dùng: lấy câu chữ từng câu trong đề, tìm cụm từ của khung khớp với nó.
# Cụm từ lấy thẳng từ cột 1 các bảng trong khung, tên chiến lược, và tiêu đề sườn 3.2.
def triggers_from_khung(text):
    trig = []
    for line in text.splitlines():
        if line.startswith("|") and not line.startswith("|---"):
            first = line.split("|")[1]
            for q in re.findall(r'"([^"]+)"', first):
                for alt in q.split(" / "):
                    pat = re.sub(r"(\\ )?\\.\\.\\.(\\ )?", ".{0,160}", re.escape(N(alt.strip())))
                    trig.append((alt.strip(), pat))
    for h in re.findall(r"^\*\*([^*]+)\*\*", text, flags=re.M):
        trig.append((h, re.escape(N(h))))
    for name in ["quay lui", "quy hoạch động", "tham lam", "chia để trị", "giảm để trị", "backtracking", "dynamic programming", "greedy"]:
        trig.append((name, re.escape(name)))
    return trig
TR = triggers_from_khung(raw)
def route(qtext):
    q = N(re.sub(r"\s+", " ", re.sub(r"[“”\"'*`]", "", qtext)))
    return sorted({name for name, pat in TR if re.search(pat, q)})
exams = {}
for fn in ["CS112_De_Thi_Mau_So_01.md", "CS112_De_Thi_Mau_So_02.md", "CS112_De_Thi_Mau_So_03.md"]:
    t = open(os.path.join(REPO, "bai_tap/Đề thi mẫu/Đề mẫu", fn), encoding="utf-8").read()
    parts = re.split(r"(?m)^### (Câu \d+[^\n]*)", t)
    for i in range(1, len(parts), 2):
        head, body = parts[i], parts[i+1]   # người đọc thấy cả tiêu đề câu lẫn nội dung
        subs = re.split(r"\*\*([a-c]\. \([^)]*\))\*\*", body)
        if len(subs) > 1:
            for j in range(1, len(subs), 2):
                exams[f"{fn[-5:-3]} {head[:6]} {subs[j][:2]}"] = head + " " + subs[j+1]
        else:
            exams[f"{fn[-5:-3]} {head[:6]}"] = head + " " + body
if hk1:
    for m in re.finditer(r"Câu (\d) \(2\.5 điểm\)(.*?)(?=Câu \d \(2\.5 điểm\)|HẾT)", hk1, flags=re.S):
        exams[f"HK1 Câu {m.group(1)}"] = m.group(2)
unrouted = []
ROUTED = {}
for k, body in exams.items():
    r = route(body)
    if not r: unrouted.append(k)
    check("F", f"{k} → {', '.join(r[:4]) or 'KHÔNG KHỚP'}", bool(r))
    ROUTED[k] = r
print(f"F: {len(exams)} câu, {len(exams)-len(unrouted)} khớp ít nhất 1 cụm từ của khung")


# F2. kỳ vọng định tuyến cho từng câu (mình đọc đề và gán đích đúng). Không phải held-out: đề mẫu dùng để dựng v1, HK1 dùng để dựng v2.
A_FAM = {"Dùng định nghĩa ... chứng minh", "O(f(n)) = O(g(n))", "phản chứng", "Nếu ... ∈ ... thì ...", "Nếu ... thì ..."}
EXPECT = {}
for k in ROUTED:
    if "Câu 1  a." in k: EXPECT[k] = [A_FAM]
    elif "Câu 1  b." in k: EXPECT[k] = [{"Phân lớp ... Big-O nhỏ nhất ... sắp xếp"}]
    elif "Câu 2  a." in k: EXPECT[k] = [{"chức năng", "trả về ... thông tin gì", "trả về (hay in ra màn hình)"}, {"Đếm số phép", "Hãy đếm"}]
    elif "Câu 2  b." in k: EXPECT[k] = [{"Thành lập phương trình đệ quy"}]
    elif "Câu 2  c." in k: EXPECT[k] = [{"chọn giải 01 trong 03"}]
    elif k.endswith("Câu 3 ") or k.endswith("Câu 3"): EXPECT[k] = [{"Phân tích bài toán"}]
    elif k.startswith("0") and "Câu 4" in k: EXPECT[k] = [{"quay lui", "Quay lui", "backtracking"}]
    elif k.startswith("0") and "Câu 5" in k: EXPECT[k] = [{"quy hoạch động", "dynamic programming"}]
EXPECT.update({"HK1 Câu 1": [A_FAM, {"Phân lớp ... Big-O nhỏ nhất ... sắp xếp"}],
               "HK1 Câu 2": [{"Thành lập phương trình đệ quy"}, {"Sử dụng 02 phương pháp ... để giải"}],
               "HK1 Câu 3": [{"quy hoạch động", "dynamic programming"}],
               "HK1 Câu 4": [{"quay lui", "backtracking"}, {"giảm để trị"}, {"theo 02 cách ... so sánh"}],
               "HK1 Câu 5": [{"tìm tất cả", "quay lui"}, {"Mô hình hóa bài toán"}],
               "HK1 Câu 6": [{"tham lam", "Tham lam", "greedy"}, {"Mô hình hóa bài toán"}]})
FORBID = {"count": "khớp nhầm biến count trong code", "Nếu ... thì ...": "cụm quá rộng, khớp nhầm câu thường", "sums": "cụm tổng khớp nhầm câu Σ trong đề"}
for k, need in EXPECT.items():
    r = set(ROUTED.get(k, []))
    miss = [sorted(n)[0] for n in need if not (r & n)]
    bad = [f for f in FORBID if f in r and not (k.endswith("Câu 1  a.") and f == "Nếu ... thì ...")]
    check("F2", f"{k}: đúng đích" + (f" (thiếu {miss})" if miss else "") + (f" (khớp nhầm {bad})" if bad else ""), not miss and not bad)

# G. held-out: đề bài HW02 (tiếng Anh, chép từ ảnh slide trang 17-26), KHÔNG dùng khi dựng bảng cụm từ.
HW02 = {
 "B1a": ("List the following functions according to their order of growth from the lowest to the highest", {"order of growth", "Phân lớp ... Big-O nhỏ nhất ... sắp xếp"}),
 "B1b": ("Rank the following functions by order of growth; that is, find an arrangement g1, g2, ..., g30 of the functions satisfying g1 = Ω(g2). Partition your list into equivalence classes such that f(n) and g(n) are in the same class if and only if f(n) = Θ(g(n)).", {"order of growth"}),
 "B2a": ("Use the informal definitions of O, Θ, and Ω to determine whether the following assertions are true or false.", {"true or false"}),
 "B2b": ("For each of the following functions, indicate the class Θ(g(n)) the function belongs to. (Use the simplest g(n) possible in your answers.) Prove your assertions.", {"indicate the class", "simplest g(n)"}),
 "B3":  ("Prove the following assertions by using the definitions of the notations involved, or disprove them by giving a specific counterexample.", {"Prove ... or disprove", "disprove"}),
 "B4":  ("Let f(n) and g(n) be asymptotically positive functions. Prove or disprove each of the following conjectures.", {"Prove ... or disprove", "disprove"}),
 "B5a": ("Compute the following sums.", {"Compute the following sums", "sums"}),
 "B5b": ("Find the order of growth of the following sums. Use the Θ(g(n)) notation with the simplest function g(n) possible.", {"order of growth", "sums"}),
 "B6":  ("For each function f(n) and time t in the following table, determine the largest size n of a problem that can be solved in time t, assuming that the algorithm to solve the problem takes f(n) microseconds.", {"largest size n ... solved in time t"}),
 "B7":  ("Indicate, for each pair of expressions (A, B) in the table below, whether A is O, o, Ω, ω, or Θ of B. Your answer should be in the form of the table with yes or no written in each box.", {"O, o, Ω, ω, or Θ", "yes or no"}),
 "B8":  ("Hypothesize a likely efficiency class of an algorithm based on the following empirical observations of its basic operation's count", {"Hypothesize ... efficiency class", "empirical"}),
 "B9a": ("Giải bằng Truy hồi: T(n) = 2T(n/2) + log n, T(1) = 1", {"Truy hồi", "Giải bằng Truy hồi"}),
 "B9b": ("Giải bằng Hàm sinh: T(n) = 7T(n-1) - 12T(n-2)", {"Hàm sinh"}),
 "B9c": ("Giải bằng Phương trình đặc trưng: T(n) = 4T(n-1) - 5T(n-2) + 2T(n-3)", {"Phương trình đặc trưng"}),
 "B9d": ("Giải bằng Đoán nghiệm: T(n) = 3T(n/2) + n^2. Đoán f(n) = an^2 + b", {"Đoán nghiệm"}),
}
g_ok = 0
for k, (txt, need) in HW02.items():
    r = set(route(txt)); ok = bool(r & need); g_ok += ok
    check("G", f"HW02 {k} → {sorted(r)[:3] or 'KHÔNG KHỚP'}", ok)
print(f"G (held-out HW02): {g_ok}/{len(HW02)} câu tới đúng dạng")


# P. độ chính xác (precision): đếm chiến lược bị khớp nhầm. Họ chiến lược lấy từ bảng 3.1 của chính khung.
sec = raw.split("### 3.1", 1)[1].split("### 3.2", 1)[0] if "### 3.1" in raw else ""
FAM = []
for line in sec.splitlines():
    if line.startswith("|") and not line.startswith("|---") and "Cụm từ trong đề" not in line:
        cells = line.split("|")
        fam = re.split(r"[.(]", cells[2].strip())[0].strip()
        for q in re.findall(r'"([^"]+)"', cells[1]):
            FAM.append((fam, re.sub(r"(\\ )?\\.\\.\\.(\\ )?", ".{0,160}", re.escape(N(q)))))
def fams(qtext):
    q = N(re.sub(r"\s+", " ", re.sub(r"[“”\"'*`]", "", qtext)))
    return {f for f, pat in FAM if re.search(pat, q)}
ALLOW = {}
for k in exams:
    if "Câu 1" in k or "Câu 2" in k: ALLOW[k] = set()
    elif k.startswith("0") and "Câu 4" in k: ALLOW[k] = {"Quay lui"}
    elif k.startswith("0") and "Câu 5" in k: ALLOW[k] = {"QHĐ"}
ALLOW.update({"HK1 Câu 3": {"QHĐ"}, "HK1 Câu 4": {"Quay lui", "Giảm để trị", "2 chiến lược"},
              "HK1 Câu 5": {"Quay lui", "Mô hình hóa"}, "HK1 Câu 6": {"Tham lam", "Mô hình hóa"}})
extras = {}
for k, allow in ALLOW.items():
    if k not in exams: continue  # không có pymupdf thì thiếu đề HK1, nhóm E đã báo FAIL
    x = fams(exams[k]) - allow
    if x: extras[k] = sorted(x)
print(f"P (precision): {sum(len(v) for v in extras.values())} lần khớp nhầm họ chiến lược trên {len(ALLOW)} câu: {extras}")
check("P", "khung có cảnh báo phân biệt 'tất cả các lời giải' với 'tính tất cả các giá trị DP'", has("tất cả các lời giải", "tính tất cả các giá trị DP"))

# H. held-out thật: đề WeCode (phát biểu trong Ôn Luyện/Tong_Hop_...md). Chưa từng dùng để viết bảng cụm từ.
# Bài 7 (Minesweeper kiểu click) bỏ ra vì không chắc đó là đề WeCode của cô.
tong = open(os.path.join(REPO, "bai_tap/Đề thi mẫu/Ôn Luyện/Tong_Hop_Toan_Bo_Bai_Tap_WeCode_Va_Loi_Giai_Chuan_Co_Thuong.md"), encoding="utf-8").read()
WECODE = {m.group(1): m.group(2) for m in re.finditer(r"## (BÀI [1-5]): [^\n]+\n+### 1\. Phát biểu bài toán:\n(.*?)(?=\n### )", tong, flags=re.S)}
check("H", "đọc được 5 đề WeCode", len(WECODE) == 5, str(list(WECODE)))
h_ok = 0
for k, txt in WECODE.items():
    ok = "Quay lui" in fams(txt); r = set(route(txt)); h_ok += ok
    check("H", f"WeCode {k} → {sorted(r)[:3] or 'KHÔNG KHỚP'}", ok)
print(f"H (held-out WeCode): {h_ok}/{len(WECODE)} đề tới Quay lui")




# I. held-out mock_exam_pttktt.md: nhãn kỳ vọng gán TRƯỚC khi chạy. Không sửa khung theo kết quả nhóm này.
mock = open(os.path.join(REPO, "bai_tap/Đề thi mẫu/mock_exam_pttktt.md"), encoding="utf-8").read()
MOCK = {}
for part in re.split(r"(?m)^## ", mock)[1:]:
    head = part.split("\n", 1)[0]
    subs = re.split(r"\*\*([a-d])\) \([^)]*\)\*\*", part)
    for j in range(1, len(subs), 2):
        MOCK[f"{head[:5]} {subs[j]}"] = head + " " + subs[j+1]
LABEL = {"Câu 1 a": {"Phân lớp ... Big-O nhỏ nhất ... sắp xếp", "order of growth", "độ phức tạp thời gian tăng dần"},
         "Câu 1 b": {"Dùng định nghĩa ... chứng minh"},
         "Câu 2 a": {"chức năng", "trả về ... thông tin gì"},
         "Câu 2 b": {"basic operation", "Đếm số phép"},
         "Câu 2 c": {"Thành lập phương trình đệ quy", "recurrence relation", "hệ thức truy hồi", "phương trình truy hồi"},
         "Câu 2 d": {"Master", "định lý Thợ"},
         "Câu 3 a": {"Phân tích bài toán", "Xác định rõ Input"},
         "Câu 3 b": {"Tham lam", "Greedy"},
         "Câu 3 c": {"Tham lam", "Greedy", "Minh họa"},
         "Câu 4 a": {"Mã giả và cấu trúc dữ liệu", "Mã giả"},
         "Câu 4 b": {"Mã giả và cấu trúc dữ liệu", "độ phức tạp"},
         "Câu 5 a": {"QHĐ", "Quy hoạch động", "chuỗi ma trận"},
         "Câu 5 b": {"QHĐ", "Quy hoạch động", "chuỗi ma trận"},
         "Câu 5 c": {"QHĐ", "Quy hoạch động", "chuỗi ma trận", "Bottom-Up"}}
i_ok = 0; misses = []
for k, txt in MOCK.items():
    r = set(route(txt)) | {f for f in fams(txt)}
    ok = bool(r & LABEL.get(k, set())); i_ok += ok
    if not ok: misses.append((k, sorted(r)[:3]))
print(f"I (held-out mock_exam, nhãn gán trước): {i_ok}/{len(MOCK)} ý tới đúng dạng. Hụt: {misses}")
check("I", "đã đo held-out mock_exam (kết quả chỉ báo cáo, không phải điều kiện PASS)", len(MOCK) == 14)


# I2. cùng tập mock_exam, chấm theo ĐÍCH (sườn học sinh sẽ làm), không theo tên cụm từ.
# Đích mỗi ý giữ nguyên ý nghĩa nhãn đã gán trước ở I. Đích của cụm từ = cột 2 của hàng chứa nó.
CUE_DEST = []
for line in raw.splitlines():
    if line.startswith("|") and not line.startswith("|---"):
        cells = line.split("|")
        if len(cells) > 3:
            for q in re.findall(r'"([^"]+)"', cells[1]):
                CUE_DEST.append((re.sub(r"(\\ )?\\.\\.\\.(\\ )?", ".{0,160}", re.escape(N(q))), N(cells[2])))
for h in re.findall(r"^\*\*([^*]+)\*\*", raw, flags=re.M):
    CUE_DEST.append((re.escape(N(h)), N(h)))
def dests(qtext):
    q = N(re.sub(r"\s+", " ", re.sub(r"[“”\"'*`]", "", qtext)))
    return [d for pat, d in CUE_DEST if re.search(pat, q)]
WANT = {"Câu 1 a": "b. phân lớp", "Câu 1 b": "a1.", "Câu 2 a": "chạy tay", "Câu 2 b": "mỗi vòng lặp là một σ",
        "Câu 2 c": "t\\(cơ sở\\)", "Câu 2 d": "master", "Câu 3 a": "phân tích bài toán", "Câu 3 b": "tham lam",
        "Câu 3 c": "phân tích bài toán|tham lam", "Câu 4 a": "mã giả và cấu trúc dữ liệu", "Câu 4 b": "mã giả và cấu trúc dữ liệu",
        "Câu 5 a": "qhđ", "Câu 5 b": "qhđ", "Câu 5 c": "qhđ"}
i2 = 0; miss2 = []
for k, txt in MOCK.items():
    ds = dests(txt); ok = any(re.search(WANT[k], d) for d in ds); i2 += ok
    if not ok: miss2.append(k)
print(f"I2 (mock_exam chấm theo đích): {i2}/{len(MOCK)}. Hụt: {miss2}")


# J. held-out cuối: suon_de_thi_pttktt.md. Nhãn đích gán TRƯỚC khi chạy, không sửa khung sau khi xem kết quả.
suon = open(os.path.join(REPO, "bai_tap/Đề thi mẫu/suon_de_thi_pttktt.md"), encoding="utf-8").read()
ITEMS = {}
for sec in re.split(r"(?m)^### ", suon)[1:]:
    head = re.match(r"(Câu \d+)", sec).group(1) if re.match(r"(Câu \d+)", sec) else sec[:6]
    for ln in sec.splitlines()[1:]:
        m = re.match(r"\s*(?:- \*\*(Dạng \d+|Nội dung):\*\*|(\d)\.)\s*(.+)", ln)
        if m:
            key = f"{head} {(m.group(1) or m.group(2))}"
            ITEMS[key] = m.group(3)
J_WANT = {"Câu 1 Dạng 1": "a1.|a4.|a5.", "Câu 1 Dạng 2": "b. phân lớp",
          "Câu 2 1": "chạy tay|phân tích bài toán", "Câu 2 2": "mỗi vòng lặp là một σ|cách cô đếm", "Câu 2 3": "t\\(cơ sở\\)|mỗi vòng lặp", "Câu 2 4": "truy hồi|thế 3 lần",
          "Câu 3 Nội dung": "chia để trị|tham lam", "Câu 3 1": "phân tích bài toán", "Câu 3 2": "phân tích bài toán", "Câu 3 3": "phân tích bài toán",
          "Câu 4 1": "mã giả và cấu trúc dữ liệu", "Câu 4 2": "mã giả và cấu trúc dữ liệu",
          "Câu 5 1": "qhđ", "Câu 5 2": "t\\(cơ sở\\)|qhđ", "Câu 5 3": "qhđ", "Câu 5 4": "qhđ", "Câu 5 5": "qhđ"}
j_ok = 0; j_miss = []
for k, want in J_WANT.items():
    txt = ITEMS.get(k, "")
    ds = dests(txt); ok = bool(txt) and any(re.search(want, d) for d in ds); j_ok += ok
    if not ok: j_miss.append(k)
print(f"J (held-out suon_de_thi, nhãn gán trước): {j_ok}/{len(J_WANT)}. Hụt: {j_miss}")
check("J", "đọc được đủ 17 ý của suon_de_thi", sum(1 for k in J_WANT if ITEMS.get(k)) == len(J_WANT), str([k for k in J_WANT if not ITEMS.get(k)]))


# K. held-out SẠCH: câu hỏi đề thi cũ do CÔ đọc trong transcript. Nhãn đích gán TRƯỚC lần chạy đầu, không sửa khung theo nhóm này.
# Văn nói nên đôi khi sai chính tả ("dãy con", "tri hồi"). Mỗi mục: (nguồn, câu chữ cô đọc, đích regex trên cột 2 của khung, họ chiến lược cho phép)
KCASES = {
 "b8:389 dãy con liền kề ±1": ("cho một cái mãng A tìm dãy con dài nhất không phải tăng mà là dài nhất thỏa điều kiện hai phần tử liền kề trên nhân một đơn vị", "qhđ", {"QHĐ"}),
 "b8:363 điền mảng M (LIS)": ("đề thi nó cho nguyên một cái dãy a vậy. Kêu em điền cho cô cái mãng m điền full cái mãng m luôn", "qhđ", {"QHĐ"}),
 "b8:49 vạch thước": ("Cho một cây thước có độ dài là L rồi một cái chiều cao H. Nhiệm vụ của em là dùng chương trình máy tính vạch ra được những cái đường kẻ như vậy. người ta đưa ra khuyến nghị mình dùng cái giải pháp chia để trị", "chia để trị", {"Chia để trị"}),
 "b8:119 Fibonacci": ("Dãy fibonacci là một cái dãy số mà hai cái số đầu tiên là số 1. yêu cầu của bài toán fibonacci là hãy cho biết cái số fibonaci thứ n trong cái dãy này", "qhđ", {"QHĐ"}),
 "b9:201 đặt ngoặc (đề)": ("có một biểu thức toán học mà trong biểu thức đó chỉ dùng phép toán cộng và phép toán nhân thôi. Hãy xác định cách đặt dấu ngoặc sao cho giá trị của biểu thức là lớn nhất", "qhđ", {"QHĐ"}),
 "b9:231 câu a điền bảng": ("Làm câu A. Câu A cô có vẽ sẵn một cái bảng mình điền số vô", "qhđ", {"QHĐ"}),
 "b9:245 câu b giá trị lớn nhất": ("Cái câu B nó hỏi là giá trị lớn nhất có thể đạt được từ cái biểu thức này là giá trị nào", "qhđ", {"QHĐ"}),
 "b9:247 câu c cấu trúc con tối ưu": ("câu C nó nói là hãy phân tích cái đặc trưng optimal substructure", "qhđ", {"QHĐ"}),
 "b9:287 câu d phương trình QHĐ": ("Câu D. Viết phương trình quy hoạch động", "qhđ", {"QHĐ"}),
 "b9:325 nhân chuỗi ma trận": ("nhân chuỗi ma trận. Các ma trận mình gọi tên nó là A1, A2 cho đến An. yêu cầu là xác định cái thứ tự nhân các ma trận sao cho số phép nhân sử dụng là ít nhất", "qhđ", {"QHĐ"}),
 "b9:443 điền bảng m và S": ("Cho em một cái chuỗi ma trận, kích thước của từng ma trận. Yêu cầu điền giá trị vào trong cái bảng m và cái bảng S", "qhđ", {"QHĐ"}),
 "b9:177 top-down C(3,2)": ("tính tổ hợp chập 2 của 3 theo cách top down memorization. Cái ô nào mình điền giá trị vào trước", "qhđ", {"QHĐ"}),
 "b7:189 tách chuỗi đối xứng": ("Cho một cái chuỗi S AAB. tìm những cái cách có thể chia cái chuỗi này ra thành những cái chuỗi con đối xứng", "quay lui", {"Quay lui"}),
 "b6:309 đường đi đồ thị": ("tìm đường đi từ một đỉnh nào đó tới một đỉnh nào đó. đề nó nói là hãy tìm hết tất cả những con đường có thể có", "quay lui", {"Quay lui"}),
 "b7:43 cây khung": ("trong cái đồ thị nó có một cái thành phần gọi là cây khung. Đề nó hỏi là tìm cây khung tối tiểu", "quay lui", {"Quay lui"}),
 "b7:421 hoán vị giảm để trị": ("liệt kê tất cả các hoán vị của một cái dãy số, một tập hợp, một cái mảng A. Bài này hồi xưa có giải rồi đó nhưng mà chúng ta giải bằng quay lui còn giờ giải bằng kiểu khác", "quay lui|giảm để trị|2 chiến lược", {"Quay lui", "Giảm để trị", "2 chiến lược"}),
 "b8:53 phát biểu bài toán": ("Input là cái gì? Output là cái gì? và cái mã giả của cái thuật toán để giải quyết cái yêu cầu là cái gì. Câu này đã từng xuất hiện trong đề thi cuối kỳ rồi", "phân tích bài toán|mã giả", {"Phân tích bài toán", "Mô hình hóa"}),
}
k_ok = 0; k_miss = []; k_fp = {}
for k, (txt, want, allow) in KCASES.items():
    ds = dests(txt); ok = any(re.search(want, d) for d in ds); k_ok += ok
    if not ok: k_miss.append(k)
    fp = fams(txt) - allow
    if fp: k_fp[k] = sorted(fp)
print(f"K (held-out sạch, lời cô đọc đề cũ): {k_ok}/{len(KCASES)} tới đúng đích. Hụt: {k_miss}. Khớp nhầm: {k_fp}")
check("K", "đã chạy held-out sạch K (chỉ báo cáo)", len(KCASES) == 17)

# ---------------- báo cáo ----------------
groups = {}
for g, name, ok, det in results:
    groups.setdefault(g, [0, 0]); groups[g][0 if ok else 1] += 1
    if not ok: print(f"FAIL [{g}] {name} {det}")
print("tổng:", {g: f"{p} pass / {f} fail" for g, (p, f) in sorted(groups.items())})
sys.exit(0 if all(r[2] for r in results) else 1)
