# 🚀 从这里开始

欢迎使用基于LangChain的智能脚本IDE！

## ⚡ 3步快速开始

### 1️⃣ 安装依赖

```bash
pip install -r requirements.txt
```

### 2️⃣ 配置API

```bash
# 复制配置模板
cp config.py.example config.py

# 编辑配置文件
nano config.py  # 或使用你喜欢的编辑器
```

在 `config.py` 中填入你的配置：

```python
# API配置
API_BASE_URL = "https://oneapi.qunhequnhe.com/v1"  # 你的API地址
API_KEY = "sk-xxxxxx"  # 你的API密钥

# 默认模型
DEFAULT_MODEL = "doubao-seed-1.6"  # 选择你要使用的模型
```

### 3️⃣ 运行程序

```bash
# 推荐：使用增强版（自动扫描项目）
python script_ide_enhanced.py

# 或使用启动脚本（可选择版本）
./run.sh        # Linux/Mac
run.bat         # Windows
```

## 🎯 第一次使用

启动后，尝试这些命令：

```
你: 列出所有文件

你: 创建一个Python脚本 hello.py，打印"你好世界"

你: 读取 hello.py

你: 修改它，添加一个函数
```

## 📚 重要文档

根据你的需求阅读：

| 文档 | 适合场景 | 阅读时间 |
|------|----------|----------|
| **CONFIG_GUIDE.md** | 配置API和模型 | 5分钟 |
| **QUICKSTART.md** | 快速入门教程 | 5分钟 |
| **ANSWER_TO_YOUR_QUESTION.md** | 理解自动检索机制 | 10分钟 |
| **COMPARISON.md** | 选择合适的版本 | 10分钟 |
| **README.md** | 完整功能说明 | 15分钟 |

## ❓ 常见问题

### Q: 我应该用哪个版本？

- **文件数 < 10个** → 使用 `script_ide.py`（基础版）
- **文件数 > 10个** → 使用 `script_ide_enhanced.py`（增强版，推荐）

### Q: 配置文件格式是什么样的？

就是你要求的Python格式：

```python
# API配置
API_BASE_URL = "https://oneapi.qunhequnhe.com/v1"
API_KEY = "sk-xxx"

# 可用的模型列表
AVAILABLE_MODELS = {
    "deepseek-r1-0528": "DeepSeek R1 模型",
    "qwen-plus-latest": "通义千问 Plus 最新版",
    "doubao-seed-1.6": "豆包 Seed 1.6 模型"
}

DEFAULT_MODEL = "doubao-seed-1.6"
```

详见：[CONFIG_GUIDE.md](CONFIG_GUIDE.md)

### Q: 会自动检索文件吗？

**会！** 增强版启动时会：
1. 扫描所有文件
2. 读取关键文件（README、配置、代码）
3. AI获得完整项目上下文

详见：[ANSWER_TO_YOUR_QUESTION.md](ANSWER_TO_YOUR_QUESTION.md)

### Q: 支持哪些API？

支持所有兼容OpenAI接口的API：
- ✅ OpenAI官方
- ✅ OneAPI（聚合）
- ✅ 通义千问
- ✅ 豆包
- ✅ DeepSeek
- ✅ 本地Ollama

详见：[CONFIG_GUIDE.md](CONFIG_GUIDE.md)

## 🎓 学习路径

### 新手（10分钟）
1. 安装依赖
2. 配置API
3. 运行程序
4. 尝试创建第一个文件

### 进阶（30分钟）
1. 阅读 QUICKSTART.md
2. 阅读 CONFIG_GUIDE.md
3. 理解两个版本的区别
4. 尝试批量操作

### 高级（1小时）
1. 阅读所有文档
2. 理解技术架构
3. 自定义配置
4. 用于实际项目

## 💡 使用技巧

### 技巧1：明确描述需求
```
❌ "修改这个文件"
✅ "修改 main.py，添加一个计算平均值的函数，使用类型注解"
```

### 技巧2：利用上下文
```
你: 读取 config.json
你: 基于这个配置，创建一个数据库连接类
```

### 技巧3：批量操作
```
你: 给所有Python文件添加类型注解和docstring
```

### 技巧4：刷新上下文
```
你: refresh  # 创建新文件后刷新项目上下文
```

## 🎯 实际应用场景

### 场景1：快速原型
```
你: 创建一个Flask API项目，包含用户和文章两个模型
```

### 场景2：代码重构
```
你: 重构 utils.py，按功能拆分成多个模块
```

### 场景3：添加测试
```
你: 为 calculator.py 创建完整的单元测试
```

### 场景4：文档生成
```
你: 给所有Python文件添加详细的docstring
```

## 📦 项目结构

```
langchain-script-ide/
├── script_ide.py              # 基础版
├── script_ide_enhanced.py     # 增强版（推荐）
├── config.py.example          # 配置模板
├── requirements.txt           # 依赖
├── run.sh / run.bat          # 启动脚本
├── START_HERE.md             # 本文件
├── CONFIG_GUIDE.md           # 配置指南
├── QUICKSTART.md             # 快速入门
└── [其他8个文档]
```

## 🔧 故障排除

### 问题：找不到config.py
```bash
cp config.py.example config.py
```

### 问题：API调用失败
1. 检查 API_KEY 是否正确
2. 检查 API_BASE_URL 是否正确
3. 确认账户余额充足

### 问题：模型不存在
修改 `config.py` 中的 `DEFAULT_MODEL`

## 🎉 准备好了吗？

现在就开始吧：

```bash
pip install -r requirements.txt
cp config.py.example config.py
# 编辑 config.py
python script_ide_enhanced.py
```

**第一句话：** "你好，帮我创建一个Python脚本"

---

## 📖 更多资源

- [完整功能说明](README.md)
- [配置详细指南](CONFIG_GUIDE.md) ⭐⭐⭐⭐⭐
- [自动检索机制说明](ANSWER_TO_YOUR_QUESTION.md) ⭐⭐⭐⭐⭐
- [版本对比](COMPARISON.md)
- [使用演示](DEMO.md)
- [项目总结](SUMMARY.md)

---

**🚀 开始你的AI驱动的编程之旅！**

有问题？所有答案都在文档中！ 📚
