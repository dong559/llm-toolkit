# llm-toolkit

一个基于 Python 调用本地 LLM 模型的工具包。

## 项目介绍

本项目封装了大语言模型调用接口，
支持通过 Python 调用本地 Ollama 模型，实现简单的 AI 对话功能。

## 功能

- 支持 LLM 对话
- 支持自定义 messages
- 支持 temperature 参数
- 支持 token 数量控制
- 简化本地模型调用流程

## 项目结构
llm-toolkit
│
├── llm_client.py # LLM客户端封装
├── llm_myself.py # 自定义聊天接口
├── test.py # 基础测试
├── test_api.py # API测试
├── test_client.py # 客户端测试
└── w1d3_demo.py # 示例代码

## 环境要求

Python 3.12+

安装依赖：
pip install ollama

## 使用方法

运行：python test_client.py

示例：

```python
messages=[
    {
        "role":"user",
        "content":"介绍一下人工智能"
    }
]

answer = chat(messages)

print(answer)
技术栈
- Python
- Ollama
- Large Language Model
- Git/GitHub
最后提醒国内挂梯子使用时候要改一下  os.environ["NO_PROXY"] = "localhost,your computer addresss"
