@echo off
chcp 65001 >nul
echo.
echo ╔══════════════════════════════════════════════╗
echo ║   萬用格式轉換器  -  安裝與打包腳本         ║
echo ╚══════════════════════════════════════════════╝
echo.

:: ── 切換到腳本所在目錄 ─────────────────────────────
cd /d "%~dp0"

:: ── 尋找 Python / uv ───────────────────────────────
set PYTHON_CMD=

:: 嘗試 python
python --version >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON_CMD=python
    echo [OK] 找到 python
    goto :install
)

:: 嘗試 py launcher
py --version >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON_CMD=py
    echo [OK] 找到 py launcher
    goto :install
)

:: 嘗試 uv 管理的 Python (常見路徑)
set UV_PYTHON=%APPDATA%\uv\python\cpython-3.12.11-windows-x86_64-none\python.exe
if exist "%UV_PYTHON%" (
    set PYTHON_CMD="%UV_PYTHON%"
    echo [OK] 找到 uv 管理的 Python: %UV_PYTHON%
    goto :install
)

:: 找 uv 並用 uv run
where uv >nul 2>&1
if %errorlevel% == 0 (
    echo [OK] 找到 uv，使用 uv pip install --system
    echo.
    echo [1/2] 安裝套件中...
    uv pip install --system Pillow pillow-heif PyMuPDF pyinstaller
    if %errorlevel% neq 0 goto :fail_pip
    echo.
    echo [2/2] 打包 exe 中...
    uv run pyinstaller --onefile --console --name "萬用格式轉換器" converter.py
    if %errorlevel% neq 0 goto :fail_build
    goto :success
)

:: 都找不到
echo.
echo [錯誤] 找不到 Python！
echo 請先安裝 Python 或確認 uv 已加入 PATH。
echo 下載：https://www.python.org/downloads/
pause
exit /b 1

:: ── 安裝套件 ──────────────────────────────────────
:install
echo.
echo [1/2] 安裝套件中 (Pillow, pillow-heif, PyMuPDF, pyinstaller)...
%PYTHON_CMD% -m pip install --upgrade Pillow pillow-heif PyMuPDF pyinstaller
if %errorlevel% neq 0 goto :fail_pip

echo.
echo [2/2] 打包 exe 中...
%PYTHON_CMD% -m PyInstaller --onefile --console --name "萬用格式轉換器" converter.py
if %errorlevel% neq 0 goto :fail_build

:: ── 成功 ───────────────────────────────────────────
:success
echo.
echo ══════════════════════════════════════════════
echo  ✅  打包完成！
echo  📁  exe 位置：%~dp0dist\萬用格式轉換器.exe
echo ══════════════════════════════════════════════
echo.
explorer "%~dp0dist"
pause
exit /b 0

:: ── 錯誤處理 ───────────────────────────────────────
:fail_pip
echo.
echo [錯誤] 套件安裝失敗。請確認網路連線正常後重試。
pause
exit /b 1

:fail_build
echo.
echo [錯誤] PyInstaller 打包失敗。請查看上方錯誤訊息。
pause
exit /b 1
