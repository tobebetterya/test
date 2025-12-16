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

REM 检查.env文件
if not exist .env (
    echo.
    echo ⚠️  警告: 未找到 .env 文件
    echo 请先配置 OpenAI API 密钥：
    echo   1. 复制: copy .env.example .env
    echo   2. 编辑 .env 文件，填入你的 API 密钥
    echo.
    pause
)

echo.
echo 🚀 启动 IDE...
echo.

REM 运行程序
python script_ide.py %*
