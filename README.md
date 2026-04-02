# OpenBackup Federation MVP v2

GitHub-ready MVP for a federated backup platform with:

- FastAPI backend
- PostgreSQL metadata storage
- JWT authentication
- MinIO object storage
- Multi-node registry
- Simple federation sync API
- Basic dashboard
- Agent uploader
- Docker Compose stack

## Stack

- FastAPI
- SQLAlchemy
- PostgreSQL
- MinIO (S3-compatible)
- JWT auth
- Docker Compose

## Quick start

```bash
cd docker
docker compose up --build
```

Services:

- API: http://localhost:8000
- API docs: http://localhost:8000/docs
- MinIO Console: http://localhost:9001
  - user: minioadmin
  - pass: minioadmin

Default login:

- username: admin
- password: admin123

## Main endpoints

- `POST /auth/token`
- `GET /auth/me`
- `POST /backups/upload`
- `GET /backups`
- `GET /backups/{backup_id}/download-url`
- `POST /nodes/register`
- `GET /nodes`
- `POST /federation/sync`
- `GET /health`

## Suggested next steps

- add per-node trust policies
- add encrypted client-side backup bundles
- add RBAC roles beyond admin/user
- add restore workflows
- add audit logs
- add scheduler and retention policies
