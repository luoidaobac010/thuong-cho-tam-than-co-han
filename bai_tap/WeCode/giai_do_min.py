def solve():
    print("Nhập N và M (cách nhau bởi khoảng trắng):")
    try:
        first_line = input().strip().split()
        if not first_line:
            return
        N, M = map(int, first_line)
    except Exception:
        print("Đầu vào không hợp lệ.")
        return

    print(f"Nhập ma trận {N}x{M} (mỗi dòng {M} số, có thể copy/paste toàn bộ):")
    A = []
    for _ in range(N):
        A.append(list(map(int, input().strip().split())))

    # Ma trận kết quả B
    B = [[0] * M for _ in range(N)]
    
    # current_sum[r][c]: Số quả mìn ĐÃ ĐẶT xung quanh ô (r, c)
    current_sum = [[0] * M for _ in range(N)]
    
    # unassigned[r][c]: Số ô kề CHƯA ĐƯỢC ĐIỀN của ô (r, c)
    unassigned = [[0] * M for _ in range(N)]

    # Bước 1: Tính số lượng ô kề ban đầu cho mỗi ô
    for r in range(N):
        for c in range(M):
            count = 0
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if 0 <= r + dr < N and 0 <= c + dc < M:
                    count += 1
            unassigned[r][c] = count

    # Kiểm tra tính hợp lệ ban đầu (Nếu 1 ô yêu cầu số mìn > số ô kề xung quanh nó)
    for r in range(N):
        for c in range(M):
            if unassigned[r][c] < A[r][c]:
                print("Không có đáp án (impossible)!")
                return

    def backtrack(i):
        # Base case: Đã duyệt xong toàn bộ ma trận
        if i == N * M:
            return True

        r = i // M
        c = i % M

        # Thử đặt 0 (không mìn) và 1 (có mìn)
        for val in (0, 1):
            B[r][c] = val
            valid = True
            updated = []

            # QUAN TRỌNG: Ô (r,c) thay đổi sẽ chỉ tác động đến các Ô KỀ của nó.
            # Do đó ta cập nhật và kiểm tra điều kiện của các ô kề.
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < N and 0 <= nc < M:
                    if val == 1:
                        current_sum[nr][nc] += 1
                    unassigned[nr][nc] -= 1
                    updated.append((nr, nc))

                    # Pruning (Cắt tỉa nhánh) 1: 
                    # Nếu số mìn xung quanh ô (nr,nc) đã vượt quá yêu cầu -> SAI
                    if current_sum[nr][nc] > A[nr][nc]:
                        valid = False
                        break
                        
                    # Pruning (Cắt tỉa nhánh) 2: 
                    # Nếu số mìn hiện có + số ô trống còn lại < yêu cầu -> KHÔNG ĐỦ MÌN -> SAI
                    if current_sum[nr][nc] + unassigned[nr][nc] < A[nr][nc]:
                        valid = False
                        break

            # Nếu thỏa mãn cả 2 điều kiện cắt tỉa, ta mới đi tiếp
            if valid:
                if backtrack(i + 1):
                    return True

            # Quay lui (backtrack): Phục hồi lại trạng thái cũ
            for nr, nc in updated:
                if val == 1:
                    current_sum[nr][nc] -= 1
                unassigned[nr][nc] += 1

        return False

    if backtrack(0):
        print("\n--- KẾT QUẢ DÒ MÌN ---")
        for row in B:
            print(" ".join(map(str, row)))
    else:
        print("Không có đáp án thỏa mãn!")

if __name__ == '__main__':
    solve()
