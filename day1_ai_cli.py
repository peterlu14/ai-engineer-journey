import requests

LLM_URL = "http://192.168.3.2:11434/api/chat"
# MODEL = "llama3.2:3b"
MODEL = "qwen3.5:9b-nothink"

messages = []
SYSTEM_PROMPT = {
    "role": "system",
    "content": "你是一個有用的助理，請用繁體中文回答。"
}

def chat(messages):
    payload = {
        "model": MODEL,
        "messages": [SYSTEM_PROMPT] + messages,
        "stream": False,
        "think": False
    }
    print(payload)
    response = requests.post(LLM_URL, json = payload)
    print(response)
    return  response.json()["message"]["content"]

def build_context(messages, max_turn = 5):
    return messages[-10:]

while True:
    print("------------------------------------------------")
    user_input = input("你: ")

    if user_input.lower() == "exit":
        break

    messages.append({"role":"user","content":user_input})
    messages = build_context(messages)
    reply = chat(messages)

    messages.append({"role":"assistant","content":reply})

    
    print(f"Ai: {reply}")