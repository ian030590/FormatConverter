"""
萬用格式轉換器 (Universal Format Converter)
整合所有圖片/PDF 格式轉換功能的終端工具
支援格式: HEIC, PNG, JPG, BMP, WEBP, TIFF, GIF, PDF
"""

import os
import sys
import glob
import shutil
from pathlib import Path

# ──────────────────────────────────────────────
# 彩色終端輸出工具
# ──────────────────────────────────────────────
class Color:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"
    DIM     = "\033[2m"

def c(text, color, bold=False):
    prefix = Color.BOLD if bold else ""
    return f"{prefix}{color}{text}{Color.RESET}"

def print_header():
    """列印程式標題橫幅"""
    os.system("cls" if os.name == "nt" else "clear")
    print(c("╔══════════════════════════════════════════════════╗", Color.CYAN, True))
    print(c("║       萬用格式轉換器  Universal Converter        ║", Color.CYAN, True))
    print(c("║   支援 HEIC · PNG · JPG · BMP · WEBP · PDF 等   ║", Color.CYAN, True))
    print(c("╚══════════════════════════════════════════════════╝", Color.CYAN, True))
    print()

def print_separator(char="─", width=52):
    print(c(char * width, Color.DIM))

def print_success(msg): print(c(f"  ✅ {msg}", Color.GREEN))
def print_error(msg):   print(c(f"  ❌ {msg}", Color.RED))
def print_info(msg):    print(c(f"  ℹ  {msg}", Color.CYAN))
def print_warn(msg):    print(c(f"  ⚠  {msg}", Color.YELLOW))

# ──────────────────────────────────────────────
# 路徑工具
# ──────────────────────────────────────────────
def get_base_path() -> Path:
    """取得執行檔或腳本所在目錄（PyInstaller 相容）"""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(os.path.abspath(__file__)).parent

def make_output_dir(base: Path, name: str = "converted_output") -> Path:
    """在 base 目錄下建立輸出資料夾"""
    out = base / name
    out.mkdir(parents=True, exist_ok=True)
    return out

def scan_files(folder: Path, extensions: list[str]) -> list[Path]:
    """掃描資料夾中符合副檔名的檔案（不區分大小寫）"""
    result = []
    for f in sorted(folder.iterdir()):
        if f.is_file() and f.suffix.lower() in extensions:
            result.append(f)
    return result

def prompt_input_folder() -> Path:
    """讓使用者輸入來源資料夾，預設為程式所在目錄"""
    base = get_base_path()
    print_info(f"預設來源資料夾：{base}")
    raw = input(c("  請輸入來源資料夾路徑（直接按 Enter 使用預設）: ", Color.WHITE)).strip()
    if raw:
        p = Path(raw)
        if not p.is_dir():
            print_error(f"找不到資料夾：{raw}")
            return None
        return p
    return base

# ──────────────────────────────────────────────
# 轉換核心函式
# ──────────────────────────────────────────────

# ---------- Pillow / pillow-heif ----------
def _load_pillow():
    try:
        from PIL import Image
        return Image
    except ImportError:
        print_error("缺少套件 Pillow，請執行: pip install Pillow")
        return None

def _load_heif():
    try:
        from pillow_heif import register_heif_opener
        register_heif_opener()
        return True
    except ImportError:
        print_error("缺少套件 pillow-heif，請執行: pip install pillow-heif")
        return False

def _load_fitz():
    try:
        import fitz
        return fitz
    except ImportError:
        print_error("缺少套件 PyMuPDF，請執行: pip install PyMuPDF")
        return None

# ---------- 圖片共用 save ----------
def _save_as(img, output_path: Path, fmt: str, quality: int = 95):
    """儲存圖片，自動處理透明通道"""
    Image = _load_pillow()
    if Image is None:
        return False
    if fmt.upper() in ("JPEG", "JPG"):
        if img.mode in ("RGBA", "LA", "P"):
            bg = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "RGBA":
                bg.paste(img, mask=img.split()[3])
            else:
                rgba = img.convert("RGBA")
                bg.paste(rgba, mask=rgba.split()[3])
            img = bg
        else:
            img = img.convert("RGB")
        img.save(output_path, "JPEG", quality=quality)
    elif fmt.upper() == "PNG":
        img.save(output_path, "PNG", optimize=True)
    elif fmt.upper() == "BMP":
        img.convert("RGB").save(output_path, "BMP")
    elif fmt.upper() == "WEBP":
        img.save(output_path, "WEBP", quality=quality)
    elif fmt.upper() == "TIFF":
        img.save(output_path, "TIFF")
    elif fmt.upper() == "GIF":
        img.save(output_path, "GIF")
    return True

