from llm_client import chat


messages=[
    {
        "role":"user",
        "content":"介绍一下人工智能"
    }
]


answer = chat(messages)


print(answer)