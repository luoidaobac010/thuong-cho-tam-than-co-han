from collections import deque
import ctypes
import os
import subprocess
import sys


def solve_c_accel(n, q, buf_it):
    c_code = b"""
    #include <stdlib.h>

    void solve_tree_c(int n, int q, const int* edges_u, const int* edges_v, const int* queries_u, const int* queries_v, int* results) {
        int* head = (int*)calloc(n + 2, sizeof(int));
        int* to = (int*)malloc((2 * n + 4) * sizeof(int));
        int* next = (int*)malloc((2 * n + 4) * sizeof(int));
        int edge_cnt = 0;

        for (int i = 0; i < n - 1; i++) {
            int u = edges_u[i];
            int v = edges_v[i];
            
            edge_cnt++;
            to[edge_cnt] = v;
            next[edge_cnt] = head[u];
            head[u] = edge_cnt;
            
            edge_cnt++;
            to[edge_cnt] = u;
            next[edge_cnt] = head[v];
            head[v] = edge_cnt;
        }

        int* depth = (int*)calloc(n + 1, sizeof(int));
        int* parent = (int*)calloc(n + 1, sizeof(int));
        int* q_arr = (int*)malloc((n + 2) * sizeof(int));
        int q_head = 0, q_tail = 0;

        depth[1] = 0;
        parent[1] = 0;
        q_arr[q_tail++] = 1;

        while (q_head < q_tail) {
            int u = q_arr[q_head++];
            for (int e = head[u]; e != 0; e = next[e]) {
                int v = to[e];
                if (v != parent[u]) {
                    parent[v] = u;
                    depth[v] = depth[u] + 1;
                    q_arr[q_tail++] = v;
                }
            }
        }

        const int LOG = 19;
        int* up = (int*)calloc(LOG * (n + 1), sizeof(int));
        for (int i = 1; i <= n; i++) {
            up[0 * (n + 1) + i] = parent[i];
        }
        for (int k = 1; k < LOG; k++) {
            int* prev = up + (k - 1) * (n + 1);
            int* curr = up + k * (n + 1);
            for (int i = 1; i <= n; i++) {
                curr[i] = prev[prev[i]];
            }
        }

        for (int i = 0; i < q; i++) {
            int u = queries_u[i];
            int v = queries_v[i];
            int orig_u = u, orig_v = v;

            if (depth[u] < depth[v]) {
                int t = u; u = v; v = t;
            }

            int diff = depth[u] - depth[v];
            for (int k = 0; k < LOG; k++) {
                if ((diff >> k) & 1) {
                    u = up[k * (n + 1) + u];
                }
            }

            int lca = u;
            if (u != v) {
                for (int k = LOG - 1; k >= 0; k--) {
                    if (up[k * (n + 1) + u] != up[k * (n + 1) + v]) {
                        u = up[k * (n + 1) + u];
                        v = up[k * (n + 1) + v];
                    }
                }
                lca = up[0 * (n + 1) + u];
            }

            results[i] = depth[orig_u] + depth[orig_v] - 2 * depth[lca];
        }

        free(head); free(to); free(next); free(depth); free(parent); free(q_arr); free(up);
    }
    """
    so_path = "/tmp/libtree_fast.so"
    subprocess.run(
        ["gcc", "-O3", "-shared", "-fPIC", "-o", so_path, "-xc", "-"],
        input=c_code,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    lib = ctypes.CDLL(so_path)
    lib.solve_tree_c.argtypes = [
        ctypes.c_int,
        ctypes.c_int,
        ctypes.POINTER(ctypes.c_int),
        ctypes.POINTER(ctypes.c_int),
        ctypes.POINTER(ctypes.c_int),
        ctypes.POINTER(ctypes.c_int),
        ctypes.POINTER(ctypes.c_int),
    ]

    edges_u = (ctypes.c_int * (n - 1))()
    edges_v = (ctypes.c_int * (n - 1))()
    for i in range(n - 1):
        edges_u[i] = next(buf_it)
        edges_v[i] = next(buf_it)

    queries_u = (ctypes.c_int * q)()
    queries_v = (ctypes.c_int * q)()
    for i in range(q):
        queries_u[i] = next(buf_it)
        queries_v[i] = next(buf_it)

    results = (ctypes.c_int * q)()
    lib.solve_tree_c(n, q, edges_u, edges_v, queries_u, queries_v, results)

    # In kết quả
    sys.stdout.write("\n".join(str(results[i]) for i in range(q)) + "\n")


def solve_py_fallback(n, q, buf_it):
    adj = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u = next(buf_it)
        v = next(buf_it)
        adj[u].append(v)
        adj[v].append(u)

    LOG = 19
    depth = [0] * (n + 1)
    parent = [0] * (n + 1)
    visited = bytearray(n + 1)

    queue = deque([1])
    visited[1] = 1

    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if not visited[v]:
                visited[v] = 1
                depth[v] = depth[u] + 1
                parent[v] = u
                queue.append(v)

    del adj, visited

    up = [parent]
    for k in range(1, LOG):
        prev = up[k - 1]
        curr = [prev[prev[i]] for i in range(n + 1)]
        up.append(curr)

    out = []
    for _ in range(q):
        u = next(buf_it)
        v = next(buf_it)
        orig_u, orig_v = u, v
        if depth[u] < depth[v]:
            u, v = v, u

        diff = depth[u] - depth[v]
        for k in range(LOG):
            if (diff >> k) & 1:
                u = up[k][u]

        if u == v:
            out.append(str(depth[orig_u] + depth[orig_v] - 2 * depth[u]))
            continue

        for k in range(LOG - 1, -1, -1):
            if up[k][u] != up[k][v]:
                u = up[k][u]
                v = up[k][v]

        lca = up[0][u]
        out.append(str(depth[orig_u] + depth[orig_v] - 2 * depth[lca]))

    sys.stdout.write("\n".join(out) + "\n")


def parse_ints(buf):
    val = 0
    in_num = False
    for b in buf:
        if 48 <= b <= 57:
            val = val * 10 + (b - 48)
            in_num = True
        elif in_num:
            yield val
            val = 0
            in_num = False
    if in_num:
        yield val


def solve():
    raw_bytes = sys.stdin.buffer.read()
    if not raw_bytes:
        return

    it = parse_ints(raw_bytes)
    try:
        n = next(it)
        q = next(it)
    except StopIteration:
        return

    try:
        solve_c_accel(n, q, it)
        return
    except Exception:
        pass

    # Nếu fallback sang Python
    it_fall = parse_ints(raw_bytes)
    next(it_fall)
    next(it_fall)
    solve_py_fallback(n, q, it_fall)


if __name__ == "__main__":
    solve()
