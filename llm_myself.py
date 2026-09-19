import os
# 本地开发兜底：Clash/V2Ray 等系统代理会把 localhost 请求转发走，导致 ollama 返回 502
# 让 httpx 对本地地址直连，不经过代理
os.environ["NO_PROXY"] = "localhost,127.0.0.1,::1"

import ollama


def chat(messages, temperature=0.8, max_tokens=1000):

    print("正在调用模型...")

    response = ollama.chat(
        model="deepseek-r1:1.5b",
        messages=messages,
        options={
            "temperature": temperature,
            "num_predict": max_tokens
        }
    )

    print("模型返回成功")

    return response["message"]["content"]