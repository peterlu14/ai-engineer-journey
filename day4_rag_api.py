from sentence_transformers import SentenceTransformer
import requests
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel


LLM_URL = "http://192.168.3.2:11434/api/chat"
MODEL = "qwen2.5:14b-instruct-q4_K_M"
EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

documents = [
    "台灣的首都是台北",
    "Python 是一種程式語言",
    "貓是一種哺乳動物",
    "FastAPI 是一個 Python web framework",
    "台灣有很多好吃的食物",
]

doc_embeddings = EMBED_MODEL.encode(documents)

app = FastAPI()

# === Retrieval ===
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def retrieve(query, top_k=2):
    query_embedding = EMBED_MODEL.encode(query)
    scores = []
    for i, doc_emb in enumerate(doc_embeddings):
        score = cosine_similarity(query_embedding, doc_emb)
        scores.append((score, i))
    scores.sort(reverse=True)
    results = []
    for score, idx in scores[:top_k]:
        results.append({
            "text":documents[idx],
            "score": round(float(score), 4)
        })
    return results

def build_system_prompt(context_docs):
    context = "\n".join([f"- {doc['text']}" for doc in context_docs])
    return f"""你是一個有用的助理，請用繁體中文回答。

規則：
1. 你只能根據下方「參考資料」來回答問題
2. 不可以使用參考資料以外的知識
3. 如果參考資料裡沒有答案，你必須回答「我在資料庫中找不到相關資訊」
4. 不可以自己推測或補充資料裡沒有的內容

參考資料：
{context}"""

def chat(question, system_prompt):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        "stream": False
    }
    response = requests.post(LLM_URL, json=payload)
    return response.json()["message"]["content"]

class AskRequest(BaseModel):
    question: str

@app.post("/ask")
def ask(req: AskRequest):
    retrieved = retrieve(req.question)
    system_prompt = build_system_prompt(retrieved)
    reply = chat(req.question, system_prompt)
    return {
        "question":req.question,
        "answer":reply,
        "sources":retrieved
    }
    