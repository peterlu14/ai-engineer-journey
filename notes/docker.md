# Docker

## 基本概念
- **Image**：打包好的環境，像是範本
- **Container**：Image 跑起來的實例
- **Build time**：`docker build` 時執行（`RUN` 指令）
- **Runtime**：`docker run` 時執行（`CMD` 指令）

## Dockerfile
```dockerfile
FROM python:3.11-slim      # 基底 image
WORKDIR /app               # 容器內工作目錄
COPY requirements.txt /app/
RUN pip install -r requirements.txt   # build 時安裝
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8010"]  # 啟動指令
```
- `--host 0.0.0.0` 必要，否則容器外連不進來

## Docker 網路隔離
- 容器預設網路與本機隔離
- 容器內的 `localhost` ≠ 本機的 `localhost`
- `network_mode: host`：取消隔離，直接用本機網路（只適合開發環境）
- 同網段的其他機器（如 `192.168.3.2`）在預設網路下通常可以連到

## Build time 預熱
模組層級的程式碼在 import 時就執行，可以利用這個在 build 時預先觸發下載：
```dockerfile
RUN python -c "import chromadb; ..."
```

## docker-compose
串接多個 container，一個指令啟動整個服務：
```yaml
services:
  backend:
    build: .
    ports:
      - "8010:8010"
```
- `build: .` → 用當前目錄的 Dockerfile build
- `image:` → 用現成的 image（如 `postgres:16`）
- `ports` 是 array，格式 `"本機:容器"`