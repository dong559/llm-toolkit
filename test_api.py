import os
os.environ["NO_PROXY"] = "localhost,127.0.0.1,::1"
import ollama


print("开始连接")


models = ollama.list()

print(models)