def solve():
    print("Nhập ma trận Sudoku 9x9 (các số cách nhau bởi khoảng trắng, dùng chữ 'X' cho ô trống).")
    print("Gợi ý: Bạn có thể copy toàn bộ 9 dòng đề bài và paste thẳng vào đây, hoặc gõ tay từng dòng.")
    print("Nhập 'q' rồi nhấn Enter nếu bạn muốn thoát ngang.")
    print("-" * 60)
    
    # Đọc dữ liệu đầu vào có kiểm tra lỗi (Robust Input)
    grid = []
    try:
        while len(grid) < 9:
            # Hiển thị dấu nhắc để người dùng biết đang ở dòng nào
            line = input(f"Dòng {len(grid) + 1}/9: ").strip()
            
            if line.lower() == 'q':
                print("Đã thoát chương trình.")
                return
            if not line:
                continue
                
            parts = line.split()
            
            # Bắt lỗi nếu nhập không đủ/dư cột
            if len(parts) != 9:
                print(f"[!] Lỗi: Bạn vừa nhập {len(parts)} phần tử. Một hàng Sudoku bắt buộc phải có đúng 9 phần tử.")
                print("[!] Vui lòng nhập lại dòng này.")
                continue
            
            # Chuẩn hóa nếu người dùng lỡ gõ 'x' thường thì tự động chuyển thành 'X' hoa
            parts = ['X' if p.lower() == 'x' else p for p in parts]
            grid.append(parts)
            
    except EOFError:
        pass
    except KeyboardInterrupt:
        print("\nĐã thoát chương trình.")
        return
        
    if len(grid) < 9:
        return
        
    print("\nĐang giải Sudoku, vui lòng đợi...")
    
    # Tìm tất cả các ô trống 'X'
    empty_cells = []
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 'X':
                empty_cells.append((r, c))
                
    N = len(empty_cells)
    
    def is_valid(r, c, val):
        """Kiểm tra xem số val có thể điền vào ô (r, c) hay không"""
        # Kiểm tra hàng và cột
        for x in range(9):
            if grid[r][x] == val: return False
            if grid[x][c] == val: return False
        
        # Kiểm tra khối 3x3
        start_row, start_col = 3 * (r // 3), 3 * (c // 3)
        for i in range(3):
            for j in range(3):
                if grid[start_row + i][start_col + j] == val:
                    return False
        return True

    def backtrack(i):
        if i == N:
            return True
            
        r, c = empty_cells[i]
        
        for j in range(1, 10):
            val = str(j)
            
            if is_valid(r, c, val):
                grid[r][c] = val
                
                if backtrack(i + 1):
                    return True
                    
                grid[r][c] = 'X'
                
        return False

    print("\n--- KẾT QUẢ GIẢI SUDOKU ---")
    if backtrack(0):
        for row in grid:
            print(" ".join(row))
    else:
        if N == 0:
            for row in grid:
                print(" ".join(row))
        else:
            print("Bó tay, không tìm thấy lời giải hợp lệ nào!")

if __name__ == '__main__':
    solve()
