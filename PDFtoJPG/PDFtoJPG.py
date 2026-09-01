import fitz  # PyMuPDF
from PIL import Image
import os
import glob

# 設定要處理的資料夾路徑，'.' 代表程式碼所在的當前資料夾
folder_path = '.'

# 創建一個名為 'output' 的資料夾來存放轉換後的圖片
output_folder = os.path.join(folder_path, 'output')
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 找到資料夾中所有的 PDF 檔案
pdf_files = glob.glob(os.path.join(folder_path, '*.pdf'))

# 檢查是否找到任何 PDF 檔案
if not pdf_files:
    print("在當前資料夾中找不到任何 PDF 檔案。")
else:
    # 逐一處理每一個 PDF 檔案
    for pdf_path in pdf_files:
        try:
            # 獲取 PDF 檔案的名稱（不包含副檔名）
            file_name = os.path.splitext(os.path.basename(pdf_path))[0]
            
            # 打開 PDF 檔案
            doc = fitz.open(pdf_path)
            
            # 判斷 PDF 總頁數
            num_pages = len(doc)

            # 設定圖片的解析度。數值越高，圖片越清晰，但檔案也越大。
            # 2.0 代表 DPI 提高為原始的 2 倍。
            zoom_factor = 2.0
            mat = fitz.Matrix(zoom_factor, zoom_factor)

            # 遍歷 PDF 的每一頁
            for page_num in range(num_pages):
                page = doc.load_page(page_num)
                pix = page.get_pixmap(matrix=mat)
                
                # 將 pixmap 轉換為 PIL Image 物件
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                
                # 根據頁數設定輸出檔名
                if num_pages == 1:
                    # 只有一頁時，檔名為原始檔名
                    output_path = os.path.join(output_folder, f"{file_name}.jpg")
                else:
                    # 超過一頁時，檔名加上頁碼
                    output_path = os.path.join(output_folder, f"{file_name}_page_{page_num + 1}.jpg")

                # 儲存為 JPG 圖片
                img.save(output_path, "JPG")
                
            print(f"已成功將 '{os.path.basename(pdf_path)}' 轉換並儲存在 'output' 資料夾中。")
            
        except Exception as e:
            print(f"處理檔案 '{os.path.basename(pdf_path)}' 時發生錯誤：{e}")

print("所有 PDF 轉換任務已完成！")
