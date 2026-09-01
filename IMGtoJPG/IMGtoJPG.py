import os
import sys
from PIL import Image

def convert_images_to_jpg(input_folder):
    # 定義想要轉換的圖片副檔名 (排除已經是 jpg/jpeg 的檔案)
    supported_formats = ('.png', '.bmp', '.webp', '.tiff', '.gif')
    
    # 確保輸入的資料夾存在
    if not os.path.exists(input_folder):
        print(f"找不到資料夾：{input_folder}")
        return

    # 建立一個獨立的輸出資料夾，避免與原始檔案混在一起
    output_folder = os.path.join(input_folder, 'converted_jpgs')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    count = 0
    # 遍歷資料夾中的所有檔案
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(supported_formats):
            file_path = os.path.join(input_folder, filename)
            
            try:
                # 開啟圖片
                with Image.open(file_path) as img:
                    # 取得沒有副檔名的主檔名
                    name_without_ext = os.path.splitext(filename)[0]
                    output_path = os.path.join(output_folder, f"{name_without_ext}.jpg")

                    # 處理帶有透明度 (RGBA) 或調色盤 (P) 模式的圖片
                    if img.mode in ('RGBA', 'LA', 'P'):
                        # 建立一張全白的底圖
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        if img.mode == 'RGBA':
                            # 將原圖貼上白底，並使用原圖的 alpha 通道做遮罩
                            background.paste(img, mask=img.split()[3]) 
                        else:
                            img_rgb = img.convert('RGBA')
                            background.paste(img_rgb, mask=img_rgb.split()[3])
                            
                        # 儲存為 JPG
                        background.save(output_path, 'JPEG', quality=95)
                    else:
                        # 一般圖片直接轉換為 RGB 並儲存
                        img_rgb = img.convert('RGB')
                        img_rgb.save(output_path, 'JPEG', quality=95)
                        
                print(f"✅ 成功轉換：{filename} -> {name_without_ext}.jpg")
                count += 1
                
            except Exception as e:
                print(f"❌ 轉換 {filename} 時發生錯誤：{e}")

    print(f"\n🎉 轉換完成！共轉換了 {count} 張圖片。")
    print(f"📂 圖片已儲存至：{output_folder}")

# ==========================================
# 自動取得當前程式所在的路徑
# ==========================================
if getattr(sys, 'frozen', False):
    # 如果是被 PyInstaller 等工具打包成 exe 執行
    target_folder = os.path.dirname(sys.executable)
else:
    # 如果是直接以 Python (.py) 腳本執行
    target_folder = os.path.dirname(os.path.abspath(__file__))

print(f"📁 目前所在目錄為：{target_folder}\n")

# 執行轉換
convert_images_to_jpg(target_folder)

# 如果打包成 exe，讓視窗停留一下以免瞬間關閉
os.system("pause")