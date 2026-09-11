import sys

s_str = ""
L = 0
S = [0] * 105
is_pal = []

def xuat_loi_giai(k):
    result = []
    start = 0
    for idx in range(1, k + 1):
        end = S[idx]
        result.append(s_str[start : end + 1])
        start = end + 1
    sys.stdout.write(" ".join(result) + "\n")

def Try(i, start_idx):
    global L, s_str, S, is_pal
    
    for j in range(start_idx, L):
        if is_pal[start_idx][j]:
            S[i] = j
            if j + 1 < L:
                Try(i + 1, j + 1)
            else:
                xuat_loi_giai(i)

if __name__ == '__main__':
    input_data = sys.stdin.read().split()
    if input_data:
        s_str = input_data[0]
        L = len(s_str)
        is_pal = [[False] * L for _ in range(L)]
        for i in range(L - 1, -1, -1):
            for j in range(i, L):
                if s_str[i] == s_str[j] and (j - i <= 2 or is_pal[i + 1][j - 1]):
                    is_pal[i][j] = True
                    
        Try(1, 0)
