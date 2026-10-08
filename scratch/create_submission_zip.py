import os
import zipfile

base_dir = r"d:\Study\Cô Thương\thuong-cho-tam-than-co-han"
app_dir = os.path.join(base_dir, "app_minesweeper_visualizer")
wecode_py = os.path.join(base_dir, "bai_tap", "WeCode", "giai_do_min_wecode.py")

submission_names = [
    "Đỗ Quốc Thắng – 26410111",
    "Đỗ Quốc Thắng - 26410111"
]

def make_archive(sub_name):
    zip_path = os.path.join(base_dir, f"{sub_name}.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        # 1. Main PDF
        pdf_path = os.path.join(app_dir, "report", "Bao_Cao_Bai_Tap_Lon.pdf")
        z.write(pdf_path, f"{sub_name}/Bao_Cao_Bai_Tap_Lon.pdf")
        
        # 2. Web Visualizer HTML
        z.write(os.path.join(app_dir, "index.html"), f"{sub_name}/index.html")
        
        # 3. WeCode Python solution
        z.write(wecode_py, f"{sub_name}/giai_do_min_wecode.py")
        
        # 4. Markdown report and plan
        z.write(os.path.join(app_dir, "Bao_Cao_Bai_Tap_Lon_Do_Min.md"), f"{sub_name}/Bao_Cao_Bai_Tap_Lon_Do_Min.md")
        z.write(os.path.join(app_dir, "plan.md"), f"{sub_name}/plan.md")
        
        # 5. Demo folder (video + scripts)
        demo_dir = os.path.join(app_dir, "demo")
        for root, dirs, files in os.walk(demo_dir):
            if "build" in root:
                continue
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, app_dir).replace("\\", "/")
                z.write(full_path, f"{sub_name}/{rel_path}")
                
        # 6. Report folder (tex, pdf, overleaf zip, images)
        report_dir = os.path.join(app_dir, "report")
        for root, dirs, files in os.walk(report_dir):
            if "bin" in root or ".system" in root:
                continue
            for file in files:
                if file.endswith((".aux", ".log", ".out", ".toc", ".xdv", ".py")):
                    continue
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, app_dir).replace("\\", "/")
                z.write(full_path, f"{sub_name}/{rel_path}")
                
    size_mb = os.path.getsize(zip_path) / (1024 * 1024)
    print(f"Created zip ({size_mb:.2f} MB)")

for name in submission_names:
    make_archive(name)
