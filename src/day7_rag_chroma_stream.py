import json
import logging

import chromadb
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
ids = ["doc1", "doc2", "doc3", "doc4", "doc5", "doc6"]

collection.add(documents=documents, ids=ids)
logger.info(f"載入 {len(documents)} 筆文件")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def retrieve(query, top_k=2):
    result = collection.query(query_texts=[query], n_results=top_k)
    return result['documents'][0]


def build_system_prompt(context_docs):
    context = "\n".join([f"- {doc}" for doc in context_docs])
    return f"""你是一個有用的助理，請用繁體中文回答。

規則：
1.你可以任意回答，但是以提到資料庫相關的，需要引用，必回傳引用的部份

參考資料：
{context}"""


def chat_stream(question, system_prompt):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        "stream": True
    }
    response = requests.post(LLM_URL, json=payload, stream=True)
    for line in response.iter_lines():
        if line:
            line = line.decode("utf-8") if isinstance(line, bytes) else line
            if line.startswith("data: "):
                line = line[6:]
            if line == "[DONE]":
                break
            data = json.loads(line)
            content = data["choices"][0]["delta"].get("content", "")
            if content:
                yield content


class AskRequest(BaseModel):
    question: str


@app.post("/ask")
def ask(req: AskRequest):
    logger.info(f"收到問題：{req.question}")
    try:
        retrieved = retrieve(req.question)
        system_prompt = build_system_prompt(retrieved)
        return StreamingResponse(chat_stream(req.question, system_prompt), media_type="text/plain")
    except Exception as e:
        logger.error(f"處理請求失敗：{e}")
        raise