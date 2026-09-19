from llm_myself import chat


messages=[
    {
        "role":"user",
        "content":"介绍一下人工智能"
    }
]


answer = chat(
    messages,
    temperature=0,
    max_tokens=500
)


print(answer)