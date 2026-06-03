# AI Engineer Journey

> 從前端 / 全端工程師轉往 AI Engineer 的系統化學習與實作紀錄。
> A structured, hands-on journey into applied AI engineering — RAG, LLM agents, fine-tuning, and observability.

每個主題都**親手實作 + 寫筆記**，從應用層一路做到 Agent 與監控，所有程式都串接本地 LLM（llama.cpp / Qwen）。

---

## 涵蓋主題

| 領域 | 實作 | 檔案 |
|------|------|------|
| **RAG** | Embedding、向量檢索、Chroma、streaming 問答 | `src/day2`–`day7` |
| **LLM Serving** | OpenAI 相容 API、本地模型（llama.cpp）、串流 | `src/day1`, `day7` |
| **Fine-tuning** | QLoRA（4-bit + LoRA）微調 Qwen2.5 | `src/day9_lora_finetune.py` |
| **AI Agent** | Tool / function calling、multi-step loop、dispatch table | `src/day8`, `day10` |
| **Observability** | 結構化 logging、latency / loop / 工具呼叫 / 錯誤率指標 | `src/day11_monitoring.py` |
| **工程化** | FastAPI、Docker / docker-compose、前後端串接 | `Dockerfile`, `frontend/` |

詳細進度見 [ROADMAP.md](ROADMAP.md)。

---

## 重點實作

- **RAG 問答服務** — FastAPI + Chroma 向量檢索 + SSE streaming，前端 React 即時顯示回答與引用來源
- **Multi-step Agent** — LLM 自主決定呼叫哪些工具、呼叫幾次，含迴圈上限 guardrail（[day10](src/day10_agent_loop.py)）
- **Agent 監控** — `/metrics` 端點輸出 latency、迴圈圈數、各工具使用次數、錯誤率，對應 LLMOps observability（[day11](src/day11_monitoring.py)）
- **QLoRA 微調** — 在單張 RTX 3060（12GB）上用 4-bit 量化微調 1.5B 模型（[day9](src/day9_lora_finetune.py)）

---

## 技術筆記

完整筆記索引見 [NOTES.md](NOTES.md)，包含：

- [RAG 架構](notes/rag.md) · [LLM Serving / 量化](notes/llm_serving.md) · [Streaming（SSE）](notes/streaming.md)
- [LoRA / QLoRA](notes/lora_qlora.md) · [AI Agent](notes/agent.md) · [監控 / Observability](notes/monitoring.md)
- [OpenAI API 格式](notes/openai_api_format.md) · [Python 重點](notes/python.md) · [Docker](notes/docker.md)

---

## 專案結構

```
ai-engineer-journey/
├── day1–day11_*.py     # 各主題實作（RAG → Agent → 監控）
├── frontend/           # Vite + React 前端
├── notes/              # 技術筆記
├── leetcode/           # 演算法練習（依 pattern 分類）
├── ROADMAP.md          # 學習路線與進度
└── docker-compose.yaml
```

---

## 技術棧

**後端** Python · FastAPI · PostgreSQL
**AI** llama.cpp (Qwen) · Chroma · SentenceTransformer · PEFT / QLoRA · YOLO
**前端** React / Next.js · Vue 3 · Vite · Tailwind
**工具** Docker · Git · Linux
