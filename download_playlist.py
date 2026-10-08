import sys
import yt_dlp

def download_playlist(playlist_url, output_path="downloads/%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s"):
    """
    Tải toàn bộ video từ một playlist YouTube.
    
    Args:
        playlist_url (str): Đường dẫn đến playlist YouTube
        output_path (str): Đường dẫn lưu file và định dạng tên file
    """
    ydl_opts = {
        # Định dạng chất lượng video tốt nhất (video + audio)
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        
        # Đường dẫn thư mục lưu trữ (mặc định tạo thư mục theo tên playlist)
        'outtmpl': output_path,
        
        # Bỏ qua các video bị lỗi (ví dụ: bị ẩn hoặc xóa)
        'ignoreerrors': True,
        
        # Không tải lại các video đã có sẵn trong máy
        'nooverwrites': True,
        
        # Ghi lại lịch sử các video đã tải (để resume nếu bị ngắt quãng)
        'download_archive': 'downloaded.txt',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Bắt đầu xử lý playlist: {playlist_url}")
            ydl.download([playlist_url])
            print("Đã hoàn tất tải playlist!")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

if __name__ == "__main__":
    # Ví dụ cách sử dụng: python download_playlist.py "https://www.youtube.com/playlist?list=..."
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("Vui lòng nhập link YouTube Playlist: ")
        
    download_playlist(url)
