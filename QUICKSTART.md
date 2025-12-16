# 快速开始指南

## 🎯 5分钟上手

### 第一步：安装依赖

```bash
pip install -r requirements.txt
```

### 第二步：配置API

1. 复制配置文件：
```bash
cp config.py.example config.py
```

2. 编辑 `config.py` 文件，填入你的API配置：
```python
# API配置
API_BASE_URL = "https://your-api-endpoint.com/v1"
API_KEY = "your-api-key-here"

# 可用的模型列表
AVAILABLE_MODELS = {
    "deepseek-r1-0528": "DeepSeek R1 模型",
    "qwen-plus-latest": "通义千问 Plus 最新版",
    "doubao-seed-1.6": "豆包 Seed 1.6 模型"
}

# 默认使用的模型
DEFAULT_MODEL = "doubao-seed-1.6"
```

> 💡 支持兼容OpenAI接口的任何API服务（如OneAPI、通义千问、豆包等）

### 第三步：运行程序

```bash
python script_ide.py
```

你会看到：

```
============================================================
欢迎使用基于LangChain的简易脚本IDE
============================================================
工作空间: /path/to/workspace

你可以通过对话来：
  - 读取和修改脚本文件
  - 创建新的脚本文件
  - 列出所有文件
  - 删除文件

输入 'exit' 或 'quit' 退出程序
============================================================

你: 
```

## 💬 试试这些命令

### 1️⃣ 列出所有文件

```
你: 列出所有文件
```

或者：

```
你: 显示工作空间中有哪些文件
```

### 2️⃣ 读取文件

```
你: 读取 examples/sample.py
```

### 3️⃣ 创建新文件

```
你: 创建一个Python脚本 calculator.py，实现加减乘除四个函数
```

或者：

```
你: 帮我写一个 todo.py，用来管理待办事项的命令行工具
```

### 4️⃣ 修改文件

```
你: 修改 examples/sample.py，添加一个计算平均值的函数
```

或者：

```
你: 把 examples/config.json 中的 debug 改成 true
```

### 5️⃣ 复杂任务

```
你: 创建一个web爬虫 scraper.py，使用requests库爬取网页内容
```

```
你: 创建一个Flask应用 app.py，有两个路由：首页和关于页面
```

## 🎨 实际使用场景

### 场景1：快速原型开发

```
你: 创建一个简单的博客系统，需要三个文件：
1. models.py - 数据模型（文章、用户、评论）
2. routes.py - API路由
3. config.py - 配置文件
```

AI会一步步帮你创建这些文件。

### 场景2：代码重构

```
你: 读取 examples/sample.py

你: 把所有函数改成使用type hints，并添加更详细的docstring
```

### 场景3：批量修改

```
你: 列出所有.py文件

你: 给每个Python文件添加shebang和编码声明
```

### 场景4：学习和探索

```
你: 创建一个示例文件 async_demo.py，演示Python中的异步编程

你: 再创建一个 decorator_demo.py，展示常用的装饰器模式
```

## 🔥 高级技巧

### 技巧1：上下文对话

AI会记住对话历史，你可以这样：

```
你: 创建一个简单的类 Person
你: 给它添加一个方法 introduce
你: 再添加一个类方法用于从字典创建实例
```

### 技巧2：引用之前的内容

```
你: 读取 sample.py
你: 基于这个文件的风格，创建一个类似的 math_utils.py
```

### 技巧3：增量修改

```
你: 创建 app.py，一个简单的Flask应用
你: 添加数据库支持
你: 添加用户认证
你: 添加日志记录
```

## ⚠️ 常见问题

### Q: 提示"未找到配置文件 config.py"？
A: 确保复制了 `config.py.example` 为 `config.py` 并正确配置了API。

### Q: API调用失败？
A: 检查网络连接，确保可以访问OpenAI API。

### Q: 生成的代码不符合预期？
A: 尝试更详细地描述需求，或者分步骤完成。

### Q: 文件被覆盖了？
A: 修改文件会覆盖原内容，建议先备份重要文件。

### Q: 支持中文文件名吗？
A: 支持，但建议使用英文文件名以避免编码问题。

## 📚 下一步

- 查看 `README.md` 了解更多功能
- 阅读 `script_ide.py` 源码了解实现原理
- 自定义工具函数扩展IDE能力
- 尝试不同的提示词，探索AI的能力边界

## 🎉 开始创作吧！

现在你已经掌握了基础用法，尽情发挥创意，让AI帮你编写代码吧！

---

有问题？欢迎提Issue！ 🚀
