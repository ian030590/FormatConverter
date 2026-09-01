import fitz  # PyMuPDF (用於 PDF 處理)
import os
import glob
from sys import exit # 用於在找不到檔案時結束程式

# 設定要處理的資料夾路徑，'.' 代表程式碼所在的當前資料夾
folder_path = '.'

# 創建一個名為 'output' 的資料夾來存放轉換後的 PDF
output_folder = os.path.join(folder_path, 'output')
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f"已創建輸出資料夾: '{output_folder}'")


# 找到資料夾中所有的圖片檔案 (.jpg, .jpeg, .png)
image_extensions = ['*.jpg', '*.jpeg', '*.png']
image_files = []
for ext in image_extensions:
    # 使用 sorted() 確保檔案依名稱排序，並將所有副檔名的結果合併到一個列表中
    image_files.extend(sorted(glob.glob(os.path.join(folder_path, ext))))

# 移除可能的重複路徑（雖然不常發生，但確保列表乾淨）
image_files = sorted(list(set(image_files)))


# 檢查是否找到任何圖片檔案
if not image_files:
    print("="*50)
    print("在當前資料夾中找不到任何 .jpg, .jpeg, 或 .png 圖片檔案。")
    print("請確保您要轉換的圖片檔案放在與此程式碼相同的資料夾中。")
    print("="*50)
else:
    print(f"找到 {len(image_files)} 個圖片檔案。將逐一轉換為單一 PDF 文件...")
    print("="*50)

    # 遍歷所有找到的圖片檔案，單獨處理
    for img_path in image_files:
        pdf_document = None # 初始化文件變數
        try:
            # 獲取原始檔案名稱（包含副檔名）
            original_filename = os.path.basename(img_path)
            
            # 設定輸出 PDF 的名稱：將圖片副檔名替換為 .pdf
            # os.path.splitext(original_filename)[0] 取得不含副檔名的部分
            file_base_name = os.path.splitext(original_filename)[0]
            output_pdf_name = f"{file_base_name}.pdf"
            output_pdf_path = os.path.join(output_folder, output_pdf_name)

            # 創建一個新的空白 PDF 文件 (每張圖片一個文件)
            pdf_document = fitz.open()

            # PyMuPDF 可以直接打開圖片檔案並將其視為只有一頁的 PDF 文件
            with fitz.open(img_path) as img_doc:
                # 將圖片頁面插入到主 PDF 文件中
                # fitz 會自動調整圖片大小以適應標準 PDF 頁面
                pdf_document.insert_pdf(img_doc)
            
            # 儲存最終的 PDF 文件
            pdf_document.save(output_pdf_path, garbage=4, deflate=True) # 進行優化和壓縮
            
            print(f"✅ 成功轉換：'{original_filename}' -> '{output_pdf_name}'")

        except Exception as e:
            print(f"❌ 處理檔案 '{original_filename}' 時發生錯誤：{e}")
        finally:
            # 確保關閉 PDF 文件，無論成功或失敗
            if pdf_document:
                pdf_document.close()

    print("\n" + "="*50)
    print("🎉 所有圖片單獨轉換為 PDF 的任務已完成！")
    print(f"📁 檔案已儲存至 '{output_folder}' 資料夾。")
    print("="*50)

print("所有圖片轉換為 PDF 的任務已完成！")
