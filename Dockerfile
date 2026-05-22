FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt day6_rag_chroma.py /app/
RUN pip install -r requirements.txt
CMD ["uvicorn", "day6_rag_chroma:app", "--host", "0.0.0.0", "--port", "8010"]