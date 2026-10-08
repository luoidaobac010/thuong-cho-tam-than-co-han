from bisect import bisect_left
import sys


def solve():
    # Đọc dữ liệu đầu vào (Fast I/O)
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    a = [int(x) for x in input_data[1 : 1 + n]]

    # tails_val: giá trị phần tử cuối nhỏ nhất của dãy tăng
    # tails_idx: chỉ số (trong mảng a) của phần tử đó
    tails_val = []
    tails_idx = []

    # parent[i]: chỉ số của phần tử đứng ngay trước a[i] trong dãy con tăng tối ưu
    parent = [-1] * n

    for i, x in enumerate(a):
        # Tìm vị trí thích hợp bằng tìm kiếm nhị phân
        idx = bisect_left(tails_val, x)

        # Lưu vết: phần tử đứng trước x chính là phần tử ở vị trí idx - 1 trong tails
        if idx > 0:
            parent[i] = tails_idx[idx - 1]

        if idx == len(tails_val):
            tails_val.append(x)
            tails_idx.append(i)
        else:
            tails_val[idx] = x
            tails_idx[idx] = i

    k = len(tails_val)

    # Truy vết lại dãy con tăng từ phần tử cuối cùng
    lis = []
    curr = tails_idx[-1]
    while curr != -1:
        lis.append(a[curr])
        curr = parent[curr]

    # Đảo ngược lại do truy vết từ đuôi lên đầu
    lis.reverse()

    # In kết quả
    sys.stdout.write(f"{k}\n")
    sys.stdout.write(" ".join(map(str, lis)) + "\n")


if __name__ == "__main__":
    solve()
