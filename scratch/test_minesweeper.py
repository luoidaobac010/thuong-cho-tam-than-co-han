import sys
import time

def solve_minesweeper(A):
    N = len(A)
    if N == 0: return None
    M = len(A[0])
    
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
            if unassigned[r][c] < A[r][c]:
                return None
                
    found = False
    ans = None
    
    # We will use iterative backtracking
    stack = []
    # stack stores (i, val_to_try, state_of_updates)
    
    def get_valid_val(i, start_val=0):
        r = i // M
        c = i % M
        for val in range(start_val, 2):
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
                    
                    if current_sum[nr][nc] > A[nr][nc] or current_sum[nr][nc] + unassigned[nr][nc] < A[nr][nc]:
                        valid = False
                        break
            if valid:
                return val, updated
                
            # Restore if invalid
            for nr, nc in updated:
                if val == 1:
                    current_sum[nr][nc] -= 1
                unassigned[nr][nc] += 1
        return None, []

    i = 0
    val, updated = get_valid_val(i, 0)
    if val is not None:
        stack.append((i, val, updated))
        i += 1
    
    while stack:
        if i == N * M:
            return [row[:] for row in B]
            
        val, updated = get_valid_val(i, 0)
        if val is not None:
            stack.append((i, val, updated))
            i += 1
        else:
            # Backtrack
            while stack:
                prev_i, prev_val, prev_updated = stack.pop()
                # Restore
                for nr, nc in prev_updated:
                    if prev_val == 1:
                        current_sum[nr][nc] -= 1
                    unassigned[nr][nc] += 1
                i = prev_i
                
                # Try next val
                next_val, next_updated = get_valid_val(i, prev_val + 1)
                if next_val is not None:
                    stack.append((i, next_val, next_updated))
                    i += 1
                    break

    return None

def test():
    import random
    N, M = 30, 30
    B_true = [[random.choice([0, 1]) for _ in range(M)] for _ in range(N)]
    A = [[0] * M for _ in range(N)]
    for r in range(N):
        for c in range(M):
            count = 0
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if 0 <= r + dr < N and 0 <= c + dc < M:
                    count += B_true[r + dr][c + dc]
            A[r][c] = count
            
    print(f"Testing {N}x{M}...")
    t0 = time.time()
    res = solve_minesweeper(A)
    print("Found solution:" , res is not None)
    if res is not None:
        valid = True
        for r in range(N):
            for c in range(M):
                count = 0
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    if 0 <= r + dr < N and 0 <= c + dc < M:
                        count += res[r + dr][c + dc]
                if count != A[r][c]:
                    valid = False
        print("Valid solution:", valid)
    print("Time:", time.time() - t0)

if __name__ == '__main__':
    test()
