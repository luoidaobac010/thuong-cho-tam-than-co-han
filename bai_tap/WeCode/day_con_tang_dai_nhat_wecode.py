from bisect import bisect_left
import sys


def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    a = [int(x) for x in input_data[1 : 1 + n]]

    tails = []
    for x in a:
        idx = bisect_left(tails, x)
        if idx == len(tails):
            tails.append(x)
        else:
            tails[idx] = x

    sys.stdout.write(str(len(tails)) + "\n")


if __name__ == "__main__":
    solve()
