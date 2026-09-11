import sys

grid = []
empty_cells = []
N = 0
found = False

def is_valid(r, c, val):
    for x in range(9):
        if grid[r][x] == val: return False
        if grid[x][c] == val: return False
    
    sr, sc = (r // 3) * 3, (c // 3) * 3
    for i in range(3):
        for j in range(3):
            if grid[sr + i][sc + j] == val:
                return False
    return True

def xuat_loi_giai():
    for row in grid:
        sys.stdout.write(" ".join(row) + "\n")

def Try(i):
    global found
    if found: return
    
    r, c = empty_cells[i]
    
    for j in range(1, 10):
        val = str(j)
        if is_valid(r, c, val):
            grid[r][c] = val
            
            if i + 1 < N:
                Try(i + 1)
            else:
                xuat_loi_giai()
                found = True
                
            grid[r][c] = 'X'

if __name__ == '__main__':
    input_text = sys.stdin.read().splitlines()
    for line in input_text:
        line = line.strip()
        if line:
            parts = line.split()
            # Chuẩn hóa 'x' thường thành 'X' hoa đề phòng test case lừa
            parts = ['X' if p.lower() == 'x' else p for p in parts]
            grid.append(parts)
            if len(grid) == 9:
                break
            
    if len(grid) == 9:
        for r in range(9):
            for c in range(9):
                if grid[r][c] == 'X':
                    empty_cells.append((r, c))
                    
        N = len(empty_cells)
        if N > 0:
            Try(0)
        else:
            xuat_loi_giai()
