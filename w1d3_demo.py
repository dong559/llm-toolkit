# ===================== 导入部分 =====================
# 【知识点1：dataclass】从dataclasses模块导入dataclass装饰器
# 作用：快速定义结构化数据类，不用手写复杂的初始化代码
from dataclasses import dataclass
# 【知识点2：requests库】导入requests第三方库
# 作用：Python发送HTTP请求的工具，相当于代码里的"浏览器"
import requests

print("【调试】代码开始执行") # 新增调试行，判断程序有没有启动

# ===================== 数据结构定义 =====================
# @dataclass 是装饰器，给下面的类自动添加初始化、打印等功能
# 对应课程要求：配合dataclass定义数据结构
@dataclass
class Message:
    """定义大模型消息的标准结构，每条消息都有角色和内容"""
    # role：消息角色，类型是字符串
    # 可选值：system（系统提示）、user（用户提问）、assistant（模型回答）
    role: str
    # content：消息的具体文本内容，类型是字符串
    content: str

# ===================== 核心函数（带完整类型注解） =====================
# 【知识点1：类型注解】完整写法：函数名(参数名: 参数类型) -> 返回值类型
# messages: list[Message]  → 参数messages是列表，列表里每个元素都是Message对象
# url: str                 → 参数url是字符串
# -> dict                  → 函数执行完会返回一个字典
def send_http_post(messages: list[Message], url: str) -> dict:
    """
    功能：向指定地址发送POST请求，携带消息数据，返回解析后的JSON
    :param messages: 消息列表，Message对象组成的数组
    :param url: 目标API的地址
    :return: 服务器返回的结果，Python字典格式
    """
    print("【调试】进入send_http_post函数，准备转换消息")

    # 步骤1：把Message对象转成字典
    # 原因：HTTP接口只能识别JSON字典，不能识别Python的类对象
    # __dict__ 是Python对象自带属性，自动把对象转成{"role":"xxx","content":"xxx"}
    message_dict_list = [msg.__dict__ for msg in messages]
    print("【调试】消息转换完成")

    # 步骤2：组装完整的请求体（JSON请求体）
    # 就是我们要发给服务器的全部数据，服务器会按约定的格式读取
    request_body = {
        "test_name": "W1D3_HTTP_POST测试",
        "messages": message_dict_list,
        "temperature": 0.7
    }
    print("【调试】请求体组装完成，准备发送POST请求")

    # 【知识点2：发送POST请求】
    # requests.post() 专门用来发POST请求
    # url= ：目标接口地址
    # json=：自动把Python字典转成JSON字符串，自动加请求头Content-Type:application/json
    response = requests.post(url=url, json=request_body, timeout=10)
    # timeout=10 ：10秒连不上服务器就直接报错，不会无限卡住

    # 可选：请求状态检查
    # 如果服务器返回错误（比如404、500），直接抛出异常，不用自己判断状态码
    response.raise_for_status()
    print("【调试】收到服务器响应")

    # 【知识点2：解析响应JSON】
    # .json() 把服务器返回的JSON文本，解析成Python字典
    # 这样我们就能用字典的方式取值
    result = response.json()
    # 返回解析后的结果，对应函数声明的 -> dict
    return result

# ===================== 程序入口（主程序） =====================
# Python固定写法：只有直接运行这个py文件时，下面的代码才会执行
# 如果被其他文件import，这部分不会运行
if __name__ == "__main__":
    print("【调试】进入主程序")
    # 目标API地址：httpbin公开测试接口，你发什么它就原封不动返回什么
    target_url = "https://httpbin.ceshiren.com/post"

    # 构造测试消息：创建2个Message对象，放进列表
    # 对应课程的system/user两条消息格式
    chat_messages = [
        Message(role="system", content="你是Python学习助手，回答要简洁"),
        Message(role="user", content="解释一下什么是POST请求")
    ]
    print("【调试】消息对象创建完成，准备调用请求函数")

    try:
        # 调用函数，发送请求，拿到返回结果
        api_result = send_http_post(chat_messages, target_url)
        # 打印完整返回结果
        print("===== httpbin 返回的完整JSON =====")
        print(api_result)
        # 单独打印我们发出去的数据，验证是否正确传递
        print("\n===== 我们发送的请求体（服务器收到的） =====")
        print(api_result["json"])
    except Exception as e:
        print(f"【错误捕获】程序出错：{e}")