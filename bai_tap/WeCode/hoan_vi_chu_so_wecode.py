n_str = input().strip()
L = len(n_str)
A = [''] + sorted(list(n_str), reverse=True)

S = [0] * 15
used = [False] * 15

def xuat_loi_giai():
    print("".join(A[S[idx]] for idx in range(1, L + 1)))

def Try(i):
    global L, S, used
    
    for j in range(1, L + 1):
        if not used[j] and (j == 1 or A[j] != A[j-1] or used[j-1]):
            S[i] = j
            used[j] = True
            
            if i < L:
                Try(i + 1)
            else:
                xuat_loi_giai()
                
            used[j] = False

if __name__ == '__main__':
    for j in range(1, L + 1):
        used[j] = False
    Try(1)
