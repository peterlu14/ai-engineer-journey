import json
import time
import logging
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ── 結構化 logging 設定 ──────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("agent")

LLM_URL = "http://192.168.3.2:8080/v1/chat/completions"
MODEL = "qwen3.6"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── 指標儲存（in-memory）────────────────────────────────
# 累積每個請求的統計，/metrics 端點可以查
METRICS = {
    "total_requests": 0,       # 總請求數
    "total_errors": 0,         # 失敗數
    "total_latency_sec": 0.0,  # 累積耗時（拿來算平均）
    "total_loops": 0,          # 累積 agent 迴圈圈數
    "tool_calls": {},          # 每個工具被呼叫幾次 {"get_weather": 3, ...}
}


def record_tool_call(name: str):
    """工具被呼叫一次就記一筆"""
    METRICS["tool_calls"][name] = METRICS["tool_calls"].get(name, 0) + 1


# ── 工具 ────────────────────────────────────────────────
def get_weather(city: str) -> str:
    fake_data = {"台北": "晴天，25°C", "高雄": "多雲，28°C", "台中": "陰天，22°C"}
    return fake_data.get(city, "查無此城市資料")


def calculate(expression: str) -> str:
    try:
        return str(eval(expression))
    except Exception:
        return "計算失敗"


TOOL_FUNCS = {"get_weather": get_weather, "calculate": calculate}

tools = [
    {"type": "function", "function": {
        "name": "get_weather", "description": "查詢台灣城市的天氣",
        "parameters": {"type": "object",
            "properties": {"city": {"type": "string", "description": "城市名稱"}},
            "required": ["city"]}}},
    {"type": "function", "function": {
        "name": "calculate", "description": "計算數學算式",
        "parameters": {"type": "object",
            "properties": {"expression": {"type": "string", "description": "數學算式"}},
            "required": ["expression"]}}},
]


class AskRequest(BaseModel):
    question: str


def call_llm(messages):
    response = requests.post(LLM_URL, json={
        "model": MODEL, "messages": messages, "tools": tools, "stream": False,
    })
    return response.json()["choices"][0]["message"]


@app.post("/ask")
def ask(req: AskRequest):
    start = time.time()                    # ① 記開始時間
    METRICS["total_requests"] += 1
    loops = 0                              # 這個請求跑了幾圈
    logger.info(f"收到請求：{req.question}")

    try:
        messages = [{"role": "user", "content": req.question}]

        for _ in range(10):
            loops += 1
            message = call_llm(messages)

            if message.get("tool_calls"):
                messages.append(message)
                for tool_call in message["tool_calls"]:
                    name = tool_call["function"]["name"]
                    args = json.loads(tool_call["function"]["arguments"])

                    # TODO ②：在這裡記錄「這個工具被呼叫了」
                    #         用上面寫好的 record_tool_call(name)
                    #         並 logger.info 記一行「呼叫了什麼工具、參數是什麼」
                    record_tool_call(name)
                    logger.info(f"工具{name}，參數{args}")

                    result = TOOL_FUNCS[name](**args)
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "content": result,
                    })
            else:
                # 正常結束：在這裡收尾統計
                latency = time.time() - start          # ③ 算耗時
                METRICS["total_loops"] += loops
                METRICS["total_latency_sec"] += latency
                logger.info(f"完成：{loops} 圈、{latency:.2f}s")
                return {"answer": message["content"]}

        # 跑滿 10 圈還沒結束（異常）
        raise RuntimeError("agent 超過最大迴圈數")

    except Exception as e:
        METRICS["total_errors"] += 1
        logger.error(f"請求失敗：{e}")
        return {"error": str(e)}


@app.get("/metrics")
def metrics():
    """查詢累積指標 + 算出平均值"""
    reqs = METRICS["total_requests"]
    ok = reqs - METRICS["total_errors"]
    return {
        **METRICS,
        "avg_latency_sec": round(METRICS["total_latency_sec"] / ok, 2) if ok else 0,
        "avg_loops": round(METRICS["total_loops"] / ok, 2) if ok else 0,
    }
