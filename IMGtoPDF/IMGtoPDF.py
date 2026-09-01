import os
import sys
from PIL import Image

def get_executable_path():
    # 取得執行檔或腳本所在的資料夾路徑
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def convert_images():
    base_path = get_executable_path()
    valid_extensions = ('.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG')
    
    # 1. 掃描檔案
    files = [f for f in os.listdir(base_path) if f.endswith(valid_extensions)]
    files.sort() # 按名稱排序

    if not files:
        print("找不到任何圖片檔案 (png, jpg, jpeg)。")
        input("按任意鍵結束...")
        return

    print(f"偵測到 {len(files)} 個圖片檔案。")
    print("-" * 30)
    print("請選擇轉換模式：")
    print("(1) 全部合併成一個 PDF 檔")
    print("(2) 每個圖片各別轉成一個 PDF 檔")
    print("-" * 30)
    
    choice = input("請輸入編號 (1 或 2): ")

    if choice == '1':
        # 模式 1：合併轉換
        output_list = []
        for f in files:
            img = Image.open(os.path.join(base_path, f))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            output_list.append(img)
        
        if output_list:
            pdf_path = os.path.join(base_path, "combined_output.pdf")
            output_list[0].save(pdf_path, save_all=True, append_images=output_list[1:])
            print(f"成功！已儲存為: {pdf_path}")

    elif choice == '2':
        # 模式 2：各別轉換
        output_dir = os.path.join(base_path, "converted_pdfs")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        for f in files:
            img = Image.open(os.path.join(base_path, f))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            filename = os.path.splitext(f)[0] + ".pdf"
            img.save(os.path.join(output_dir, filename))
        print(f"成功！檔案已存放在: {output_dir}")
    
    else:
        print("無效的選擇。")

    input("\n處理完畢，按任意鍵退出...")

if __name__ == "__main__":
    convert_images()