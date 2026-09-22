import sys

lines = sys.stdin.read().split()
if not lines:
    sys.exit(0)
    
n = int(lines[0])
w = [0] * (n + 1)
for i in range(1, n + 1):
    w[i] = int(lines[i])
I_target = float(lines[n+1])

min_T = round(I_target * 400) - 20
max_T = round(I_target * 400) + 19

rem_w = [0] * (n + 1)
for i in range(1, n + 1):
    rem_w[i] = sum(w[k] for k in range(i + 1, n + 1))

S = [0] * (n + 1)
current_T = 0

def format_score(v):
    s = v * 0.25
    if s.is_integer():
        return str(int(s))
    return str(s)

def xuat_loi_giai():
    print(" ".join(format_score(S[idx]) for idx in range(1, n + 1)))

def Try(i):
    global current_T
    
    rem_max = rem_w[i] * 40
    rem_min = rem_w[i] * 1
    
    for j in range(1, 41):
        new_T = current_T + j * w[i]
        if min_T <= new_T + rem_max and new_T + rem_min <= max_T:
            S[i] = j
            current_T = new_T
            
            if i < n:
                Try(i + 1)
            else:
                xuat_loi_giai()
                
            current_T -= j * w[i]

if __name__ == '__main__':
    Try(1)
