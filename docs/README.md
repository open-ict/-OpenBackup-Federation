# OpenBackup MVP

## What this MVP includes

* FastAPI backend for backup upload/list/download
* Local catalog for backup metadata
* Simple federation sync endpoint
* Agent upload client
* Minimal HTML dashboard
* Docker Compose for local run

## Run locally

```bash
cd docker
docker compose up
```

Open API: http://localhost:8000/docs

## Upload a file

```bash
python agent/upload\_client.py ../docs/README.md http://localhost:8000/backup
```

