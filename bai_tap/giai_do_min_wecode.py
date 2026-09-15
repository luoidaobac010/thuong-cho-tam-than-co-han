import sys

sys.setrecursionlimit(10**6)

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
        
    N = int(input_data[0])
    M = int(input_data[1])
    
    if N == 0 or M == 0:
        return
        
    A = []
    idx = 2
    for _ in range(N):
        row = []
        for _ in range(M):
            row.append(int(input_data[idx]))
            idx += 1
        A.append(row)
        
    B = [[0] * M for _ in range(N)]
    found = False
    
    def check_and_fill():
        for r in range(1, N):
            for c in range(M):
                val = A[r-1][c]
                if r >= 2:
                    val -= B[r-2][c]
                if c > 0:
                    val -= B[r-1][c-1]
                if c < M - 1:
                    val -= B[r-1][c+1]
                if val < 0 or val > 1:
                    return False
                B[r][c] = val
                
        for c in range(M):
            sum_val = 0
            if N >= 2:
                sum_val += B[N-2][c]
            if c > 0:
                sum_val += B[N-1][c-1]
            if c < M - 1:
                sum_val += B[N-1][c+1]
            if sum_val != A[N-1][c]:
                return False
        return True

    def backtrack(c):
        nonlocal found
        if found:
            return
            
        if c == M:
            if check_and_fill():
                found = True
            return
            
        lo, hi = 0, 1
        
        if c >= 1:
            base = A[0][c-1]
            if c >= 2:
                base -= B[0][c-2]
                
            if N == 1:
                if base < 0 or base > 1:
                    return
                lo = hi = base
            else:
                lo = max(0, base - 1)
                hi = min(1, base)
                if lo > hi:
                    return
                    
        for val in range(lo, hi + 1):
            B[0][c] = val
            ok = True
            
            max_r = min(c, N - 1)
            for r in range(1, max_r + 1):
                col = c - r
                rv = A[r-1][col]
                if r >= 2:
                    rv -= B[r-2][col]
                if col > 0:
                    rv -= B[r-1][col-1]
                rv -= B[r-1][col+1]
                
                if rv < 0 or rv > 1:
                    ok = False
                    break
                else:
                    B[r][col] = rv
                    
            if not ok:
                continue
                
            backtrack(c + 1)
            if found:
                return

    backtrack(0)
    
    if found:
        for row in B:
            sys.stdout.write(" ".join(map(str, row)) + "\n")

if __name__ == '__main__':
    solve()
