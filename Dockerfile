FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt src/day7_rag_chroma_stream.py /app/
RUN pip install -r requirements.txt
RUN python -c "import chromadb; client = chromadb.Client(); col = client.create_collection('test'); col.add(documents=['test'], ids=['1'])"
CMD ["uvicorn", "day7_rag_chroma_stream:app", "--host", "0.0.0.0", "--port", "8010"]