# AI Engineer 學習路線圖

前端工程師（有 Python backend 實戰）轉 AI Engineer。

## 薪資目標 & 里程碑（今年內）

```
70萬（現在）→ 100-130萬（今年底首個 offer）→ 150-200萬（站穩後跳槽推進）
```

- **8-9 月**：有 2-3 個紮實作品，開始投台灣職位
- **10 月**：目標首個 offer（100-130 萬）
- 先跳一級再跳一級，遠端外商（200萬+）是站穩後的下一步，現在不當主目標

---

## 並行任務（跨整個期間，不綁特定 Day）

| 任務 | 規則 | 備註 |
|------|------|------|
| **英文口說** | 每天 15 分鐘，用 AI 對話練 | ⚠️ 最大盲點，4 月就要開始，不可拖到投履歷前。遠端外商視訊面試必考 |
| **找目標公司** | 每週看 LinkedIn / Wellfound / Levels.fyi 職缺 | 搜尋 AI Engineer / LLM Engineer / Full-stack AI remote，校準作品方向 |
| **LeetCode** | 每週 3-5 題維持手感 | 見 [LEETCODE.md](LEETCODE.md)，優先 Array&Hashing / Two Pointers / Stack，不主攻 Hard DP / 競賽題 |

---

## 每日 / 每週時間分配

**平日（4hr）**
- 主線學習/實作 2.5hr
- 專案動手 1hr
- LeetCode 20min
- 英文口說 10min

**假日（6hr，分兩段）**
- 上午專案衝刺 3hr
- 下午補進度/整理筆記/做 demo 2hr
- LeetCode 1 題 30min

> 撐不住時平日降到 3hr 就好。原則：**不要斷 > 時數多**。

---

## Phase 1：應用層基礎 ✅（4/1 – 4/30）

核心目標：做出第一個能 demo 的完整 AI 工具（前端 + FastAPI + RAG）。前端背景是優勢，讓 demo 更專業。

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

## Phase 2：工程化 / Serving ⚙️（5/1 – 5/31）

核心目標：讓服務「像一個真正的系統」。Docker 化幾乎每個職缺都要求。

| Day | 主題 | 檔案 | 狀態 |
|-----|------|------|------|
| - | Docker / docker-compose | Dockerfile, docker-compose.yaml | ✅ |
| - | Streaming（SSE + ReadableStream） | day7_rag_chroma_stream.py | ✅ |
| - | vLLM 概念、量化、OpenAI API 格式 | notes/llm_serving.md | ✅ |
| 9 | LoRA / QLoRA fine-tuning | day9_lora_finetune.py | ✅ |

---

## Phase 3：Agent / Infra ⚙️（6/1 – 6/30）

核心目標：做一個有「系統設計」感的 Agent 系統。

| Day | 主題 | 檔案 | 狀態 |
|-----|------|------|------|
| 8 | Agent tool calling + streaming | day8_agent_tools.py | ✅ |
| 10 | Multi-step agent loop（多輪工具呼叫） | day10_agent_loop.py | ✅ |
| 11 | 監控（logging / metrics / tracing） | day11_monitoring.py | ⬜ |

---

## Phase 4：作品集 & 求職（7/1 – 8/15）

核心目標：把前三個月的東西收斂成履歷上的戰力。

| 項目 | 狀態 |
|------|------|
| 整理 GitHub README（每個 repo 都要像樣） | ⬜ |
| 架構圖（能說明設計取捨） | ⬜ |
| 技術文章 2-3 篇（Medium / 部落格，題材取自 RAG / QLoRA / Agent） | ⬜ |
| 部署 demo（Render / Railway） | ⬜ |
| 履歷對準 AI Engineer / Full-stack AI | ⬜ |
| Mock interview 至少 3 次 | ⬜ |

---

## 技術棧

- **後端**：Python + FastAPI
- **本地模型**：llama.cpp (Qwen3.6-35B-A3B)
- **Embedding**：SentenceTransformer（all-MiniLM-L6-v2）
- **Vector DB**：Chroma
- **前端**：Vite + React + Tailwind + shadcn + TanStack Query
- **容器**：Docker + docker-compose
