S = [0] * 15
used = [False] * 15
n = 0

def xuat_loi_giai():
    print(" ".join(str(S[idx]) for idx in range(1, n + 1)))

def Try(i):
    global n, S, used
    
    for j in range(1, n + 1):
        if not used[j]:
            S[i] = j
            used[j] = True
            
            if i < n:
                Try(i + 1)
            else:
                xuat_loi_giai()
                
            used[j] = False

if __name__ == '__main__':
    n = int(input().strip())
    for j in range(1, n + 1):
        used[j] = False
    Try(1)
