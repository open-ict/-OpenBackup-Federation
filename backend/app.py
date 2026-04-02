from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
from pathlib import Path
import hashlib, json, shutil, os

BASE = Path(__file__).resolve().parent.parent
STORAGE = BASE / 'storage'
CATALOG = BASE / 'storage' / 'catalog.json'
STORAGE.mkdir(exist_ok=True)
if not CATALOG.exists():
    CATALOG.write_text('[]', encoding='utf-8')

app = FastAPI(title='OpenBackup Federation MVP')

class Node(BaseModel):
    name: str
    url: str

class SyncPayload(BaseModel):
    remote_catalog: list


def load_catalog():
    return json.loads(CATALOG.read_text(encoding='utf-8'))


def save_catalog(items):
    CATALOG.write_text(json.dumps(items, indent=2), encoding='utf-8')


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


@app.get('/')
def root():
    return {'service': 'OpenBackup Federation MVP', 'status': 'ok'}


@app.post('/backup')
async def upload_backup(file: UploadFile = File(...)):
    dest = STORAGE / file.filename
    with dest.open('wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    entry = {
        'filename': file.filename,
        'size': dest.stat().st_size,
        'sha256': sha256_of(dest),
    }
    catalog = [x for x in load_catalog() if x.get('filename') != file.filename]
    catalog.append(entry)
    save_catalog(catalog)
    return {'stored': entry}


@app.get('/backups')
def list_backups():
    return {'items': load_catalog()}


@app.get('/download/{filename}')
def download_backup(filename: str):
    path = STORAGE / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail='Backup not found')
    return FileResponse(path)


@app.get('/federation/catalog')
def federation_catalog():
    return {'catalog': load_catalog()}


@app.post('/federation/sync')
def federation_sync(payload: SyncPayload):
    local = load_catalog()
    seen = {item['filename']: item for item in local}
    for item in payload.remote_catalog:
        key = item.get('filename')
        if key and key not in seen:
            seen[key] = item
    merged = list(seen.values())
    save_catalog(merged)
    return {'merged_items': len(merged)}
