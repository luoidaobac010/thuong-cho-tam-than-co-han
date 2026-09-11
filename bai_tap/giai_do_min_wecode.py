import sys

N, M = 0, 0
A = []
B = []
current_sum = []
unassigned = []
found = False

def xuat_loi_giai():
    for row in B:
        sys.stdout.write(" ".join(map(str, row)) + "\n")

def Try(i):
    global found
    if found: return
    
    r = i // M
    c = i % M
    
    for val in (0, 1):
        B[r][c] = val
        valid = True
        updated = []
        
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < N and 0 <= nc < M:
                if val == 1:
                    current_sum[nr][nc] += 1
                unassigned[nr][nc] -= 1
                updated.append((nr, nc))
                
                if current_sum[nr][nc] > A[nr][nc]:
                    valid = False
                    break
                if current_sum[nr][nc] + unassigned[nr][nc] < A[nr][nc]:
                    valid = False
                    break
                    
        if valid:
            if i + 1 < N * M:
                Try(i + 1)
            else:
                found = True
                xuat_loi_giai()
                
        for nr, nc in updated:
            if val == 1:
                current_sum[nr][nc] -= 1
            unassigned[nr][nc] += 1

if __name__ == '__main__':
    input_data = sys.stdin.read().split()
    if not input_data:
        sys.exit()
        
    N = int(input_data[0])
    M = int(input_data[1])
    
    idx = 2
    for _ in range(N):
        row = []
        for _ in range(M):
            row.append(int(input_data[idx]))
            idx += 1
        A.append(row)
        
    B = [[0] * M for _ in range(N)]
    current_sum = [[0] * M for _ in range(N)]
    unassigned = [[0] * M for _ in range(N)]
    
    for r in range(N):
        for c in range(M):
            count = 0
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if 0 <= r + dr < N and 0 <= c + dc < M:
                    count += 1
            unassigned[r][c] = count
            
    possible = True
    for r in range(N):
        for c in range(M):
            if unassigned[r][c] < A[r][c]:
                possible = False
                break
        if not possible:
            break
            
    if possible:
        Try(0)
