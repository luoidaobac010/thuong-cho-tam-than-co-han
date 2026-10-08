import sys


def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    grid = input_data[1 : 1 + n]

    if grid[0][0] == "*" or grid[n - 1][n - 1] == "*":
        sys.stdout.write("0\n")
        return

    MOD = 10**9 + 7
    dp = [0] * n
    dp[0] = 1

    for r in range(n):
        row = grid[r]
        if row[0] == "*":
            dp[0] = 0

        for c in range(1, n):
            if row[c] == "*":
                dp[c] = 0
            else:
                dp[c] = (dp[c] + dp[c - 1]) % MOD

    sys.stdout.write(str(dp[n - 1]) + "\n")


if __name__ == "__main__":
    solve()