# ══════════════════════════════════════════════
# 功能 1：圖片 → 圖片格式轉換
# ══════════════════════════════════════════════
IMG_EXTS = [".heic", ".heif", ".png", ".jpg", ".jpeg",
            ".bmp", ".webp", ".tiff", ".tif", ".gif"]
IMG_FMT_CHOICES = {
    "1": ("JPG",  ".jpg"),
    "2": ("PNG",  ".png"),
    "3": ("BMP",  ".bmp"),
    "4": ("WEBP", ".webp"),
    "5": ("TIFF", ".tiff"),
    "6": ("GIF",  ".gif"),
}

def convert_img_to_img(src_folder: Path):
    """圖片格式互轉（含 HEIC）"""
    Image = _load_pillow()
    if Image is None:
        return

    # 選擇目標格式
    print()
    print(c("  選擇輸出格式：", Color.YELLOW, True))
    for k, (name, _) in IMG_FMT_CHOICES.items():
        print(f"    {c(k, Color.CYAN)}) {name}")
    choice = input(c("  請輸入編號: ", Color.WHITE)).strip()
    if choice not in IMG_FMT_CHOICES:
        print_error("無效選擇。")
        return
    target_fmt, target_ext = IMG_FMT_CHOICES[choice]

    # 如果輸入包含 HEIC，載入 heif opener
    all_files = scan_files(src_folder, IMG_EXTS)
    has_heic = any(f.suffix.lower() in (".heic", ".heif") for f in all_files)
    if has_heic:
        _load_heif()

    # 過濾掉已是目標格式的檔案
    files = [f for f in all_files if f.suffix.lower() != target_ext.lower()]
    if not files:
        print_warn(f"在 {src_folder} 中找不到可轉換的圖片（排除已是 {target_fmt} 的檔案）。")
        return

    print_info(f"找到 {len(files)} 個圖片檔案，將轉換為 {target_fmt}")
    out_dir = make_output_dir(src_folder, f"converted_to_{target_fmt.lower()}")
    print_separator()

    success = 0
    for f in files:
        try:
            img = Image.open(f)
            out_path = out_dir / (f.stem + target_ext)
            _save_as(img, out_path, target_fmt)
            print_success(f"{f.name}  →  {out_path.name}")
            success += 1
        except Exception as e:
            print_error(f"{f.name}：{e}")

    print_separator()
    print_success(f"完成！共轉換 {success}/{len(files)} 個檔案")
    print_info(f"輸出資料夾：{out_dir}")

# ══════════════════════════════════════════════
# 功能 2：圖片 → PDF
# ══════════════════════════════════════════════
IMG_FOR_PDF_EXTS = [".png", ".jpg", ".jpeg", ".bmp",
                    ".webp", ".tiff", ".tif", ".gif",
                    ".heic", ".heif"]

