import sys


def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    q = int(input_data[1])
    a = [int(x) for x in input_data[2 : 2 + n]]

    prefix_sum = [0] * (n + 1)
    for i in range(1, n + 1):
        prefix_sum[i] = prefix_sum[i - 1] + a[i - 1]

    idx = 2 + n
    results = []
    for _ in range(q):
        u = int(input_data[idx])
        v = int(input_data[idx + 1])
        idx += 2
        results.append(str(prefix_sum[v] - prefix_sum[u - 1]))

    sys.stdout.write("\n".join(results) + "\n")


if __name__ == "__main__":
    solve()
