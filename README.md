# FormatConverter (多格式批次檔案轉換工具箱) 🔄🖼️

高效輕量的多媒體與文件格式批次轉換工具集，支援圖片、高效率圖檔（HEIC）與 PDF 雙向互轉，提供萬用終端互動式 CLI 與獨立功能腳本。

## 🌟 支援轉換功能 / Features

- 📑 **PDF 與圖片互轉**：
  - `PDFtoJPG` / `PDFtoPNG`：將 PDF 文件各頁批次提取轉換為高解析度圖檔。
  - `IMGtoPDF` / `JPGtoPDF`：將單張或多張圖片（JPG, PNG, WebP）合併轉換為標準 PDF 文件。
- 📱 **手機照片相容性轉換**：
  - `HEICtoPNG`：批次將 Apple iPhone/iPad 之 HEIC 高效率圖檔轉為 PNG。
  - `IMGtoJPG`：通用格式轉為標準 JPEG。
- 🧰 **萬用轉換器（Universal Converter）**：
  - 整合式終端工具（`UniversalConverter/converter.py`），支援 HEIC、PNG、JPG、BMP、WEBP、TIFF、GIF、PDF 一鍵掃描與批次互轉。

## 📂 專案目錄結構 / Directory Structure

```text
Format Converter/
├── UniversalConverter/    # 萬用多格式整合轉換器
├── HEICtoPNG/             # HEIC 轉 PNG 專用工具
├── IMGtoJPG/              # 圖片轉 JPG 專用工具
├── IMGtoPDF/              # 圖片轉 PDF 專用工具
├── JPGtoPDF/              # JPG 轉 PDF 專用工具
├── PDFtoJPG/              # PDF 轉 JPG 專用工具
├── PDFtoPNG/              # PDF 轉 PNG 專用工具
└── README.md              # 專案說明文件
```

## 🚀 使用方式 / Quick Start

### 萬用轉換器 (Universal Converter)
```bash
cd UniversalConverter
pip install pillow pillow-heif pypdf pdf2image
python converter.py
```

### 獨立模組執行
進入各專用資料夾，將待處理檔案放置於同層目錄或指定路徑後執行對應 Python 腳本即可。

## 📄 授權 / License

MIT License
