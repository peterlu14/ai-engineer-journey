# AI Agent

## Agent vs Tool Calling

Tool calling 是 agent 的核心機制，但不等於 agent。

**Tool calling（一次性）：**
```
用戶問 → LLM 呼叫工具 → 拿結果 → 回答
```

**Agent（loop）：**
```
用戶給任務
  → LLM 思考：我需要做什麼？
  → 呼叫工具 A
  → 看結果，再思考
  → 呼叫工具 B
  → 再思考...
  → 任務完成，回答
```

## Agent 的三個要素

1. **工具（Tools）** — LLM 可以呼叫的外部函式
2. **Loop** — 重複「思考 → 行動 → 觀察」直到任務完成
3. **自主決策** — LLM 自己決定呼叫哪個工具、呼叫幾次、何時停止

## 程式結構

```python
messages = [{"role": "user", "content": task}]

while True:
    response = llm(messages)
    message = response["choices"][0]["message"]

    if message.get("tool_calls"):
        # 執行工具，把結果加回 messages
        tool_result = execute_tool(message["tool_calls"][0])
        messages.append(message)
        messages.append({"role": "tool", "content": tool_result})
        # 繼續 loop
    else:
        # LLM 決定任務完成，直接回答
        print(message["content"])
        break
```

## Day 8 vs Day 10

| | Day 8 | Day 10 |
|---|---|---|
| Tool call 次數 | 固定 1 次 | LLM 自己決定 |
| Loop | 沒有 | 有 |
| 算不算 Agent | 不算 | ✅ |
