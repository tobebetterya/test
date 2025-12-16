#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基于LangChain的增强版脚本IDE
启动时自动扫描项目结构并建立上下文
"""

import os
import sys
from pathlib import Path
from typing import List, Optional, Dict
from dotenv import load_dotenv
from colorama import Fore, Style, init

from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.tools import Tool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import SystemMessage, HumanMessage

# 初始化colorama
init(autoreset=True)

# 加载环境变量
load_dotenv()


class ProjectContext:
    """项目上下文管理器"""
    
    def __init__(self, workspace_dir: Path):
        self.workspace_dir = workspace_dir
        self.file_tree = []
        self.file_contents = {}
        self.project_summary = ""
        
    def scan_workspace(self, max_file_size_kb: int = 100, max_files_to_read: int = 10):
        """扫描工作空间并读取关键文件"""
        print(f"{Fore.YELLOW}🔍 正在扫描工作空间...{Style.RESET_ALL}")
        
        # 1. 构建文件树
        for item in self.workspace_dir.rglob("*"):
            if item.is_file():
                rel_path = item.relative_to(self.workspace_dir)
                self.file_tree.append(str(rel_path))
        
        print(f"{Fore.GREEN}✓ 发现 {len(self.file_tree)} 个文件{Style.RESET_ALL}")
        
        # 2. 读取关键文件（优先级：README、配置文件、小型代码文件）
        priority_patterns = [
            'README*', 'readme*',
            '*.md',
            'config.*', 'package.json', 'requirements.txt',
            '*.py', '*.js', '*.ts',
            '*.json', '*.yaml', '*.yml', '*.toml'
        ]
        
        files_read = 0
        for pattern in priority_patterns:
            if files_read >= max_files_to_read:
                break
                
            for file_path_str in self.file_tree:
                if files_read >= max_files_to_read:
                    break
                    
                file_path = self.workspace_dir / file_path_str
                
                # 匹配模式
                if not any(file_path.match(pat) for pat in [pattern]):
                    continue
                
                # 检查文件大小
                try:
                    file_size_kb = file_path.stat().st_size / 1024
                    if file_size_kb > max_file_size_kb:
                        continue
                    
                    # 读取文件
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        self.file_contents[file_path_str] = content
                        files_read += 1
                        print(f"{Fore.CYAN}  ↳ 读取: {file_path_str}{Style.RESET_ALL}")
                        
                except Exception as e:
                    continue
        
        print(f"{Fore.GREEN}✓ 已读取 {files_read} 个关键文件{Style.RESET_ALL}")
        
    def generate_summary(self) -> str:
        """生成项目摘要"""
        summary_parts = []
        
        # 文件树概览
        summary_parts.append("## 项目结构")
        summary_parts.append(f"工作空间包含 {len(self.file_tree)} 个文件：")
        
        # 按类型分组
        file_types = {}
        for file_path in self.file_tree:
            ext = Path(file_path).suffix or '(无扩展名)'
            file_types[ext] = file_types.get(ext, 0) + 1
        
        for ext, count in sorted(file_types.items(), key=lambda x: x[1], reverse=True):
            summary_parts.append(f"  - {ext}: {count} 个文件")
        
        # 文件列表（分层显示）
        summary_parts.append("\n## 文件列表")
        for file_path in sorted(self.file_tree)[:50]:  # 最多显示50个
            summary_parts.append(f"  - {file_path}")
        
        if len(self.file_tree) > 50:
            summary_parts.append(f"  ... 还有 {len(self.file_tree) - 50} 个文件")
        
        # 已读取文件的摘要
        if self.file_contents:
            summary_parts.append("\n## 已读取的关键文件")
            for file_path in self.file_contents.keys():
                summary_parts.append(f"  - {file_path}")
        
        return "\n".join(summary_parts)
    
    def get_context_for_agent(self) -> str:
        """获取传递给Agent的上下文"""
        context_parts = [
            "# 项目上下文信息",
            "",
            self.generate_summary()
        ]
        
        # 添加重要文件的内容片段
        if self.file_contents:
            context_parts.append("\n## 关键文件内容预览")
            for file_path, content in list(self.file_contents.items())[:5]:  # 最多5个文件
                context_parts.append(f"\n### {file_path}")
                # 只显示前500字符
                preview = content[:500]
                if len(content) > 500:
                    preview += "\n... (内容已截断)"
                context_parts.append(f"```\n{preview}\n```")
        
        return "\n".join(context_parts)


class EnhancedScriptIDE:
    """增强版脚本IDE - 带项目上下文感知"""
    
    def __init__(self, workspace_dir: str = "./workspace", enable_auto_scan: bool = True):
        """初始化IDE
        
        Args:
            workspace_dir: 工作空间目录
            enable_auto_scan: 是否启动时自动扫描项目
        """
        self.workspace_dir = Path(workspace_dir)
        self.workspace_dir.mkdir(exist_ok=True)
        
        # 初始化LLM
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print(f"{Fore.RED}错误: 未设置OPENAI_API_KEY环境变量{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}请创建.env文件并设置: OPENAI_API_KEY=your_api_key{Style.RESET_ALL}")
            sys.exit(1)
            
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            api_key=api_key
        )
        
        # 项目上下文
        self.project_context = ProjectContext(self.workspace_dir)
        if enable_auto_scan and any(self.workspace_dir.iterdir()):
            self.project_context.scan_workspace()
        
        # 创建工具
        self.tools = self._create_tools()
        
        # 创建提示模板（包含项目上下文）
        system_message_content = f"""你是一个智能脚本IDE助手，可以帮助用户管理和修改脚本文件。

