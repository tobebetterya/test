# 更新日志

## [v1.1.0] - 2025-12-16

### ✨ 新增功能

- **Python格式配置文件**: 从 `.env` 迁移到 `config.py`
  - 支持复杂数据结构（字典、列表）
  - 更好的IDE支持和类型提示
  - 可以添加注释和文档
  
- **多模型支持**: 
  - 可配置多个可用模型
  - 支持任何兼容OpenAI接口的API服务商
  - 包括：OpenAI、OneAPI、通义千问、豆包、DeepSeek等
  
- **详细配置指南**: 新增 `CONFIG_GUIDE.md` 文档
  - 完整的配置说明
  - 各大API服务商配置示例
  - 故障排除指南

### 🔧 改进

- **配置加载优化**: 使用Python模块导入代替环境变量
- **错误提示改进**: 更友好的配置错误提示信息
- **启动脚本更新**: 检查 `config.py` 而不是 `.env`
- **文档更新**: 所有文档更新为新的配置方式

### 🗑️ 移除

- 移除 `python-dotenv` 依赖
- 移除 `.env.example` 文件
- 移除环境变量加载逻辑

### 📝 配置文件格式变更

**旧格式 (.env):**
```bash
OPENAI_API_KEY=sk-xxx
```

**新格式 (config.py):**
```python
# API配置
API_BASE_URL = "https://api.example.com/v1"
API_KEY = "sk-xxx"

# 可用的模型列表
AVAILABLE_MODELS = {
    "model-1": "模型1描述",
    "model-2": "模型2描述"
}

# 默认模型
DEFAULT_MODEL = "model-1"

# LLM参数
TEMPERATURE = 0.7
MAX_TOKENS = 4000
```

### 🔄 迁移指南

如果你使用的是旧版本：

```bash
# 1. 更新代码
git pull

# 2. 重新安装依赖（移除了python-dotenv）
pip install -r requirements.txt

# 3. 创建新配置文件
cp config.py.example config.py

# 4. 迁移配置
# 将你的 .env 文件中的 OPENAI_API_KEY 
# 迁移到 config.py 的 API_KEY

# 5. 删除旧配置文件（可选）
rm .env
```

---

## [v1.0.0] - 2025-12-16

### 🎉 首次发布

- **基础版IDE** (`script_ide.py`)
  - 文件读取、写入、列出、删除
  - LangChain Agent驱动
  - 对话式交互

- **增强版IDE** (`script_ide_enhanced.py`)
  - 启动时自动扫描项目
  - 预加载关键文件
  - 智能上下文感知
  - 项目结构分析

- **完整文档**
  - README.md - 项目主文档
  - QUICKSTART.md - 快速入门
  - COMPARISON.md - 版本对比
  - ENHANCED_FEATURES.md - 增强功能
  - DEMO.md - 使用演示
  - PROJECT_OVERVIEW.md - 技术架构
  - ANSWER_TO_YOUR_QUESTION.md - 核心问题解答
  - FILE_LIST.md - 文件清单

- **跨平台支持**
  - Linux/Mac启动脚本 (run.sh)
  - Windows启动脚本 (run.bat)

- **示例文件**
  - Python脚本示例
  - JSON配置示例
  - 说明文档

### 🛠️ 技术栈

- LangChain >= 0.1.0
- LangChain-OpenAI >= 0.0.2
- Colorama >= 0.4.6
- Python 3.7+

---

## 🔮 未来计划

### v1.2.0 (计划中)
- [ ] 命令行参数动态选择模型
- [ ] 运行时模型切换
- [ ] 增量项目扫描
- [ ] 文件变化监听

### v1.3.0 (计划中)
- [ ] Git集成
- [ ] 代码diff预览
- [ ] 操作历史和撤销
- [ ] 文件夹操作支持

### v2.0.0 (规划中)
- [ ] Web界面
- [ ] 多用户支持
- [ ] 插件系统
- [ ] 更多LLM提供商支持

---

## 💬 反馈

遇到问题？有建议？欢迎提交Issue！

感谢使用！ 🚀
