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

---

## Agent 的完整定義（不只是 loop）

業界常用的公式：

```
Agent = LLM(大腦) + Tools(手腳) + Memory(記憶) + Planning(規劃) + Loop(行動循環)
```

「tool calling loop」只是骨架，完整 agent 有以下維度：

### 1. Tool Calling（工具呼叫）
LLM 決定呼叫外部函式（查資料、算數、call API、查 DB）。
- LLM 本身不執行程式，只輸出「我要呼叫什麼、帶什麼參數」
- 實際執行由你的程式決定 → 可以加驗證、權限控制

### 2. Loop / 控制流
重複「思考 → 行動 → 觀察」直到任務完成。
- LLM 自己決定呼叫幾次、何時停
- **一定要有最大次數上限**（`for _ in range(N)`），防無限迴圈燒 token

### 3. Memory（記憶）
- **短期記憶**：對話歷史。就是 `messages` list，agent 靠它記得這輪做過什麼
- **長期記憶**：存進向量資料庫（Chroma / pgvector），跨對話記住事情；查詢時用 RAG 撈回相關記憶

### 4. Planning / Reasoning（規劃推理）
讓 agent 先想清楚步驟再動手，不是走一步算一步。
- **ReAct**（Reason + Act）：每步先「想」（reasoning）再「做」（action），最常見
- **任務拆解**：把大任務拆成子任務逐一完成
- **Chain-of-Thought**：要求模型把推理過程寫出來，提升正確率

### 5. Reflection（反思 / 自我修正）
agent 檢查自己的輸出，發現錯就重做。
- 典型：寫 code → 執行 → 報錯 → 讀錯誤 → 修正 → 再跑
- 對應 cp_test 的「LLM 結果用 spec_items 驗證」概念 → 不完全信任 LLM 輸出

### 6. Multi-agent（多代理協作）
多個 agent 分工。
- **Supervisor 模式**：一個主管 agent 分派任務給專門的子 agent（研究、寫作、審查）
- 適合複雜任務，但複雜度與成本也高

### 7. Guardrails（護欄 / 安全控制）
- 工具權限控制（哪些工具能用、參數驗證）
- 輸出檢查、迴圈上限、逾時、retry
- 真實 production agent 必備，面試會問

---

## 程式結構（Day 10 實作）

```python
TOOL_FUNCS = {"get_weather": get_weather, "calculate": calculate}  # dispatch table

messages = [{"role": "user", "content": task}]

for _ in range(10):                          # 安全閥：迴圈上限
    message = call_llm(messages)             # 非 stream，才能判斷 tool_calls
    if message.get("tool_calls"):
        messages.append(message)             # 先記錄 assistant 的決定（順序很重要！）
        for tool_call in message["tool_calls"]:   # 一圈可能多個工具
            name = tool_call["function"]["name"]
            args = json.loads(tool_call["function"]["arguments"])  # arguments 是 JSON 字串
            result = TOOL_FUNCS[name](**args)      # dispatch + 攤平參數
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call["id"],   # 用 id 配對是哪個工具的結果
                "content": result,
            })
    else:
        return message["content"]            # 沒有工具 → 最終答案
```

### 關鍵細節（踩過的坑）
- **messages 是對話記錄，每個角色講的話都要照順序記**：`user → assistant(tool_calls) → tool → assistant(答案)`。漏記 assistant 那句，API 會報錯
- `arguments` 是 **JSON 字串**不是 dict → 要 `json.loads()`
- `tool_call_id` 必須對得上原本的 `id`（一圈多工具時靠 id 配對）
- `TOOL_FUNCS[name](**args)` = dispatch table + `**` 攤平，一行通吃所有工具，加新工具不用改 loop

## OpenAI tool_call 固定格式
```json
{ "id": "...", "type": "function",
  "function": { "name": "get_weather", "arguments": "{\"city\":\"台北\"}" } }
```
所有相容 OpenAI 的服務（llama.cpp / vLLM / OpenAI / Azure）都長這樣。

