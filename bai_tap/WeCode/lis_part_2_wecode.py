from bisect import bisect_left
import sys


def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    a = [int(x) for x in input_data[1 : 1 + n]]

    tails_val = []
    tails_idx = []
    parent = [-1] * n

    for i, x in enumerate(a):
        idx = bisect_left(tails_val, x)
        if idx > 0:
            parent[i] = tails_idx[idx - 1]

        if idx == len(tails_val):
            tails_val.append(x)
            tails_idx.append(i)
        else:
            tails_val[idx] = x
            tails_idx[idx] = i

    k = len(tails_val)
    lis = []
    curr = tails_idx[-1]
    while curr != -1:
        lis.append(a[curr])
        curr = parent[curr]

    lis.reverse()

    sys.stdout.write(f"{k}\n")
    sys.stdout.write(" ".join(map(str, lis)) + "\n")


if __name__ == "__main__":
    solve()
