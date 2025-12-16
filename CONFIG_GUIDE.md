# 配置指南

## 📝 配置文件格式

本项目使用Python格式的配置文件 `config.py`，而不是传统的 `.env` 文件。

### 优势

✅ **类型安全** - Python原生格式，IDE有完整提示  
✅ **灵活配置** - 支持复杂数据结构（字典、列表等）  
✅ **易于维护** - 可以添加注释和文档  
✅ **版本控制** - 可以追踪配置变更历史（使用 .example 文件）

## 🚀 快速配置

### 1. 复制示例文件

```bash
cp config.py.example config.py
```

### 2. 编辑配置文件

打开 `config.py`，填入你的实际配置：

```python
# API配置
API_BASE_URL = "https://oneapi.qunhequnhe.com/v1"
API_KEY = "sk-Mg0kSuvqf6aasasasaasa121212121212121212222asasax"

# 可用的模型列表
AVAILABLE_MODELS = {
    "deepseek-r1-0528": "DeepSeek R1 模型",
    "qwen-plus-latest": "通义千问 Plus 最新版",
    "bge-m3-1024d": "BGE M3 嵌入模型",
    "doubao-seed-1.6": "豆包 Seed 1.6 模型"
}

# 默认使用的模型
DEFAULT_MODEL = "doubao-seed-1.6"

# LLM配置
TEMPERATURE = 0.7  # 生成温度，范围0-1，越高越随机
MAX_TOKENS = 4000  # 最大生成token数
```

## 🔧 配置项说明

### API配置

| 配置项 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| `API_BASE_URL` | str | API端点URL | `"https://api.openai.com/v1"` |
| `API_KEY` | str | API密钥 | `"sk-xxx..."` |

### 模型配置

| 配置项 | 类型 | 说明 |
|--------|------|------|
| `AVAILABLE_MODELS` | dict | 可用模型字典，键为模型ID，值为描述 |
| `DEFAULT_MODEL` | str | 默认使用的模型ID |

### LLM参数

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `TEMPERATURE` | float | 0.7 | 生成温度，0=确定性，1=随机性 |
| `MAX_TOKENS` | int | 4000 | 单次最大生成token数 |

## 🌐 支持的API服务商

本项目支持任何兼容OpenAI接口的API服务：

### 1. OpenAI 官方

```python
API_BASE_URL = "https://api.openai.com/v1"
API_KEY = "sk-your-openai-key"
DEFAULT_MODEL = "gpt-4o-mini"
```

### 2. OneAPI（聚合服务）

```python
API_BASE_URL = "https://oneapi.example.com/v1"
API_KEY = "sk-your-oneapi-key"
DEFAULT_MODEL = "gpt-4o-mini"  # 或其他支持的模型
```

### 3. 通义千问（阿里云）

```python
API_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
API_KEY = "sk-your-qwen-key"
DEFAULT_MODEL = "qwen-plus-latest"
```

### 4. 豆包（字节跳动）

```python
API_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
API_KEY = "your-doubao-key"
DEFAULT_MODEL = "doubao-seed-1.6"
```

### 5. DeepSeek

```python
API_BASE_URL = "https://api.deepseek.com/v1"
API_KEY = "sk-your-deepseek-key"
DEFAULT_MODEL = "deepseek-r1-0528"
```

### 6. 本地模型（Ollama）

```python
API_BASE_URL = "http://localhost:11434/v1"
API_KEY = "ollama"  # Ollama不需要真实key
DEFAULT_MODEL = "llama2"
```

## 🎯 模型选择建议

### 通用场景

```python
DEFAULT_MODEL = "gpt-4o-mini"  # 性价比高
TEMPERATURE = 0.7
```

### 代码生成（更精确）

```python
DEFAULT_MODEL = "deepseek-coder"
TEMPERATURE = 0.3  # 降低随机性
```

### 创意写作（更多样）

```python
DEFAULT_MODEL = "gpt-4"
TEMPERATURE = 0.9  # 提高创造性
```

### 快速原型（省钱）

```python
DEFAULT_MODEL = "qwen-plus-latest"
TEMPERATURE = 0.7
MAX_TOKENS = 2000  # 减少token消耗
```

## 🔒 安全注意事项

### 1. 不要提交配置文件

`config.py` 已在 `.gitignore` 中，不会被Git跟踪：

```bash
# 查看Git状态，确保config.py未被追踪
git status

# 如果不小心添加了，移除：
git rm --cached config.py
```

