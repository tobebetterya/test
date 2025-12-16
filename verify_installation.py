#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安装验证脚本
检查所有依赖和配置是否正确
"""

import sys
from pathlib import Path

def print_status(message, status):
    """打印状态信息"""
    if status:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")
    return status

def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    is_ok = version.major == 3 and version.minor >= 7
    print_status(f"Python版本: {version.major}.{version.minor}.{version.micro}", is_ok)
    if not is_ok:
        print("   需要Python 3.7或更高版本")
    return is_ok

def check_dependencies():
    """检查依赖包"""
    required = {
        'langchain': 'LangChain',
        'langchain_openai': 'LangChain OpenAI',
        'langchain_community': 'LangChain Community',
        'colorama': 'Colorama'
    }
    
    all_ok = True
    for module, name in required.items():
        try:
            __import__(module)
            print_status(f"{name} 已安装", True)
        except ImportError:
            print_status(f"{name} 未安装", False)
            all_ok = False
    
    if not all_ok:
        print("\n请运行: pip install -r requirements.txt")
    
    return all_ok

def check_config():
    """检查配置文件"""
    config_file = Path(__file__).parent / "config.py"
    
    if not config_file.exists():
        print_status("配置文件 config.py", False)
        print("   请运行: cp config.py.example config.py")
        print("   然后编辑 config.py 填入你的API配置")
        return False
    
    # 尝试加载配置
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("config", config_file)
        config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config)
        
        print_status("配置文件 config.py", True)
        
        # 检查必需的配置项
        has_api_key = hasattr(config, 'API_KEY') and config.API_KEY
        has_base_url = hasattr(config, 'API_BASE_URL') and config.API_BASE_URL
        has_model = hasattr(config, 'DEFAULT_MODEL') and config.DEFAULT_MODEL
        
        print_status(f"  API_KEY: {'已配置' if has_api_key else '未配置'}", has_api_key)
        print_status(f"  API_BASE_URL: {config.API_BASE_URL if has_base_url else '未配置'}", has_base_url)
        print_status(f"  DEFAULT_MODEL: {config.DEFAULT_MODEL if has_model else '未配置'}", has_model)
        
        if has_api_key and config.API_KEY.startswith("sk-"):
            print("   ⚠️  API_KEY看起来是示例值，请填入真实的密钥")
        
        return has_api_key and has_base_url and has_model
        
    except Exception as e:
        print_status("配置文件加载", False)
        print(f"   错误: {e}")
        return False

def check_files():
    """检查核心文件"""
    files = {
        'script_ide.py': '基础版程序',
        'script_ide_enhanced.py': '增强版程序',
        'requirements.txt': '依赖文件',
        'config.py.example': '配置模板'
    }
    
    all_ok = True
    for file, desc in files.items():
        exists = (Path(__file__).parent / file).exists()
        print_status(f"{desc} ({file})", exists)
        all_ok = all_ok and exists
    
    return all_ok

def main():
    """主函数"""
    print("=" * 60)
    print("LangChain Script IDE - 安装验证")
    print("=" * 60)
    print()
    
    print("【1/4】检查Python环境")
    py_ok = check_python_version()
    print()
    
    print("【2/4】检查依赖包")
    deps_ok = check_dependencies()
    print()
    
    print("【3/4】检查核心文件")
    files_ok = check_files()
    print()
    
    print("【4/4】检查配置文件")
    config_ok = check_config()
    print()
    
    print("=" * 60)
    if py_ok and deps_ok and files_ok and config_ok:
        print("✅ 所有检查通过！")
        print()
        print("🚀 现在可以运行程序了：")
        print()
        print("   python script_ide_enhanced.py")
        print()
        print("或使用启动脚本：")
        print("   ./run.sh (Linux/Mac)")
        print("   run.bat (Windows)")
    else:
        print("❌ 部分检查未通过，请根据上述提示修复")
        print()
        print("常见问题：")
        print("1. 依赖未安装 → pip install -r requirements.txt")
        print("2. 配置文件不存在 → cp config.py.example config.py")
        print("3. API未配置 → 编辑 config.py 填入API信息")
        print()
        print("📖 详细帮助：")
        print("   - 快速开始: START_HERE.md")
        print("   - 配置指南: CONFIG_GUIDE.md")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
