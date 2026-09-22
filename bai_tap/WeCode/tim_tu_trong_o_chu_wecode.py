import sys

word = ""
grid = []
rows = 0
cols = 0
word_len = 0
used = []
found = False

directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

def Try(i, r, c):
    global found
    if found: return
    
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and not used[nr][nc]:
            if grid[nr][nc] == word[i]:
                used[nr][nc] = True
                if i + 1 < word_len:
                    Try(i + 1, nr, nc)
                else:
                    found = True
                used[nr][nc] = False

if __name__ == '__main__':
    try:
        word = input().strip()
        while True:
            line = input().strip()
            if line == '.':
                break
            if line:
                grid.append(list(line))
    except EOFError:
        pass
        
    word_len = len(word)
    rows = len(grid)
    if rows > 0:
        cols = len(grid[0])
    
    if word_len == 0 or rows == 0 or cols == 0:
        print("false")
        sys.exit()
        
    used = [[False] * cols for _ in range(rows)]
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == word[0]:
                if word_len == 1:
                    found = True
                    break
                used[r][c] = True
                Try(1, r, c)
                used[r][c] = False
                if found:
                    break
        if found:
            break
            
    if found:
        print("true")
    else:
        print("false")
