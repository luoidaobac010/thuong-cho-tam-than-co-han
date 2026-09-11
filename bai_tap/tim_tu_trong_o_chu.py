def solve():
    """
    Giải quyết bài toán Tìm từ trong ô chữ (Word Search)
    Cho phép di chuyển 8 hướng: ngang, dọc, 2 đường chéo.
    """
    try:
        word = input().strip()
        grid = []
        while True:
            line = input().strip()
            if line == '.':
                break
            if line:
                grid.append(list(line))
    except EOFError:
        pass
        
    if not word or not grid:
        print("false")
        return
        
    rows = len(grid)
    cols = len(grid[0])
    word_len = len(word)
    
    # Ma trận đánh dấu các ô đã đi qua để không dùng lại
    used = [[False] * cols for _ in range(rows)]
    
    # 8 hướng di chuyển: Lên, Xuống, Trái, Phải, và 4 hướng chéo
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]
                  
    def backtrack(index, r, c):
        # Base case: đã tìm đủ các ký tự của từ
        if index == word_len:
            return True
            
        # Vòng lặp duyệt các khả năng (8 hướng lân cận)
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            # Kiểm tra ô mới: nằm trong bảng, chưa đi qua, và đúng ký tự tiếp theo
            if 0 <= nr < rows and 0 <= nc < cols and not used[nr][nc]:
                if grid[nr][nc] == word[index]:
                    
                    # Ghi nhận trạng thái: đánh dấu đã đi qua
                    used[nr][nc] = True
                    
                    # Đệ quy tìm ký tự tiếp theo
                    if backtrack(index + 1, nr, nc):
                        return True
                        
                    # Trả lại trạng thái: bỏ đánh dấu để thử hướng khác
                    used[nr][nc] = False
                    
        return False

    # Quét toàn bộ bảng để tìm điểm xuất phát (ký tự đầu tiên của từ)
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == word[0]:
                # Xử lý ngoại lệ từ chỉ có 1 ký tự
                if word_len == 1:
                    print("true")
                    return
                
                # Ghi nhận ô bắt đầu
                used[r][c] = True
                
                # Bắt đầu quay lui từ ký tự thứ 2 (index = 1)
                if backtrack(1, r, c):
                    print("true")
                    return
                    
                # Bỏ đánh dấu nếu từ điểm xuất phát này không tìm ra từ
                used[r][c] = False
                
    print("false")

if __name__ == "__main__":
    solve()
