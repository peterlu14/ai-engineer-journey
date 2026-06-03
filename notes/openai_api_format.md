# OpenAI API 格式 — 哪些固定、哪些自己取

寫 LLM 應用時，code 裡混了三種來源的格式，分不清會很混亂。

## 三種來源

```
① OpenAI 定義的   → 固定，不能改名（改了 API 不認）
② FastAPI 框架的  → 框架規定的寫法
③ 你自己取的      → 隨便改都行
```

**一眼分辨**：問自己「這個名字是不是我跟 LLM API 溝通時用的？」
- 是 → OpenAI 規格，不能改
- 不是，是我自己邏輯用的 → 隨便改

權威文件：https://platform.openai.com/docs/api-reference/chat
（llama.cpp / vLLM / Azure 都遵循這份）

---

## ① OpenAI 定義的（固定，不能改名）

### Request body（送出去）
```python
{
    "model": MODEL,        # 固定欄位名
    "messages": [...],     # 固定
    "tools": [...],        # 固定
    "stream": False,       # 固定
    "temperature": 0.05,   # 固定
}
```

### messages 的 role（只有這四種）
```
"system"     系統指示
"user"       使用者
"assistant"  AI 回的
"tool"       工具結果
```

### message 的欄位
```python
{
    "role": "...",          # 固定
    "content": "...",       # 固定
    "tool_calls": [...],    # 固定（assistant 要呼叫工具時才有）
    "tool_call_id": "...",  # 固定（role=tool 時用來配對是哪個工具的結果）
}
```

### tool_calls 結構
```python
{
    "id": "...",            # 固定，配對用
    "type": "function",     # 固定
    "function": {
        "name": "...",      # 固定欄位名
        "arguments": "..."  # 固定，是 JSON 字串 → 要 json.loads()
    }
}
```

### tools 定義（這整塊是 JSON Schema 標準）
```python
{
    "type": "function",          # 固定
    "function": {
        "name": "get_weather",   # 欄位名固定（值你取）
        "description": "...",    # 欄位名固定
        "parameters": {          # 固定 → JSON Schema 格式
            "type": "object",        # 固定
            "properties": {...},     # 固定
            "required": [...]        # 固定
        }
    }
}
```

### Response（收回來）
```python
response.json()["choices"][0]["message"]   # 非 stream：choices, message 固定
#               ["choices"][0]["delta"]    # stream：delta 固定
# 還有 "finish_reason"（停止原因）、"usage"（token 數）都是固定
```

---

## ② FastAPI 框架的
```python
@app.post("/ask")              # FastAPI 裝飾器
@app.get("/metrics")           # FastAPI

class AskRequest(BaseModel):   # Pydantic（FastAPI 用來驗證輸入）
    question: str              # 欄位名你取，但「用 BaseModel」是框架規定
```

---

## ③ 你自己取的（隨便改）
```python
LLM_URL, MODEL          # 常數名
get_weather, calculate  # 工具函式名
TOOL_FUNCS              # dispatch table 名
METRICS                 # 指標 dict 名 + 裡面所有 key
question                # AskRequest 的欄位名
{"answer": ...}         # 你回傳給前端的格式（跟前端約定就好）
```

---

## 對照例子
- `message["tool_calls"]` ← OpenAI 的，不能改成 `message["toolcalls"]`
- `METRICS["total_loops"]` ← 你的，想改叫什麼都行

## 相關
- Ollama 原生格式 vs OpenAI 格式對照 → [llm_serving.md](llm_serving.md)
- chat / stream / tool_call 的 response 差異 → [streaming.md](streaming.md)、[agent.md](agent.md)
