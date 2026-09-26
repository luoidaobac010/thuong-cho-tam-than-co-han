import os
import time
import subprocess
import sys

def watch_and_compile(tex_file):
    print(f"[*] Đang theo dõi file: {tex_file}")
    print("[*] Bấm Ctrl+C để dừng.")

    last_mtime = 0

    while True:
        try:
            current_mtime = os.path.getmtime(tex_file)
            if current_mtime > last_mtime:
                if last_mtime != 0: # Bỏ qua lần chạy đầu tiên
                    print(f"\n[+] Phát hiện file thay đổi lúc {time.strftime('%X')}. Đang biên dịch...")

                    # Gọi pdflatex (yêu cầu máy đã cài TexLive hoặc MacTeX)
                    try:
                        result = subprocess.run(
                            ['pdflatex', '-interaction=nonstopmode', tex_file],
                            capture_output=True,
                            text=True
                        )
                    except FileNotFoundError:
                        print("\n[!!!] LỖI HỆ THỐNG:")
                        print("Không tìm thấy lệnh 'pdflatex' trên máy của bạn!")
                        print("Bạn CHƯA CÀI phần mềm biên dịch LaTeX (MacTeX/TeXLive).")
                        print("Vui lòng cài đặt xong mới có thể tự động build PDF được nhé!")
                        break

                    if result.returncode == 0:
                        print("[+] DONE! Biên dịch thành công ra file PDF.")
                    else:
                        print("[!] LỖI BIÊN DỊCH! Xem chi tiết bên dưới:")
                        # In ra 10 dòng cuối của log lỗi để dễ debug
                        lines = result.stdout.split('\n')
                        for line in lines[-15:]:
                            print("  " + line)

                last_mtime = current_mtime

            time.sleep(1) # Quét mỗi giây

        except KeyboardInterrupt:
            print("\n[!] Đã dừng theo dõi.")
            break
        except FileNotFoundError:
            print(f"[!] Không tìm thấy file {tex_file}. Đang chờ file được tạo...")
            time.sleep(2)

if __name__ == "__main__":
    # Tên file mặc định
    tex_file = "[CS112.2026.TX][HW02] Đỗ Quốc Thắng - 26410111_v9.tex"

    # Nếu truyền tham số từ terminal thì dùng tham số đó
    if len(sys.argv) > 1:
        tex_file = sys.argv[1]

    if not os.path.exists(tex_file):
        print(f"Cảnh báo: File {tex_file} chưa tồn tại trong thư mục hiện tại.")

    watch_and_compile(tex_file)
