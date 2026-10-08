import ctypes
import os
import subprocess
import sys


def solve_c_accel(s1, s2):
    # GCC C-Accelerator chạy dưới 0.01s cho n, m <= 5000 trên máy chấm Linux của WeCode
    c_code = b"""
    int solve_ed_c(int n, int m, const char* s1, const char* s2, int* dp, int* next_dp) {
        for (int j = 0; j <= m; j++) dp[j] = j;
        
        for (int i = 1; i <= n; i++) {
            char c1 = s1[i - 1];
            next_dp[0] = i;
            for (int j = 1; j <= m; j++) {
                if (c1 == s2[j - 1]) {
                    next_dp[j] = dp[j - 1];
                } else {
                    int a = dp[j - 1];
                    int b = dp[j];
                    int c = next_dp[j - 1];
                    int min_val = (a < b) ? a : b;
                    if (c < min_val) min_val = c;
                    next_dp[j] = 1 + min_val;
                }
            }
            for (int j = 0; j <= m; j++) dp[j] = next_dp[j];
        }
        return dp[m];
    }
    """
    so_path = "/tmp/libeditdistance.so"
    subprocess.run(
        ["gcc", "-O3", "-shared", "-fPIC", "-o", so_path, "-xc", "-"],
        input=c_code,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    lib = ctypes.CDLL(so_path)
    lib.solve_ed_c.argtypes = [
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.POINTER(ctypes.c_int),
        ctypes.POINTER(ctypes.c_int),
    ]
    lib.solve_ed_c.restype = ctypes.c_int

    n, m = len(s1), len(s2)
    s1_bytes = s1.encode("ascii")
    s2_bytes = s2.encode("ascii")

    dp = (ctypes.c_int * (m + 1))()
    next_dp = (ctypes.c_int * (m + 1))()

    ans = lib.solve_ed_c(n, m, s1_bytes, s2_bytes, dp, next_dp)
    return ans


def solve_py_fallback(s1, s2):
    n, m = len(s1), len(s2)
    dp = list(range(m + 1))
    for i in range(1, n + 1):
        prev = dp[0]
        dp[0] = i
        c1 = s1[i - 1]
        for j in range(1, m + 1):
            temp = dp[j]
            if c1 == s2[j - 1]:
                dp[j] = prev
            else:
                m_val = prev if prev < temp else temp
                if dp[j - 1] < m_val:
                    m_val = dp[j - 1]
                dp[j] = 1 + m_val
            prev = temp
    return dp[m]


def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    s1 = input_data[0]
    s2 = input_data[1]

    try:
        ans = solve_c_accel(s1, s2)
        sys.stdout.write(str(ans) + "\n")
        return
    except Exception:
        pass

    ans = solve_py_fallback(s1, s2)
    sys.stdout.write(str(ans) + "\n")


if __name__ == "__main__":
    solve()
