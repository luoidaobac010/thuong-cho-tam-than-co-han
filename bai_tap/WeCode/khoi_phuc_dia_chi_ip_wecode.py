import sys

s_str = ""
L = 0
S = [0] * 5

def is_valid_part(start, end):
    length = end - start + 1
    if length <= 0 or length > 3: 
        return False
    if length > 1 and s_str[start] == '0': 
        return False
    
    val = 0
    for idx in range(start, end + 1):
        val = val * 10 + int(s_str[idx])
    return val <= 255

def xuat_loi_giai():
    part1 = s_str[0 : S[1]+1]
    part2 = s_str[S[1]+1 : S[2]+1]
    part3 = s_str[S[2]+1 : S[3]+1]
    part4 = s_str[S[3]+1 : S[4]+1]
    sys.stdout.write(f"{part1}.{part2}.{part3}.{part4}\n")

def Try(i, start_idx):
    global L, s_str, S
    
    if L - start_idx > (4 - i + 1) * 3:
        return
    if L - start_idx < (4 - i + 1):
        return

    for j in range(start_idx, min(start_idx + 3, L)):
        if is_valid_part(start_idx, j):
            S[i] = j
            if i < 4:
                Try(i + 1, j + 1)
            else:
                if j == L - 1:
                    xuat_loi_giai()

if __name__ == '__main__':
    input_data = sys.stdin.read().split()
    if input_data:
        s_str = input_data[0]
        L = len(s_str)
        if 4 <= L <= 12:
            Try(1, 0)
