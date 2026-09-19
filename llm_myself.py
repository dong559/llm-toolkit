import os
os.environ["NO_PROXY"] = "localhost,127.0.0.1,::1"
import logging
import ollama

# 日志配置
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def chat(messages: list,
         model: str = "deepseek-r1:1.5b",
         temperature: float = 0.8,
         max_tokens: int = 1000
         ) -> str:
    """调用ollama 本地大模型进行对话"""
    logger.info(f"正在调用模型{model}...")
    try:
        response = ollama.chat(
            model=model,
            messages=messages,
            options={
                "temperature": temperature,
                "num_predict": max_tokens
            }
        )
        logger.info("模型返回成功")
        content = response.get("message", {}).get("content", "")
        return content
    except Exception as e:
        logger.exception(f"调用模型{model}时发生异常: {str(e)}")
        raise e


if __name__ == "__main__":
    messages = [{"role": "user", "content": "你好"}]
    res = chat(messages)
    print("回答：", res)
