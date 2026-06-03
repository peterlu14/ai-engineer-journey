import json
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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


# ── 工具實作 ──────────────────────────────────────────────
def get_weather(city: str) -> str:
    fake_data = {
        "台北": "晴天，25°C",
        "高雄": "多雲，28°C",
        "台中": "陰天，22°C",
    }
    return fake_data.get(city, "查無此城市資料")


def calculate(expression: str) -> str:
    try:
        return str(eval(expression))
    except Exception:
        return "計算失敗"


# 工具名稱 → 實際函式 的對照表（dispatch table）
# loop 裡用這個來呼叫對應的工具，不用寫一堆 if/else
TOOL_FUNCS = {
    "get_weather": get_weather,
    "calculate": calculate,
}

# 給 LLM 看的工具定義
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
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "計算數學算式，例如 24 * 7",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "數學算式字串，例如 '24 * 7'"}
                },
                "required": ["expression"],
            },
        },
    },
]


class AskRequest(BaseModel):
    question: str


def call_llm(messages):
    """非 stream 呼叫 LLM，回傳完整的 message（才能判斷有沒有 tool_calls）"""
    response = requests.post(LLM_URL, json={
        "model": MODEL,
        "messages": messages,
        "tools": tools,
        "stream": False,
    })
    return response.json()["choices"][0]["message"]


@app.post("/ask")
def ask(req: AskRequest):
    messages = [{"role": "user", "content": req.question}]

    # TODO: 在這裡寫 agent loop
    #   重複「呼叫 LLM → 有 tool_calls 就執行、結果丟回去 → 再問」
    #   直到 LLM 不再要求工具，回傳最終答案。
    #   記得加一個最大次數上限，避免無限迴圈。
    for _ in range(10):
        message = call_llm(messages)
        if message.get('tool_calls'):
            messages.append(message)
            for tool_call in message.get('tool_calls'):
                name = tool_call["function"]["name"]
                args = json.loads(tool_call["function"]["arguments"])
                result = TOOL_FUNCS[name](**args)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "content": result
                })
        else:
            return {"answer": message["content"]}


    return {"answer": "(還沒實作)"}
