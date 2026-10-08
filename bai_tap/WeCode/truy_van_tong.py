import sys


def solve():
    # Đọc toàn bộ dữ liệu đầu vào (Fast I/O)
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    q = int(input_data[1])

    # n phần tử của mảng A
    a = [int(x) for x in input_data[2 : 2 + n]]

    # Xây dựng mảng cộng dồn prefix_sum (1-indexed)
    # prefix_sum[i] là tổng của i phần tử đầu tiên
    prefix_sum = [0] * (n + 1)
    for i in range(1, n + 1):
        prefix_sum[i] = prefix_sum[i - 1] + a[i - 1]

    # Xử lý q truy vấn [a, b]
    idx = 2 + n
    results = []
    for _ in range(q):
        u = int(input_data[idx])
        v = int(input_data[idx + 1])
        idx += 2

        # Tổng đoạn [u, v] (1-indexed) = prefix_sum[v] - prefix_sum[u - 1]
        total = prefix_sum[v] - prefix_sum[u - 1]
        results.append(str(total))

    # In kết quả
    sys.stdout.write("\n".join(results) + "\n")


if __name__ == "__main__":
    solve()
