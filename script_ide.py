#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基于LangChain的简易脚本IDE
可以通过对话来读取、修改和生成脚本文件
"""

import os
import sys
from pathlib import Path
from typing import List, Optional
from colorama import Fore, Style, init

from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.tools import Tool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import SystemMessage

# 初始化colorama
init(autoreset=True)

# 加载配置文件
def load_config():
    """加载配置文件"""
    config_file = Path(__file__).parent / "config.py"
    if not config_file.exists():
        print(f"{Fore.RED}错误: 未找到配置文件 config.py{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}请复制 config.py.example 为 config.py 并填入你的配置{Style.RESET_ALL}")
        sys.exit(1)
    
    # 导入配置
    import importlib.util
    spec = importlib.util.spec_from_file_location("config", config_file)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)
    return config

config = load_config()


class ScriptIDE:
    """基于LangChain的脚本IDE"""
    
    def __init__(self, workspace_dir: str = "./workspace"):
        """初始化IDE
        
        Args:
            workspace_dir: 工作空间目录
        """
        self.workspace_dir = Path(workspace_dir)
        self.workspace_dir.mkdir(exist_ok=True)
        
        # 初始化LLM
        if not hasattr(config, 'API_KEY') or not config.API_KEY or config.API_KEY.startswith("sk-"):
            print(f"{Fore.YELLOW}提示: 请在 config.py 中配置你的 API_KEY{Style.RESET_ALL}")
        
        api_base = getattr(config, 'API_BASE_URL', None)
        api_key = getattr(config, 'API_KEY', None)
        model = getattr(config, 'DEFAULT_MODEL', 'gpt-4o-mini')
        temperature = getattr(config, 'TEMPERATURE', 0.7)
        max_tokens = getattr(config, 'MAX_TOKENS', 4000)
        
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            api_key=api_key,
            base_url=api_base
        )
        
        print(f"{Fore.CYAN}使用模型: {model}{Style.RESET_ALL}")
        if hasattr(config, 'AVAILABLE_MODELS') and model in config.AVAILABLE_MODELS:
            print(f"{Fore.CYAN}模型说明: {config.AVAILABLE_MODELS[model]}{Style.RESET_ALL}")
        
        # 创建工具
        self.tools = self._create_tools()
        
        # 创建提示模板
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""你是一个智能脚本IDE助手，可以帮助用户管理和修改脚本文件。

你的能力包括：
1. 读取文件内容
2. 修改现有文件
3. 创建新文件
4. 列出工作空间中的所有文件
5. 删除文件

当用户要求修改文件时，你需要：
1. 先读取文件内容
2. 理解用户的修改需求
3. 生成修改后的完整内容
4. 使用write_file工具保存修改

当用户要求创建新文件时，你需要：
1. 理解用户的需求
2. 生成完整的文件内容
3. 使用write_file工具创建文件

请始终确保代码的正确性和完整性。用中文回复用户。"""),
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
            )
        ]
    
    def run(self):
        """运行IDE交互界面"""
        print(f"{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}欢迎使用基于LangChain的简易脚本IDE")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}工作空间: {self.workspace_dir.absolute()}{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}你可以通过对话来：")
        print(f"  - 读取和修改脚本文件")
        print(f"  - 创建新的脚本文件")
        print(f"  - 列出所有文件")
        print(f"  - 删除文件{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}输入 'exit' 或 'quit' 退出程序{Style.RESET_ALL}")
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
    
    parser = argparse.ArgumentParser(description="基于LangChain的简易脚本IDE")
    parser.add_argument(
        "--workspace",
        type=str,
        default="./workspace",
        help="工作空间目录（默认: ./workspace）"
    )
    
    args = parser.parse_args()
    
    # 创建并运行IDE
    ide = ScriptIDE(workspace_dir=args.workspace)
    ide.run()


if __name__ == "__main__":
    main()
