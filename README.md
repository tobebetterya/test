# 基于LangChain的简易脚本IDE

一个类似Cursor IDE的智能脚本编辑器，可以通过自然语言对话来读取、修改和生成脚本文件。

## 🎯 两个版本可选

本项目提供两个版本，满足不同需求：

| 版本 | 文件名 | 适合场景 | 特点 |
|------|--------|----------|------|
| **基础版** | `script_ide.py` | 小项目、学习 | 简单直观，按需调用工具 |
| **增强版** | `script_ide_enhanced.py` | 大项目、实际使用 | 启动时自动扫描，智能上下文感知 |

📖 **详细对比**: 查看 [COMPARISON.md](COMPARISON.md) 了解两个版本的详细区别

### 快速选择：

- 👉 **文件数 < 10个？** → 使用基础版
- 👉 **需要批量操作？** → 使用增强版
- 👉 **想学习原理？** → 使用基础版
- 👉 **实际项目使用？** → 使用增强版

## ✨ 功能特性

- 📖 **读取文件**: 通过对话读取任何文本或脚本文件
- ✏️ **修改文件**: 自然语言描述修改需求，AI自动修改文件
- 🆕 **创建文件**: 描述需求，AI帮你生成新的脚本文件
- 📋 **文件管理**: 列出、删除工作空间中的文件
- 💬 **对话记忆**: AI记住对话历史，理解上下文
- 🎨 **彩色输出**: 友好的命令行界面

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置API密钥

复制环境变量示例文件并配置你的OpenAI API密钥：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的API密钥：

```
OPENAI_API_KEY=sk-your-api-key-here
```

### 3. 运行程序

**基础版：**
```bash
python script_ide.py
```

**增强版（推荐）：**
```bash
python script_ide_enhanced.py
```

或者使用启动脚本：
```bash
./run.sh              # Linux/Mac
run.bat               # Windows
```

指定自定义工作空间目录：
```bash
python script_ide.py --workspace /path/to/your/workspace
python script_ide_enhanced.py --workspace /path/to/your/workspace
```

禁用增强版的自动扫描：
```bash
python script_ide_enhanced.py --no-scan
```

## 📖 使用示例

### 示例1: 创建Python脚本

```
你: 帮我创建一个Python脚本 hello.py，打印"Hello World"

AI助手: [创建文件 hello.py，包含打印语句]
```

### 示例2: 修改现有文件

```
你: 读取 hello.py 文件

AI助手: [显示文件内容]

你: 把它改成打印"你好，世界！"，并添加一个函数

AI助手: [修改文件，添加函数]
```

### 示例3: 创建配置文件

```
你: 创建一个JSON配置文件 config.json，包含数据库连接信息

AI助手: [生成配置文件]
```

### 示例4: 批量操作

```
你: 列出所有文件

AI助手: [显示工作空间中的所有文件]

你: 删除 test.py

AI助手: [删除指定文件]
```

## 🛠️ 技术架构

- **LangChain**: 核心框架，处理LLM交互和工具调用
- **OpenAI GPT-4**: 强大的语言模型
- **Agent模式**: 使用LangChain的Agent自动选择和执行工具
- **工具系统**: 
  - `read_file`: 读取文件内容
  - `write_file`: 写入/创建文件
  - `list_files`: 列出文件
  - `delete_file`: 删除文件

## 📁 项目结构

```
.
├── script_ide.py                # 基础版主程序
├── script_ide_enhanced.py       # 增强版主程序（推荐）
├── requirements.txt             # Python依赖
├── .env.example                 # 环境变量示例
├── .gitignore                   # Git忽略文件
├── run.sh / run.bat            # 启动脚本
├── README.md                    # 本文件
├── QUICKSTART.md               # 快速入门
├── ANSWER_TO_YOUR_QUESTION.md  # 核心问题解答
├── COMPARISON.md               # 版本对比
├── ENHANCED_FEATURES.md        # 增强功能详解
├── DEMO.md                     # 使用演示
├── PROJECT_OVERVIEW.md         # 技术架构
├── FILE_LIST.md                # 文件清单
└── workspace/                  # 默认工作空间目录
    └── examples/               # 示例文件
```

📋 完整文件说明请查看 [FILE_LIST.md](FILE_LIST.md)

## 🎯 支持的文件类型

理论上支持所有文本格式的文件：

- Python脚本 (`.py`)
- JavaScript/TypeScript (`.js`, `.ts`)
- Shell脚本 (`.sh`, `.bash`)
- 配置文件 (`.json`, `.yaml`, `.toml`, `.ini`)
- 文本文件 (`.txt`, `.md`)
- SQL脚本 (`.sql`)
- 其他任何文本格式

## ⚙️ 命令行参数

```bash
python script_ide.py [选项]

选项:
  --workspace PATH    指定工作空间目录（默认: ./workspace）
  -h, --help         显示帮助信息
```

## 💡 使用技巧

1. **明确描述需求**: 越具体的描述，AI生成的代码越准确
2. **分步操作**: 对于复杂任务，可以分多次对话完成
3. **先读取再修改**: 修改文件前，AI会自动读取文件内容
4. **使用相对路径**: 文件路径相对于工作空间目录
5. **利用对话记忆**: AI会记住之前的对话，可以引用前面的内容

## 🔒 安全提示

- API密钥不要提交到代码仓库
- 工作空间目录默认在 `.gitignore` 中
- 谨慎使用删除文件功能
- 建议定期备份重要文件

## 🛣️ 未来规划

- [ ] 支持更多LLM提供商（Claude, 本地模型等）
- [ ] 添加代码diff预览功能
- [ ] 支持文件夹操作
- [ ] 添加代码执行功能
- [ ] Web界面
- [ ] 多文件同时编辑
- [ ] Git集成

## 📝 注意事项

1. 确保网络可以访问OpenAI API
2. API调用会产生费用，请注意使用量
3. 首次运行会创建工作空间目录
4. 支持中文交互

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

---

**开始使用，享受AI驱动的编程体验吧！** 🚀
