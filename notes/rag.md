# RAG 架構

```
使用者問題
  → Embedding 模型（文字 → 向量）
  → Vector DB 搜尋相似文件（Chroma）
  → 組成 system prompt（參考資料）
  → LLM 生成回答（Ollama）
  → 回傳 answer + sources
```

## Chroma
- `chromadb.Client()` → in-memory，重啟資料消失
- `chromadb.HttpClient()` → 連獨立 Chroma server，資料持久化
- 預設用自己的 ONNX embedding 模型，也可以換成 SentenceTransformer

## CORS
瀏覽器安全機制，不同 origin 的 fetch 需要後端允許：
```python
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], ...)
```
Production 要換成真實前端網址，不能用 `*`。