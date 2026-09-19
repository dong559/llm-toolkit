# llm_client.py
import os
# 本地开发兜底：避免 Clash 等系统代理把 localhost:11434 的请求转发走导致 502
os.environ["NO_PROXY"] = "localhost,127.0.0.1,::1"
import logging
from openai import OpenAI, APIError, APIConnectionError, NotFoundError

# ========== 日志配置 ==========
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# ========= Ollama本地配置 =========
client = OpenAI(
    api_key="dummy_key",
    base_url="http://localhost:11434/v1"
)
MODEL_NAME = "qwen2.5-coder:7b"


def chat(messages, temperature=0.7, max_tokens=512):
    """
    大模型对话函数
    :param messages: 消息列表 [{"role":"user", "content":"xxx"}]
    :param temperature: 0=最确定，1=创造力强
    :param max_tokens: 最大输出token
    :return: 模型返回的文本，出错返回None
    """
    try:
        logger.info(f"发送请求到模型: {MODEL_NAME}, temperature={temperature}")
        resp = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=30  # 超时30秒
        )
        result = resp.choices[0].message.content
        logger.info(f"模型返回成功，长度: {len(result)} 字符")
        return result

    except APIConnectionError as e:
        logger.error(f"连接Ollama失败！请确认 ollama serve 已启动: {e}")
        return None
    except NotFoundError as e:
        logger.error(f"模型不存在！请检查MODEL_NAME是否正确，或 ollama pull 模型: {e}")
        return None
    except APIError as e:
        logger.error(f"API报错: {e}")
        return None
    except Exception as e:
        logger.error(f"未知错误: {e}")
        return None


if __name__ == "__main__":
    # 练习①：英文翻译成中文
    print("=====练习1：英译中=====")
    msg1 = [
        {"role": "system", "content": "你是专业翻译，把下面英文翻译成通顺中文，只输出翻译结果。"},
        {"role": "user", "content": "Large language models can understand natural language and generate human-like text."}
    ]
    res1 = chat(msg1, temperature=0)
    print(res1 if res1 else "翻译失败")

    # 练习②：文章摘要
    print("\n=====练习2：文章摘要=====")
    article = """
    Python是一门解释型高级编程语言，语法简洁易读。它拥有丰富第三方库，
    在数据分析、AI大模型、web开发领域广泛使用。很多初学者都会选择Python作为第一门编程语言。
    """
    msg2 = [
        {"role": "system", "content": "对用户输入的文本做简短摘要，控制在50字以内，只输出摘要。"},
        {"role": "user", "content": article}
    ]
    res2 = chat(msg2, temperature=0)
    print(res2 if res2 else "摘要失败")

    # 练习③：代码解释
    print("\n=====练习3：代码解释=====")
    code = "def add(a,b):\n    return a + b"
    msg3 = [
        {"role": "system", "content": "解释下面这段Python代码的作用，通俗易懂。"},
        {"role": "user", "content": code}
    ]
    res3 = chat(msg3, temperature=0)
    print(res3 if res3 else "解释失败")

    # 调试对比 temperature
    print("\n=====对比 temperature=0 vs temperature=1 =====")
    test_msg = [{"role": "user", "content": "写一句描写春天的短句"}]
    print("temperature=0：", chat(test_msg, temperature=0, max_tokens=32) or "失败")
    print("temperature=1：", chat(test_msg, temperature=1, max_tokens=32) or "失败")
