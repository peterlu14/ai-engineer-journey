# LLM Serving 框架

## Ollama vs vLLM

| | Ollama | vLLM |
|--|--------|------|
| 設計目標 | 個人 / 開發用 | 生產 / 高併發 |
| 單人推理速度 | 快 | 較慢 |
| VRAM 使用 | 省（按需分配） | 全吃（預分配 KV cache） |
| 模型格式 | GGUF | safetensors + 量化 |
| 適合場景 | 本機開發、學習 | 100+ 使用者同時打 API |

vLLM 核心技術：**PagedAttention**，把 KV cache 像作業系統管理記憶體一樣分頁管理，讓多個 request 共享 GPU 記憶體，高併發 throughput 比 Ollama 高很多。

## 量化（Quantization）

把模型參數從高精度壓縮成低精度，省 VRAM、速度更快，品質略降：

| 格式 | 每參數大小 | 9B 模型 VRAM | 適合框架 |
|------|-----------|-------------|---------|
| bfloat16（原始）| 2 bytes | ~18GB | 高階 GPU |
| FP8 | 1 byte | ~9GB | vLLM / 資料中心 |
| AWQ / GPTQ (4-bit) | 0.5 bytes | ~5GB | vLLM |
| GGUF Q4 | ~0.5 bytes | ~5GB | Ollama / llama.cpp |

AWQ 和 GGUF 效果類似，但格式不同、不能互換。

## OpenAI 相容 API 格式

OpenAI 定義了一套標準 API，vLLM、Ollama、Azure OpenAI 都支援：

```
POST /v1/chat/completions
{
  "model": "model-name",
  "messages": [
    {"role": "system", "content": "你是助理"},
    {"role": "user", "content": "你好"}
  ],
  "stream": false
}
```

**Ollama 原生格式 vs OpenAI 格式對照：**

| 功能 | Ollama | OpenAI 格式 |
|------|--------|------------|
| 對話 | `POST /api/chat` | `POST /v1/chat/completions` |
| 列出模型 | `GET /api/tags` | `GET /v1/models` |

Response 差異：
- Ollama：`data["message"]["content"]`
- OpenAI：`data["choices"][0]["message"]["content"]`

Ollama 也支援 OpenAI 格式，只需把 URL 改成 `/v1/chat/completions`，好處是 code 一套可以接 OpenAI / vLLM / Azure，換服務不改 code。