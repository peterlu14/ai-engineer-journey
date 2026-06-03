import json
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

LLM_URL = "http://192.168.3.2:8080/v1/chat/completions"
MODEL = "qwen3.6"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_weather(city: str) -> str:
    fake_data = {
        "台北": "晴天，25°C",
        "高雄": "多雲，28°C",
        "台中": "陰天，22°C",
    }
    return fake_data.get(city, "查無此城市資料")

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查詢台灣城市的天氣",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名稱，例如台北"}
                },
                "required": ["city"]
            }
        }
    }
]

class AskRequest(BaseModel):
    question: str

def stream_llm(messages):
    response = requests.post(LLM_URL, json={
        "model": MODEL,
        "messages": messages,
        "stream": True
    }, stream=True)
    for line in response.iter_lines():
        if line:
            line = line.decode("utf-8") if isinstance(line, bytes) else line
            if line.startswith("data: "):
                line = line[6:]
            if line == "[DONE]":
                break
            data = json.loads(line)
            content = data["choices"][0]["delta"].get("content", "")
            if content:
                yield content

@app.post("/ask")
def ask(req: AskRequest):
    messages = [{"role": "user", "content": req.question}]

    # 第一次非 stream：需要完整 response 才能判斷有沒有 tool_calls
    response = requests.post(LLM_URL, json={
        "model": MODEL,
        "messages": messages,
        "tools": tools,
        "stream": False
    })
    message = response.json()["choices"][0]["message"]

    if message.get("tool_calls"):
        tool_call = message["tool_calls"][0]
        func_args = json.loads(tool_call["function"]["arguments"])
        tool_result = get_weather(**func_args)

        messages.append(message)
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call["id"],
            "content": tool_result
        })

        # 第二次 stream：把工具結果丟回給 LLM，串流回應
        return StreamingResponse(stream_llm(messages), media_type="text/plain")

    # 直接回答：已有結果，包成單一 chunk 串流
    return StreamingResponse(iter([message["content"]]), media_type="text/plain")
