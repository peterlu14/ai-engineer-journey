from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

documents = [
    "台灣的首都是台北",
    "Python 是一種程式語言",
    "貓是一種哺乳動物",
    "FastAPI 是一個 Python web framework",
    "台灣有很多好吃的食物",
]

doc_embeddings = model.encode(documents)

def cosine_similarity(a,b):
    return np.dot(a,b) / (np.linalg.norm(a) * np.linalg.norm(b))

def retrieve(query, top_k=2):
    query_embedding = model.encode(query)

    scores = []
    for i , doc_emb in enumerate(doc_embeddings):
        score = cosine_similarity(query_embedding, doc_emb)
        scores.append((score, i))

    scores.sort(reverse=True)

    results = []
    for  score, idx in scores[:top_k]:
        results.append({
            "text": documents[idx],
            "score": round(float(score), 4)
        })
    return results
# 測試的時候改成這樣，印出所有文件的分數
# query = "台灣的首都在哪裡？"
# query_embedding = model.encode(query)

# for i, doc_emb in enumerate(doc_embeddings):
#     score = cosine_similarity(query_embedding, doc_emb)
#     print(f"{score:.4f} | {documents[i]}")
    # 測試
query = "台灣的首都在哪裡？"
results = retrieve(query)

print(f"Query: {query}")
print("最相關的文件：")
for r in results:
    print(f"  score: {r['score']} | {r['text']}")


# **跑完之後你應該會看到**
# ```
# Query: 台灣的首都在哪裡？
# 最相關的文件：
#   score: 0.85xx | 台灣的首都是台北
#   score: 0.43xx | 台灣有很多好吃的食物