def convert_img_to_pdf(src_folder: Path):
    """圖片轉 PDF，可選個別轉換或合併成一個 PDF"""
    Image = _load_pillow()
    if Image is None:
        return

    has_heic = any(f.suffix.lower() in (".heic", ".heif")
                   for f in src_folder.iterdir() if f.is_file())
    if has_heic:
        _load_heif()

    files = scan_files(src_folder, IMG_FOR_PDF_EXTS)
    if not files:
        print_warn(f"在 {src_folder} 中找不到任何圖片檔案。")
        return

    print_info(f"找到 {len(files)} 個圖片檔案")
    for i, f in enumerate(files, 1):
        print(f"    {c(str(i), Color.DIM)}. {f.name}")
    print()
    print(c("  選擇轉換模式：", Color.YELLOW, True))
    print(f"    {c('1', Color.CYAN)}) 每張圖片各自轉換為獨立 PDF")
    print(f"    {c('2', Color.CYAN)}) 所有圖片合併為一個 PDF")
    mode = input(c("  請輸入編號 (1 或 2): ", Color.WHITE)).strip()
    print_separator()

    if mode == "1":
        out_dir = make_output_dir(src_folder, "converted_to_pdf")
        success = 0
        for f in files:
            try:
                img = Image.open(f)
                if img.mode != "RGB":
                    img = img.convert("RGB")
                out_path = out_dir / (f.stem + ".pdf")
                img.save(out_path, "PDF")
                print_success(f"{f.name}  →  {out_path.name}")
                success += 1
            except Exception as e:
                print_error(f"{f.name}：{e}")
        print_separator()
        print_success(f"完成！共轉換 {success}/{len(files)} 個檔案")
        print_info(f"輸出資料夾：{out_dir}")

    elif mode == "2":
        merged_name = input(c("  輸入合併後的 PDF 檔案名稱（不需加 .pdf，預設: combined）: ",
                              Color.WHITE)).strip()
        if not merged_name:
            merged_name = "combined"
        out_path = src_folder / f"{merged_name}.pdf"
        try:
            imgs = []
            for f in files:
                img = Image.open(f)
                if img.mode != "RGB":
                    img = img.convert("RGB")
                imgs.append(img)
                print_info(f"已載入：{f.name}")
            if imgs:
                imgs[0].save(out_path, "PDF", save_all=True, append_images=imgs[1:])
                print_separator()
                print_success(f"合併完成！→  {out_path}")
        except Exception as e:
            print_error(f"合併失敗：{e}")
    else:
        print_error("無效選擇。")

# ══════════════════════════════════════════════
# 功能 3：PDF → 圖片格式
# ══════════════════════════════════════════════
PDF_OUT_CHOICES = {
    "1": ("JPG",  ".jpg"),
    "2": ("PNG",  ".png"),
}

def convert_pdf_to_img(src_folder: Path):
    """PDF 轉圖片（JPG / PNG）"""
    fitz = _load_fitz()
    Image = _load_pillow()
    if fitz is None or Image is None:
        return

    pdf_files = scan_files(src_folder, [".pdf"])
    if not pdf_files:
        print_warn(f"在 {src_folder} 中找不到任何 PDF 檔案。")
        return

    print_info(f"找到 {len(pdf_files)} 個 PDF 檔案")
    print()
    print(c("  選擇輸出圖片格式：", Color.YELLOW, True))
    for k, (name, _) in PDF_OUT_CHOICES.items():
        print(f"    {c(k, Color.CYAN)}) {name}")
    fmt_choice = input(c("  請輸入編號: ", Color.WHITE)).strip()
    if fmt_choice not in PDF_OUT_CHOICES:
        print_error("無效選擇。")
        return
    target_fmt, target_ext = PDF_OUT_CHOICES[fmt_choice]

    # DPI 設定
    print()
    print(c("  選擇輸出解析度：", Color.YELLOW, True))
    print(f"    {c('1', Color.CYAN)}) 標準 (150 DPI)  - 快速，檔案較小")
    print(f"    {c('2', Color.CYAN)}) 高解析 (300 DPI) - 推薦，品質佳")
    print(f"    {c('3', Color.CYAN)}) 超高解析 (600 DPI) - 最高品質，檔案最大")
    dpi_map = {"1": 1.5, "2": 3.0, "3": 6.0}
    dpi_name = {"1": "150", "2": "300", "3": "600"}
    dpi_choice = input(c("  請輸入編號 (預設 2): ", Color.WHITE)).strip() or "2"
    zoom = dpi_map.get(dpi_choice, 3.0)

    out_dir = make_output_dir(src_folder, f"converted_to_{target_fmt.lower()}")
    print_separator()

    total_pages = 0
    for pdf_path in pdf_files:
        try:
            doc = fitz.open(str(pdf_path))
            num_pages = len(doc)
            mat = fitz.Matrix(zoom, zoom)
            base_name = pdf_path.stem

            for page_num in range(num_pages):
                page = doc.load_page(page_num)
                pix = page.get_pixmap(matrix=mat)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

                if num_pages == 1:
                    out_name = f"{base_name}{target_ext}"
                else:
                    out_name = f"{base_name}_page{page_num + 1:03d}{target_ext}"

                out_file = out_dir / out_name
                _save_as(img, out_file, target_fmt)
                total_pages += 1

            doc.close()
            print_success(f"{pdf_path.name}  →  {num_pages} 頁")
        except Exception as e:
            print_error(f"{pdf_path.name}：{e}")

    print_separator()
    print_success(f"完成！共轉換 {len(pdf_files)} 個 PDF，{total_pages} 頁圖片")
    print_info(f"輸出資料夾：{out_dir}")