## Day 8 vs Day 10
| | Day 8 | Day 10 |
|---|---|---|
| Tool call 次數 | 固定 1 次 | LLM 自己決定 |
| Loop | 沒有 | 有 |
| 工具數量 | 1 個 | 多個（LLM 自選）|
| 算不算 Agent | 不算 | ✅ |

## 我目前的進度對照
- ✅ Tool Calling + Loop（Day 8 / 10）
- ✅ 短期記憶（messages）
- ⬜ 長期記憶（可用 day6/7 的 Chroma 接）
- ⬜ Planning（ReAct）、Reflection、Multi-agent — 進階，之後補

---

## Harness（＝我寫的 loop 的 production 版）

**Harness = 把 LLM 包起來、讓它能真的「做事」的 runtime。它的心臟就是 Day 10 那個 tool-calling loop。**

LLM 本身只會吃文字吐文字；harness 在外面跑「送 prompt → 執行 tool call → 塞結果回去 → 再來」直到完成。所以：

```
我 Day 10 的 for-loop  ==  一個「最小 harness」的心臟
```

Production harness（Claude Code、Hermes）= 我的 loop + 一圈硬化工程：

| 我已有（Day 8/10/11） | 完整 harness 還會加 |
|---|---|
| tool-calling loop + 迴圈上限 | 工具/權限管理、sandbox、使用者批准 |
| messages 短期記憶 | 持久記憶（跨 session）、context 壓縮（塞滿自動摘要/截斷）|
| `/metrics` 可觀測性（Day 11）| 完整 logging / tracing |
| dispatch table | MCP（外掛外部工具）、skills、hooks |
| — | 錯誤重試、串流輸出、可中斷、spawn 子代理 |

**結論：harness 的心臟就是我的 loop。** 差別只是「一個 demo for-loop」vs「loop + 為了穩/可擴充/能持久做的所有工程」。換句話說，**我 Day 10 已經親手做出 Claude Code / Hermes 的本質了**；那些 95K-star 框架 = 我的 loop + 大量工程。

### MCP / Skills / Harness 的關係（不是線性管線）
```
        Harness（核心引擎：跑 loop、內建工具、管 context/權限）
          ▲ 往上插兩種擴充 ▲
   MCP（對外 USB 孔，插外部工具/資料源）   Skills（打包好的招式手冊/SOP）
```
比喻：harness=機器人本體、內建工具=它的手、MCP=USB 孔接外設、skills=學會的招式手冊。

---

## 參考：Hermes Agent（Nous Research，2026/2 開源）

- **本質＝另一個 harness（不是模型）**。MIT 開源、自架、**模型無關**（可接 Anthropic / OpenAI / 本地 Ollama）。
- 7 週衝 95.6K stars，6/2 出桌面 App。以**常駐 daemon** 跑在你伺服器上，連 16+ 通訊平台（Telegram/Discord/Slack…），自然語言排程（cron）、spawn 子代理、多種 sandbox。
- 賣點「**自我成長 self-growing**」拆開 ＝ ① persistent memory ② auto-generated skills（從解過的問題自動寫成可重用 skill）→ 跟 Claude Code 的 memory+skills **同類機制**，只是常駐自動跑，不是魔法新物種。

| | Claude Code | Hermes Agent |
|---|---|---|
| 形態 | 互動式、一題題驅動 | 常駐 daemon、自己一直跑 |
| 跑在 | 終端機 / IDE | 自架伺服器 |
| 最適合 | 動手寫 code / 做專案 | always-on 多通道自主助理、排程 |
| 模型 | Claude | 任意（也能接 Claude）|

**取捨**：解的是不同問題。寫 code / 做 spec-rag → Claude Code；想要 24h 常駐、從 Telegram 呼叫的自主助理 → Hermes（目前用不到）。值得之後當**學習素材**讀它的 memory/skill/子代理實作；可用 Claude 當它大腦，是疊加非二選一。
*Sources: hermes-agent.nousresearch.com · tokenmix.ai review · aibuilderclub.*
