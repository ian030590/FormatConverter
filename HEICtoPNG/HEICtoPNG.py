import os
from pathlib import Path
from PIL import Image
from pillow_heif import register_heif_opener

# 註冊 HEIF 開啟器，讓 Pillow 可以識別和處理 .heic 檔案
register_heif_opener()

def convert_heic_to_png(input_dir: str, output_dir_name: str = "outputs"):
    """
    偵測指定資料夾及其子資料夾中的 .heic 或 .heif 檔案，
    將它們轉換為無損的 .png 格式，並存入指定的輸出資料夾。

    Args:
        input_dir (str): 程式執行所在的根資料夾路徑。
        output_dir_name (str): 輸出 PNG 檔案的資料夾名稱。
    """
    
    # 建立輸出資料夾
    output_path = Path(input_dir) / output_dir_name
    output_path.mkdir(exist_ok=True)
    
    print(f"--- HEIC/HEIF 轉 PNG 轉換程式 ---")
    print(f"正在搜尋資料夾：{input_dir}")
    print(f"PNG 輸出資料夾：{output_path.resolve()}")
    print("-" * 30)
    
    heic_files_found = 0
    conversions_successful = 0
    
    # 遍歷指定資料夾及其所有子資料夾
    for root, _, files in os.walk(input_dir):
        for file in files:
            # 檢查檔案是否為 HEIC/HEIF 格式，不區分大小寫
            if file.lower().endswith(('.heic', '.heif')):
                heic_files_found += 1
                
                input_file_path = Path(root) / file
                
                # 確保不處理輸出資料夾中的檔案
                if output_dir_name in input_file_path.parts:
                    continue

                try:
                    print(f"找到檔案：{input_file_path.name}")
                    
                    # 使用 Pillow 打開 HEIC 檔案
                    # 由於 register_heif_opener() 的作用，Pillow 可以直接處理
                    img = Image.open(input_file_path)
                    
                    # 建立輸出檔案名稱 (將副檔名替換為 .png)
                    base_name = input_file_path.stem
                    output_file_name = f"{base_name}.png"
                    output_file_path = output_path / output_file_name
                    
                    # 儲存為 PNG 格式
                    # PNG 是一種無損格式，且 save() 預設就是無損壓縮
                    # optimize=True 可以略微縮小檔案大小，但不會影響畫質
                    img.save(output_file_path, format="PNG", optimize=True)
                    
                    print(f"  -> 成功轉換並儲存為：{output_file_path.name}")
                    conversions_successful += 1

                except Exception as e:
                    print(f"  -> 轉換失敗：{input_file_path.name} 錯誤: {e}")

    print("-" * 30)
    print(f"掃描完成。")
    print(f"總共找到 HEIC/HEIF 檔案：{heic_files_found} 個")
    print(f"成功轉換為 PNG 檔案：{conversions_successful} 個")
    print("所有轉換後的 PNG 檔案已存放在 'outputs' 資料夾中。")
    
    # 讓視窗保持開啟，直到使用者按下 Enter (僅在 .exe 運行時有用)
    if os.environ.get("CONVERT_TO_EXE"):
        input("\n轉換完成，請按 Enter 鍵結束程式...")

if __name__ == "__main__":
    # 取得當前腳本執行所在的資料夾路徑
    current_directory = os.getcwd()
    
    # 為了方便 PyInstaller 打包，設定一個環境變數標記
    os.environ["CONVERT_TO_EXE"] = "1" 
    
    convert_heic_to_png(current_directory)