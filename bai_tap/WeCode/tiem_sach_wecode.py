import array
import ctypes
import os
import subprocess
import sys


def solve_c_accel(n, x, h, s):
    c_code = b"""
    void solve_c(int n, int x, int* h, int* s, int* dp) {
        for (int i = 0; i < n; i++) {
            int p = h[i];
            int pg = s[i];
            if (p > x) continue;
            for (int j = x; j >= p; j--) {
                int v = dp[j - p] + pg;
                if (v > dp[j]) dp[j] = v;
            }
        }
        for (int j = 1; j <= x; j++) {
            if (dp[j - 1] > dp[j]) dp[j] = dp[j - 1];
        }
    }
    """
    so_path = "/tmp/libknapsack.so"
    subprocess.run(
        ["gcc", "-O3", "-shared", "-fPIC", "-o", so_path, "-xc", "-"],
        input=c_code,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    lib = ctypes.CDLL(so_path)
    lib.solve_c.argtypes = [
        ctypes.c_int,
        ctypes.c_int,
        ctypes.POINTER(ctypes.c_int),
        ctypes.POINTER(ctypes.c_int),
        ctypes.POINTER(ctypes.c_int),
    ]

    h_arr = (ctypes.c_int * n)(*h)
    s_arr = (ctypes.c_int * n)(*s)
    dp_arr = (ctypes.c_int * (x + 1))()

    lib.solve_c(n, x, h_arr, s_arr, dp_arr)
    return dp_arr[x]


def solve_py_fallback(n, x, h, s):
    dp = [0] * (x + 1)
    reach = 0
    for p, pg in zip(h, s):
        if p > x:
            continue
        reach = min(x, reach + p)
        for j in range(reach, p - 1, -1):
            v = dp[j - p] + pg
            if v > dp[j]:
                dp[j] = v

    for j in range(1, x + 1):
        if dp[j - 1] > dp[j]:
            dp[j] = dp[j - 1]
    return dp[x]


def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    x = int(input_data[1])

    h = [int(v) for v in input_data[2 : 2 + n]]
    s = [int(v) for v in input_data[2 + n : 2 + 2 * n]]

    total_cost = sum(h)
    if total_cost <= x:
        sys.stdout.write(str(sum(s)) + "\n")
        return

    x = min(x, total_cost)

    try:
        ans = solve_c_accel(n, x, h, s)
        sys.stdout.write(str(ans) + "\n")
        return
    except Exception:
        pass

    ans = solve_py_fallback(n, x, h, s)
    sys.stdout.write(str(ans) + "\n")


if __name__ == "__main__":
    solve()
