import os
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.deps import get_current_user
from app.models import BackupRecord, User
from app.schemas.backup import BackupOut
from app.services.minio_client import get_s3_client
from app.core.config import settings


router = APIRouter(prefix="/backups", tags=["backups"])


@router.post("/upload", response_model=BackupOut)
def upload_backup(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    s3 = get_s3_client()
    object_name = f"{current_user.username}/{uuid.uuid4()}-{file.filename}"
    file.file.seek(0, os.SEEK_END)
    size = file.file.tell()
    file.file.seek(0)
    s3.upload_fileobj(file.file, settings.minio_bucket, object_name)

    record = BackupRecord(
        filename=file.filename,
        object_name=object_name,
        content_type=file.content_type,
        size=size,
        owner_id=current_user.id,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("", response_model=list[BackupOut])
def list_backups(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(BackupRecord)
        .filter(BackupRecord.owner_id == current_user.id)
        .order_by(BackupRecord.created_at.desc())
        .all()
    )


@router.get("/{backup_id}/download-url")
def get_download_url(
    backup_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    backup = (
        db.query(BackupRecord)
        .filter(BackupRecord.id == backup_id, BackupRecord.owner_id == current_user.id)
        .first()
    )
    if not backup:
        raise HTTPException(status_code=404, detail="Backup not found")

    s3 = get_s3_client()
    url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.minio_bucket, "Key": backup.object_name},
        ExpiresIn=3600,
    )
    return {"download_url": url}