### 2. 使用示例文件

修改 `config.py.example` 作为模板：

```python
# config.py.example - 可以提交到Git
API_BASE_URL = "https://api.example.com/v1"
API_KEY = "your-api-key-here"  # 占位符
DEFAULT_MODEL = "model-name"
```

### 3. 环境变量覆盖（高级）

如果需要，可以在代码中添加环境变量支持：

```python
# config.py
import os

API_KEY = os.getenv("API_KEY", "fallback-key")
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
```

## 📊 配置验证

创建一个测试脚本检查配置：

```bash
# 创建 test_config.py
cat > test_config.py << 'EOF'
#!/usr/bin/env python3
try:
    import config
    print("✅ 配置文件加载成功")
    print(f"API端点: {config.API_BASE_URL}")
    print(f"默认模型: {config.DEFAULT_MODEL}")
    print(f"可用模型数: {len(config.AVAILABLE_MODELS)}")
except Exception as e:
    print(f"❌ 配置文件错误: {e}")
EOF

python3 test_config.py
```

## 🔄 动态切换模型

### 方法1：修改配置文件

编辑 `config.py`，修改 `DEFAULT_MODEL`，然后重启程序。

### 方法2：命令行参数（未来功能）

```bash
python script_ide.py --model deepseek-r1-0528
```

### 方法3：运行时切换（未来功能）

```python
你: 切换到 deepseek-r1 模型
AI: 已切换模型为 deepseek-r1-0528
```

## 🛠️ 故障排除

### 问题1：找不到config.py

```
错误: 未找到配置文件 config.py
```

**解决方案：**
```bash
cp config.py.example config.py
```

### 问题2：API密钥无效

```
Error: Invalid API key
```

**解决方案：**
1. 检查 `config.py` 中的 `API_KEY` 是否正确
2. 确认API服务商账户余额充足
3. 检查API端点URL是否正确

### 问题3：模型不存在

```
Error: Model not found
```

**解决方案：**
1. 确认 `DEFAULT_MODEL` 在API服务商中可用
2. 查看API服务商文档获取可用模型列表
3. 更新 `AVAILABLE_MODELS` 字典

### 问题4：请求超时

**解决方案：**
1. 检查网络连接
2. 尝试减少 `MAX_TOKENS`
3. 更换API端点

## 📚 更多配置示例

### 完整配置示例

```python
# config.py - 完整配置

# ===== API配置 =====
API_BASE_URL = "https://oneapi.example.com/v1"
API_KEY = "sk-xxxxx"

# ===== 模型配置 =====
AVAILABLE_MODELS = {
    # OpenAI
    "gpt-4o": "GPT-4 Optimized",
    "gpt-4o-mini": "GPT-4 Mini (推荐)",
    
    # 国产模型
    "qwen-plus-latest": "通义千问 Plus",
    "qwen-turbo-latest": "通义千问 Turbo",
    "doubao-seed-1.6": "豆包 Seed 1.6",
    
    # DeepSeek
    "deepseek-r1-0528": "DeepSeek R1",
    "deepseek-coder": "DeepSeek Coder",
    
    # 本地模型
    "llama2": "Llama 2 (本地)",
    "codellama": "Code Llama (本地)",
}

DEFAULT_MODEL = "gpt-4o-mini"

# ===== LLM参数 =====
TEMPERATURE = 0.7      # 创造性
MAX_TOKENS = 4000      # 最大输出
TOP_P = 0.95          # 核采样
FREQUENCY_PENALTY = 0  # 频率惩罚
PRESENCE_PENALTY = 0   # 存在惩罚

# ===== 代理配置 =====
USE_PROXY = False
PROXY_URL = "http://127.0.0.1:7890"

# ===== 工作空间配置 =====
DEFAULT_WORKSPACE = "./workspace"
MAX_FILE_SIZE_KB = 100
MAX_FILES_TO_READ = 10

# ===== 日志配置 =====
LOG_LEVEL = "INFO"
LOG_FILE = "script_ide.log"
```

## 🎓 最佳实践

1. **版本控制**: 只提交 `config.py.example`，不提交 `config.py`
2. **文档化**: 在配置文件中添加详细注释
3. **验证**: 启动前验证配置项的有效性
4. **备份**: 定期备份配置文件
5. **分环境**: 开发/生产环境使用不同配置

---

**配置完成后，运行程序：**

```bash
python script_ide_enhanced.py
```

享受基于你自定义API的智能编程体验！ 🚀
