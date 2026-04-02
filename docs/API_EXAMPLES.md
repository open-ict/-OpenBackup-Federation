# API Examples

## Get token

```bash
curl -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

## Upload file

```bash
curl -X POST http://localhost:8000/backups/upload \
  -H "Authorization: Bearer <TOKEN>" \
  -F "file=@sample.zip"
```

## Register node

```bash
curl -X POST http://localhost:8000/nodes/register \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "node-athens",
    "base_url": "http://localhost:8000",
    "region": "GR",
    "description": "Athens test node"
  }'
```
