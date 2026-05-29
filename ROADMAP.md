# AI Engineer 學習路線圖

目標：前端工程師轉 AI Engineer，薪資 120 萬+

---

## Phase 1：應用層基礎 ✅

| Day | 主題 | 檔案 | 狀態 |
|-----|------|------|------|
| 1 | Ollama CLI assistant（多輪對話） | day1_ai_cli.py | ✅ |
| 2 | Embedding + cosine similarity | day2_ai_cli_embedding.py | ✅ |
| 3 | RAG CLI（retrieval + LLM） | day3_ai_cli_rag.py | ✅ |
| 4 | FastAPI /ask endpoint（含 sources） | day4_ai_cli_rag_api.py | ✅ |
| 5 | 前端串接（Vite + React + fetch） | frontend/ | ✅ |
| 6 | Chroma vector database | day6_rag_chroma.py | ✅ |
| 7 | Sources 顯示前端，完整 RAG demo | day7_rag_chroma_stream.py | ✅ |

---

## Phase 2：工程化 ⚙️

| Day | 主題 | 檔案 | 狀態 |
|-----|------|------|------|
| - | Docker / docker-compose | Dockerfile, docker-compose.yaml | ✅ |
| - | Streaming（SSE + ReadableStream） | day7_rag_chroma_stream.py | ✅ |
| - | vLLM 概念、量化、OpenAI API 格式 | notes/llm_serving.md | ✅ |
| 9 | LoRA / QLoRA fine-tuning | day9_lora_finetune.py | ⬜ |

---

## Phase 3：Agent ⚙️

| Day | 主題 | 檔案 | 狀態 |
|-----|------|------|------|
| 8 | Agent tool calling + streaming | day8_agent_tools.py | ✅ |
| 10 | Multi-step agent loop（多輪工具呼叫） | day10_agent_loop.py | ⬜ |
| 11 | 監控（LangSmith / tracing） | day11_monitoring.py | ⬜ |

---

## Phase 4：作品集 & 求職

| 項目 | 狀態 |
|------|------|
| 整理 GitHub README | ⬜ |
| 部署 demo（Render / Railway） | ⬜ |
| 履歷更新 | ⬜ |
| Mock interview | ⬜ |

---

## 技術棧

- **後端**：Python + FastAPI
- **本地模型**：llama.cpp (Qwen3.6-35B-A3B)
- **Embedding**：SentenceTransformer（all-MiniLM-L6-v2）
- **Vector DB**：Chroma
- **前端**：Vite + React + Tailwind + shadcn + TanStack Query
- **容器**：Docker + docker-compose
