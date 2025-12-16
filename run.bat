@echo off
REM Windows启动脚本
chcp 65001 >nul

echo ================================
echo   LangChain 脚本IDE 启动器
echo ================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到 Python
    echo 请先安装 Python 3.7 或更高版本
    pause
    exit /b 1
)

echo ✅ Python 已安装

REM 检查依赖
python -c "import langchain" >nul 2>&1
if errorlevel 1 (
    echo.
    echo ⚠️  警告: 依赖未安装
    echo 正在安装依赖...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ 依赖安装失败
        pause
        exit /b 1
    )
    echo ✅ 依赖安装完成
)

REM 检查config.py文件
if not exist config.py (
    echo.
    echo ⚠️  警告: 未找到 config.py 文件
    echo 请先配置 API：
    echo   1. 复制: copy config.py.example config.py
    echo   2. 编辑 config.py 文件，填入你的 API 配置
    echo.
    pause
)

echo.
echo 请选择版本：
echo   1) 基础版 (script_ide.py)
echo   2) 增强版 (script_ide_enhanced.py) - 推荐
echo.
set /p choice="请输入选项 [1/2] (默认: 2): "

if "%choice%"=="" set choice=2

if "%choice%"=="1" (
    echo.
    echo 🚀 启动基础版...
    echo.
    python script_ide.py %*
) else if "%choice%"=="2" (
    echo.
    echo 🚀 启动增强版...
    echo.
    python script_ide_enhanced.py %*
) else (
    echo ❌ 无效选项
    pause
    exit /b 1
)
