#!/bin/bash
# 启动脚本

echo "================================"
echo "  LangChain 脚本IDE 启动器"
echo "================================"
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python3"
    echo "请先安装 Python 3.7 或更高版本"
    exit 1
fi

echo "✅ Python 版本: $(python3 --version)"

# 检查依赖是否安装
if ! python3 -c "import langchain" 2>/dev/null; then
    echo ""
    echo "⚠️  警告: 依赖未安装"
    echo "正在安装依赖..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败"
        exit 1
    fi
    echo "✅ 依赖安装完成"
fi

# 检查.env文件
if [ ! -f .env ]; then
    echo ""
    echo "⚠️  警告: 未找到 .env 文件"
    echo "请先配置 OpenAI API 密钥："
    echo "  1. 复制: cp .env.example .env"
    echo "  2. 编辑 .env 文件，填入你的 API 密钥"
    echo ""
    read -p "按回车键继续（或Ctrl+C退出）..."
fi

echo ""
echo "🚀 启动 IDE..."
echo ""

# 运行程序
python3 script_ide.py "$@"
