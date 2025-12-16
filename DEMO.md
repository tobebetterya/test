# 使用演示

这是一个完整的使用演示，展示如何使用这个基于LangChain的脚本IDE。

## 🎬 演示场景

### 场景 1: 创建一个简单的待办事项管理器

**对话示例：**

```
你: 创建一个Python脚本 todo_manager.py，实现一个简单的待办事项管理器，支持添加、删除、列出和完成任务

AI助手: [分析需求]
AI助手: [调用write_file工具]
AI助手: 我已经创建了 todo_manager.py 文件，它包含以下功能：
- TodoManager类，用于管理待办事项
- add_task: 添加新任务
- remove_task: 删除任务
- list_tasks: 列出所有任务
- complete_task: 标记任务为已完成
- 命令行界面，可以交互式使用

你可以运行 python todo_manager.py 来使用它。
```

### 场景 2: 修改配置文件

**对话示例：**

```
你: 读取 examples/config.json 文件

AI助手: [调用read_file工具]
AI助手: 文件内容显示如下：
{
  "database": {
    "host": "localhost",
    ...
  }
  ...
}

你: 修改这个文件，把数据库端口改成3306，并添加一个新的section "email"，包含smtp服务器配置

AI助手: [调用write_file工具]
AI助手: 我已经修改了 config.json 文件，更改如下：
1. 数据库端口从5432改为3306
2. 添加了email配置section，包含：
   - smtp_host: smtp.gmail.com
   - smtp_port: 587
   - use_tls: true
```

### 场景 3: 批量创建文件

**对话示例：**

```
你: 我要创建一个简单的Web API项目，需要以下文件：
1. app.py - Flask应用主文件
2. models.py - 数据模型
3. routes.py - API路由
4. requirements.txt - 依赖列表

AI助手: [依次调用write_file工具创建4个文件]
AI助手: 我已经为你创建了一个完整的Flask API项目：

1. ✅ app.py - 主应用，包含：
   - Flask应用初始化
   - 数据库配置
   - 蓝图注册
   - 运行入口

2. ✅ models.py - 数据模型，包含：
   - User模型
   - Product模型
   - 使用SQLAlchemy

3. ✅ routes.py - API路由，包含：
   - 用户CRUD操作
   - 产品CRUD操作
   - RESTful API设计

4. ✅ requirements.txt - 依赖列表

项目已经可以运行了！使用以下命令启动：
pip install -r requirements.txt
python app.py
```

### 场景 4: 代码重构

**对话示例：**

```
你: 读取 examples/sample.py

AI助手: [显示文件内容]

你: 对这个文件进行重构：
1. 添加类型注解
2. 改进docstring格式，使用Google风格
3. 添加异常处理
4. 添加单元测试示例

AI助手: [调用write_file工具修改文件]
AI助手: 我已经完成了代码重构，主要改进：

1. ✅ 添加了类型注解：
   - 函数参数和返回值都有明确的类型
   - 使用typing模块的List等类型

2. ✅ 改进了docstring：
   - 使用Google风格的docstring
   - 包含Args、Returns、Raises等section

3. ✅ 添加了异常处理：
   - calculate_sum函数现在会检查输入类型
   - 适当的错误信息

4. ✅ 添加了单元测试：
   - 使用unittest框架
   - 测试所有主要功能

现在的代码更加健壮和专业了！
```

### 场景 5: 生成数据处理脚本

**对话示例：**

```
你: 创建一个数据分析脚本 analyze_data.py，要求：
- 读取CSV文件
- 计算基本统计信息（均值、中位数、标准差）
- 生成数据可视化图表
- 导出分析报告

AI助手: [调用write_file工具]
AI助手: 我已经创建了 analyze_data.py 脚本，功能包括：

1. DataAnalyzer类，提供以下方法：
   - load_csv(): 读取CSV文件
   - calculate_statistics(): 计算统计信息
   - generate_plots(): 生成多种图表（直方图、箱线图、散点图）
   - export_report(): 导出HTML格式报告

2. 使用的库：
   - pandas: 数据处理
   - numpy: 数值计算
   - matplotlib/seaborn: 数据可视化
   - jinja2: 报告生成

3. 命令行接口：
   python analyze_data.py input.csv --output report.html

使用前请安装依赖：pip install pandas numpy matplotlib seaborn jinja2
```

### 场景 6: 创建自动化脚本

**对话示例：**

```
你: 创建一个备份脚本 backup.py，功能：
- 压缩指定目录
- 添加时间戳到文件名
- 支持增量备份
- 发送通知（可选）

AI助手: [生成脚本]
AI助手: 已创建 backup.py 脚本，主要功能：

1. ✅ 完整备份：
   - 使用zipfile压缩目录
   - 文件名包含时间戳
   - 排除指定的文件/目录

2. ✅ 增量备份：
   - 只备份修改过的文件
   - 基于文件修改时间判断

3. ✅ 通知功能：
   - 支持邮件通知
   - 支持Slack webhook
   - 备份成功/失败都会通知

4. ✅ 配置文件：
   - backup_config.json
   - 可配置备份目录、排除规则等

使用方法：
python backup.py --source /path/to/source --dest /path/to/backup
python backup.py --config backup_config.json --incremental
```

## 💡 实用技巧演示

### 技巧 1: 逐步完善代码

```
你: 创建一个简单的计算器 calc.py
AI: [创建基础版本]

你: 添加科学计算功能
AI: [添加sin、cos、sqrt等函数]

你: 添加历史记录功能
AI: [添加命令历史]

你: 添加图形界面
AI: [使用tkinter创建GUI]
```

### 技巧 2: 学习新技术

```
你: 创建一个异步编程示例 async_example.py，演示asyncio的使用

AI: [创建详细的示例代码，包含注释说明]

你: 再创建一个对比文件 sync_example.py，展示同步版本，让我理解区别

AI: [创建同步版本，并添加性能对比]
```

### 技巧 3: 代码风格转换

```
你: 读取 old_style.py

你: 把这个Python 2代码转换成Python 3，使用现代的Python特性

AI: [转换代码，使用f-string、类型注解、pathlib等现代特性]
```

### 技巧 4: 添加文档和测试

```
你: 读取 my_module.py

你: 为这个模块添加完整的文档字符串和类型注解

AI: [添加文档]

你: 再创建一个测试文件 test_my_module.py

AI: [创建pytest测试文件]
```

## 🎯 高级应用场景

### 多文件项目创建

```
你: 创建一个完整的Python包项目结构，包名为mypackage，需要：
- setup.py
- README.md
- mypackage/__init__.py
- mypackage/core.py
- tests/test_core.py
- .gitignore

AI: [依次创建所有文件，形成完整的包结构]
```

### 配置文件管理

```
你: 列出所有JSON文件

AI: [列出文件]

你: 把所有JSON文件转换成YAML格式，保存在configs目录

AI: [转换并保存]
```

### 代码生成模板

```
你: 创建一个Django模型生成器 model_generator.py，输入表名和字段，自动生成models.py代码

AI: [创建代码生成工具]
```

## 📝 总结

这个IDE的强大之处在于：

1. **自然语言交互** - 用说话的方式编程
2. **上下文理解** - AI记住你的需求
3. **完整代码生成** - 不只是代码片段，而是完整可用的文件
4. **智能修改** - 理解意图，精确修改
5. **批量操作** - 一次性处理多个文件

开始探索吧，发挥你的创意！🚀
