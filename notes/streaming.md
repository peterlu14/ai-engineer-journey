# Streaming

## 技術比較

| 技術 | 方向 | 適合場景 |
|------|------|----------|
| Chunked Response | 單向，等全部完成 | 簡單 API |
| SSE | 單向，server 推 | LLM streaming（ChatGPT 用這個） |
| WebSocket | 雙向 | 聊天室、即時協作、遊戲 |

LLM streaming 推薦用 SSE，前端用 `fetch` + `ReadableStream` 讀。

## 前端 ReadableStream
```ts
const reader = response.body!.getReader()
const decoder = new TextDecoder()  // bytes → 字串

while (true) {
  const { done, value } = await reader.read()  // 每次讀一塊
  if (done) break
  const text = decoder.decode(value)
}
```

三種 Stream 的角色：
- **ReadableStream** — 資料來源（水管）
- **Reader** — 拿杯子去接水，`read()` 每次接一杯
- **WritableStream** — 資料終點，LLM streaming 用不到
- **TransformStream** — 中間過濾器，LLM streaming 用不到

## 後端 StreamingResponse（FastAPI）
```python
from fastapi.responses import StreamingResponse

def chat_stream(question, system_prompt):
    payload = {"model": MODEL, "messages": [...], "stream": True}
    response = requests.post(LLM_URL, json=payload, stream=True)  # requests 也要 stream=True
    for line in response.iter_lines():
        if line:
            data = json.loads(line)
            yield data["message"]["content"]  # yield 而不是 return
            if data["done"]:
                break

@app.post("/ask")
def ask(req: AskRequest):
    return StreamingResponse(chat_stream(...), media_type="text/plain")
```

`yield` vs `return`：
- `return` → 等全部好了才回傳
- `yield` → 每產生一個值就立刻送出，函式不會結束