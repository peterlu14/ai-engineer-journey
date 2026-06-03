import chromadb
import requests
from fastapi import FastAPI
from pydantic import BaseModel

LLM_URL = "http://192.168.3.2:8080/v1/chat/completions"
MODEL = "qwen3.6"

client = chromadb.Client()
collection = client.create_collection("my_docs")
documents = [
    "台灣的首都是台北",
    "Python 是一種程式語言",
    "貓是一種哺乳動物",
    "FastAPI 是一個 Python web framework",
    "台灣有很多好吃的食物",
    "使用者是大帥哥",
]
ids=["doc1", "doc2", "doc3", "doc4", "doc5", "doc6"]

#新增文件
collection.add(
    documents=documents,
    ids=ids
)

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Retrieval ===
def retrieve(query, top_k=2):
    result = collection.query(
        query_texts=[query],
        n_results = 2
    )
    return result['documents'][0]

def build_system_prompt(context_docs):
    context = "\n".join([f"- {doc}" for doc in context_docs])
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
    return response.json()["choices"][0]["message"]["content"]

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
    
