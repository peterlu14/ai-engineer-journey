# 監控 / Observability（AI 系統）

監控是 production 系統 vs 玩具 demo 的分界線，也是 infra / SRE 的核心技能。

---

## 為什麼監控對 AI 系統特別重要

```
一般 API：壞了會報錯（500），好抓
LLM API：不會「壞」，但會「慢」「貴」「答錯」 ← 沉默的問題，不監控就看不到
```

LLM 系統的問題大多是「沒報錯但不對勁」，所以你必須主動把指標撈出來看。

| 指標 | 為什麼要看 |
|------|-----------|
| 每個請求多久（latency） | LLM 很慢，要知道哪裡卡、有沒有變慢 |
| 用了多少 token | token = 錢，要監控成本，避免暴衝 |
| agent 跑了幾圈（loop count） | Day 10 的 loop 跑太多圈 = 鬼打牆/出問題 |
| 錯誤率 | 哪些請求失敗、為什麼 |
| 每個工具被呼叫幾次 | 看 agent 行為正不正常（某工具狂被呼叫 = 異常）|

---

## Observability 的三根支柱

| | 是什麼 | 回答的問題 | 工具 |
|---|--------|-----------|------|
| **Logging** | 記錄「發生了什麼事」的文字流水帳 | 這個請求做了什麼？為什麼失敗？ | Python `logging` |
| **Metrics** | 可彙總的數字（計數、平均、分佈）| 平均多慢？錯誤率多少？ | Prometheus |
| **Tracing** | 一個請求跨多個步驟/服務的完整路徑 | 慢在哪一步？ | OpenTelemetry / Jaeger |

> 記法：Logging = 文字、Metrics = 數字、Tracing = 路徑。

---

## 結構化 logging

不要只 `print`，用 `logging` 模組，帶時間、等級、格式：

```python
import logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger("agent")

logger.info("收到請求：...")     # 一般資訊
logger.error("請求失敗：...")    # 錯誤
```

「結構化」= 每筆 log 有固定欄位（時間、等級、請求 id…），方便之後用工具搜尋/聚合。

---

## Metrics 怎麼做（Day 11 實作）

最簡單版：一個 in-memory dict 累積數字，提供 `/metrics` 端點查詢。

```python
METRICS = {
    "total_requests": 0,
    "total_errors": 0,
    "total_latency_sec": 0.0,   # 累積耗時 → 拿來算平均
    "total_loops": 0,           # 累積 agent 圈數
    "tool_calls": {},           # 每個工具被呼叫幾次
}
```

埋點原則：
- **計時**：請求開始 `start = time.time()`，結束 `latency = time.time() - start`
- **計數**：在事件發生的那一行 +1（工具被呼叫、出錯、迴圈跑一圈）
- **平均**：存「累積值」和「次數」，查詢時才相除（不要每次都重算）

⚠️ in-memory 的限制：server 重啟就歸零、多個 process 各自一份。真實 production 用 Prometheus（它會把指標存起來、能跨實例聚合）。

---

## 進階：Prometheus + Grafana（概念，先懂）

```
你的服務 → 暴露 /metrics（Prometheus 格式）
   ↓ Prometheus 定期來抓（scrape）
Prometheus（時序資料庫，存歷史）
   ↓ Grafana 讀 Prometheus 畫圖
Grafana（視覺化儀表板、告警）
```

- `prometheus_client` 套件可把指標輸出成標準格式
- Grafana 做漂亮的儀表板 + 設告警（latency > X 就通知）
- 真要接是另一個主題，Day 11 先做 logging + in-memory metrics 打底