# ══════════════════════════════════════════════
# 功能 4：PDF 合併
# ══════════════════════════════════════════════
def merge_pdfs(src_folder: Path):
    """將資料夾中所有 PDF 合併為一個"""
    fitz = _load_fitz()
    if fitz is None:
        return

    pdf_files = scan_files(src_folder, [".pdf"])
    if not pdf_files:
        print_warn(f"在 {src_folder} 中找不到任何 PDF 檔案。")
        return

    print_info(f"找到 {len(pdf_files)} 個 PDF 檔案（將依檔名順序合併）：")
    for i, f in enumerate(pdf_files, 1):
        print(f"    {c(str(i), Color.DIM)}. {f.name}")

    merged_name = input(c("\n  輸入輸出檔案名稱（不需加 .pdf，預設: merged）: ",
                          Color.WHITE)).strip()
    if not merged_name:
        merged_name = "merged"
    out_path = src_folder / f"{merged_name}.pdf"
    print_separator()

    try:
        merged_doc = fitz.open()
        for pdf_path in pdf_files:
            with fitz.open(str(pdf_path)) as doc:
                merged_doc.insert_pdf(doc)
                print_info(f"已合併：{pdf_path.name} ({len(doc)} 頁)")
        merged_doc.save(str(out_path), garbage=4, deflate=True)
        merged_doc.close()
        print_separator()
        print_success(f"合併完成！→  {out_path}")
    except Exception as e:
        print_error(f"合併失敗：{e}")

# ══════════════════════════════════════════════
# 主選單
# ══════════════════════════════════════════════
MENU_ITEMS = {
    "1": "圖片格式互轉      (HEIC/PNG/JPG/BMP/WEBP/TIFF/GIF → 各種格式)",
    "2": "圖片 → PDF        (可選各自轉換 或 合併成一個 PDF)",
    "3": "PDF  → 圖片       (JPG / PNG，可選解析度)",
    "4": "PDF  合併          (多個 PDF 合併為一個)",
    "0": "離開",
}

def main():
    while True:
        print_header()
        print(c("  ▌ 請選擇功能", Color.YELLOW, True))
        print_separator()
        for key, desc in MENU_ITEMS.items():
            color = Color.RED if key == "0" else Color.CYAN
            print(f"    {c(key, color, True)})  {desc}")
        print_separator()

        choice = input(c("\n  請輸入功能編號: ", Color.WHITE)).strip()

        if choice == "0":
            print_info("感謝使用，再見！")
            break

        if choice not in MENU_ITEMS or choice == "0":
            print_error("無效選擇，請重新輸入。")
            input(c("\n  按 Enter 返回主選單…", Color.DIM))
            continue

        print()
        src = prompt_input_folder()
        if src is None:
            input(c("\n  按 Enter 返回主選單…", Color.DIM))
            continue

        print_separator()

        try:
            if choice == "1":
                convert_img_to_img(src)
            elif choice == "2":
                convert_img_to_pdf(src)
            elif choice == "3":
                convert_pdf_to_img(src)
            elif choice == "4":
                merge_pdfs(src)
        except KeyboardInterrupt:
            print_warn("\n操作已取消。")

        input(c("\n  按 Enter 返回主選單…", Color.DIM))

if __name__ == "__main__":
    # 啟用 Windows 終端彩色輸出
    if os.name == "nt":
        os.system("color")
        import ctypes
        try:
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except Exception:
            pass
    main()