你的能力包括：
1. 读取文件内容
2. 修改现有文件
3. 创建新文件
4. 列出工作空间中的所有文件
5. 删除文件
6. 刷新项目上下文（重新扫描工作空间）

重要：你已经获得了项目的上下文信息，包括文件结构和关键文件内容。
当用户提出涉及多个文件或整个项目的需求时，你可以直接引用这些信息，无需每次都重新读取。

当然，如果用户询问的具体文件你还没有完整内容，可以使用read_file工具读取。

当用户要求修改文件时：
1. 如果已有上下文，直接使用；否则先读取文件
2. 理解用户的修改需求
3. 生成修改后的完整内容
4. 使用write_file工具保存修改

当用户要求创建新文件时：
1. 参考项目现有的代码风格和结构
2. 生成符合项目规范的代码
3. 使用write_file工具创建文件

请始终确保代码的正确性和完整性。用中文回复用户。

{self.project_context.get_context_for_agent() if self.project_context.file_tree else "（工作空间为空，尚无项目上下文）"}
"""
        
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=system_message_content),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # 创建记忆
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # 创建agent
        self.agent = create_openai_tools_agent(self.llm, self.tools, self.prompt)
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            max_iterations=10
        )
    
    def _create_tools(self) -> List[Tool]:
        """创建工具列表"""
        
        def read_file(filename: str) -> str:
            """读取文件内容"""
            try:
                file_path = self.workspace_dir / filename
                if not file_path.exists():
                    return f"错误: 文件 {filename} 不存在"
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return f"文件 {filename} 的内容:\n\n{content}"
            except Exception as e:
                return f"读取文件时出错: {str(e)}"
        
        def write_file(filename_and_content: str) -> str:
            """写入或创建文件
            
            参数格式: filename|||content
            使用|||作为文件名和内容的分隔符
            """
            try:
                if "|||" not in filename_and_content:
                    return "错误: 参数格式不正确。请使用格式: filename|||content"
                
                filename, content = filename_and_content.split("|||", 1)
                filename = filename.strip()
                
                file_path = self.workspace_dir / filename
                file_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                return f"成功写入文件: {filename}"
            except Exception as e:
                return f"写入文件时出错: {str(e)}"
        
        def list_files(directory: str = ".") -> str:
            """列出工作空间中的文件"""
            try:
                target_dir = self.workspace_dir / directory
                if not target_dir.exists():
                    return f"错误: 目录 {directory} 不存在"
                
                files = []
                for item in target_dir.rglob("*"):
                    if item.is_file():
                        rel_path = item.relative_to(self.workspace_dir)
                        files.append(str(rel_path))
                
                if not files:
                    return "工作空间中没有文件"
                
                return "工作空间中的文件:\n" + "\n".join(f"- {f}" for f in sorted(files))
            except Exception as e:
                return f"列出文件时出错: {str(e)}"
        
        def delete_file(filename: str) -> str:
            """删除文件"""
            try:
                file_path = self.workspace_dir / filename
                if not file_path.exists():
                    return f"错误: 文件 {filename} 不存在"
                
                file_path.unlink()
                return f"成功删除文件: {filename}"
            except Exception as e:
                return f"删除文件时出错: {str(e)}"
        
        def refresh_context() -> str:
            """刷新项目上下文（重新扫描工作空间）"""
            try:
                print(f"\n{Fore.YELLOW}🔄 刷新项目上下文...{Style.RESET_ALL}")
                self.project_context = ProjectContext(self.workspace_dir)
                self.project_context.scan_workspace()
                
                # 更新system prompt
                # 注意：这里只返回消息，实际的prompt更新需要重启对话
                return "项目上下文已刷新！已重新扫描工作空间并读取关键文件。"
            except Exception as e:
                return f"刷新上下文时出错: {str(e)}"
        
        return [
            Tool(
                name="read_file",
                func=read_file,
                description="读取文件内容。输入: 文件名（相对于工作空间的路径）"
            ),
            Tool(
                name="write_file",
                func=write_file,
                description="写入或创建文件。输入格式: filename|||content（使用|||分隔文件名和内容）"
            ),
            Tool(
                name="list_files",
                func=list_files,
                description="列出工作空间中的所有文件。输入: 目录路径（默认为当前目录）"
            ),
            Tool(
                name="delete_file",
                func=delete_file,
                description="删除指定文件。输入: 文件名（相对于工作空间的路径）"
            ),
            Tool(
                name="refresh_context",
                func=refresh_context,
                description="刷新项目上下文，重新扫描工作空间。当有新文件创建或需要更新项目信息时使用。"
            )
        ]
    
    def run(self):
        """运行IDE交互界面"""
        print(f"{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}欢迎使用增强版LangChain脚本IDE")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}工作空间: {self.workspace_dir.absolute()}{Style.RESET_ALL}")
        
        if self.project_context.file_tree:
            print(f"{Fore.GREEN}✓ 已加载项目上下文: {len(self.project_context.file_tree)} 个文件{Style.RESET_ALL}")
            print(f"{Fore.GREEN}✓ 已读取: {len(self.project_context.file_contents)} 个关键文件{Style.RESET_ALL}")
        
        print(f"\n{Fore.YELLOW}增强功能：")
        print(f"  ✨ 自动扫描项目结构")
        print(f"  ✨ 预加载关键文件内容")
        print(f"  ✨ 智能理解项目上下文")
        print(f"  ✨ 无需每次手动列出文件{Style.RESET_ALL}")
        
        print(f"\n{Fore.YELLOW}你可以通过对话来：")
        print(f"  - 直接询问项目相关问题（无需先列出文件）")
        print(f"  - 读取和修改脚本文件")
        print(f"  - 创建新的脚本文件")
        print(f"  - 批量处理多个文件")
        print(f"  - 刷新项目上下文{Style.RESET_ALL}")
        
        print(f"\n{Fore.YELLOW}特殊命令：")
        print(f"  - 'refresh' 或 '刷新': 重新扫描项目")
        print(f"  - 'context' 或 '上下文': 显示当前项目信息")
        print(f"  - 'exit' 或 'quit': 退出程序{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
        
        while True:
            try:
                # 获取用户输入
                user_input = input(f"{Fore.GREEN}你: {Style.RESET_ALL}").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['exit', 'quit', '退出']:
                    print(f"\n{Fore.CYAN}再见！{Style.RESET_ALL}")
                    break
                
                # 特殊命令处理
                if user_input.lower() in ['context', '上下文', 'info', '信息']:
                    print(f"\n{Fore.BLUE}当前项目信息：{Style.RESET_ALL}")
                    print(self.project_context.generate_summary())
                    print()
                    continue
                
                if user_input.lower() in ['refresh', '刷新', 'rescan', '重新扫描']:
                    self.project_context = ProjectContext(self.workspace_dir)
                    self.project_context.scan_workspace()
                    print(f"{Fore.GREEN}✓ 项目上下文已刷新{Style.RESET_ALL}\n")
                    continue
                
                # 执行agent
                print(f"\n{Fore.BLUE}AI助手: {Style.RESET_ALL}", end="")
                response = self.agent_executor.invoke({"input": user_input})
                print(f"{response['output']}\n")
                
            except KeyboardInterrupt:
                print(f"\n\n{Fore.CYAN}再见！{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"\n{Fore.RED}错误: {str(e)}{Style.RESET_ALL}\n")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="增强版LangChain脚本IDE（带项目上下文感知）")
    parser.add_argument(
        "--workspace",
        type=str,
        default="./workspace",
        help="工作空间目录（默认: ./workspace）"
    )
    parser.add_argument(
        "--no-scan",
        action="store_true",
        help="禁用启动时自动扫描"
    )
    
    args = parser.parse_args()
    
    # 创建并运行IDE
    ide = EnhancedScriptIDE(
        workspace_dir=args.workspace,
        enable_auto_scan=not args.no_scan
    )
    ide.run()


if __name__ == "__main__":
    main()
