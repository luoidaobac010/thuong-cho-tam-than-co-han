from bisect import bisect_left
import sys


def solve():
    # Đọc dữ liệu đầu vào (Fast I/O)
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    a = [int(x) for x in input_data[1 : 1 + n]]

    # tails[i] lưu giá trị phần tử kết thúc nhỏ nhất của dãy con tăng độ dài i + 1
    tails = []

    for x in a:
        # Tìm vị trí đầu tiên trong tails có giá trị >= x (dãy tăng nghiêm ngặt)
        idx = bisect_left(tails, x)

        if idx == len(tails):
            # Mở rộng dãy tăng
            tails.append(x)
        else:
            # Tối ưu hóa giá trị kết thúc nhỏ hơn
            tails[idx] = x

    # Độ dài của tails chính là độ dài LIS
    sys.stdout.write(str(len(tails)) + "\n")


if __name__ == "__main__":
    solve()
