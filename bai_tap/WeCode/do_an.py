from bisect import bisect_left
import sys


def solve():
    # Đọc theo từng dòng (readline) để tránh tạo danh sách chuỗi khổng lồ trong RAM
    readline = sys.stdin.readline
    first_line = readline()
    if not first_line:
        return

    n = int(first_line.strip())

    # Nén 3 số (b, a, p) vào 1 số nguyên 64-bit duy nhất để tiết kiệm tối đa bộ nhớ (tránh MLE)
    # Vì a, b, p <= 10^9 < 2^30 nên ta dùng 30-bit cho mỗi trường: (b << 60) | (a << 30) | p
    MASK30 = (1 << 30) - 1
    projects = [0] * n

    for i in range(n):
        parts = readline().split()
        a = int(parts[0])
        b = int(parts[1])
        p = int(parts[2])
        projects[i] = (b << 60) | (a << 30) | p

    # Sắp xếp in-place theo b (vì b nằm ở 60 bit cao nhất)
    projects.sort()

    # Mảng dp lưu số tín chỉ tối đa
    dp = [0] * (n + 1)

    for i in range(1, n + 1):
        val = projects[i - 1]
        a_i = (val >> 30) & MASK30
        p_i = val & MASK30

        # Tìm kiếm nhị phân trực tiếp trên mảng projects với khóa tìm kiếm (a_i << 60)
        k = bisect_left(projects, a_i << 60, 0, i - 1)

        prev = dp[i - 1]
        take = dp[k] + p_i
        dp[i] = prev if prev > take else take

    sys.stdout.write(str(dp[n]) + "\n")


if __name__ == "__main__":
    solve()
