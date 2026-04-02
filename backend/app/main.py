from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.core.database import Base, SessionLocal, engine
from app.core.security import get_password_hash
from app.models import User
from app.routers import auth, backups, federation, nodes
from app.services.minio_client import ensure_bucket_exists


app = FastAPI(title="OpenBackup Federation MVP v2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)
    ensure_bucket_exists()
    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.username == "admin").first()
        if not user:
            db.add(User(username="admin", hashed_password=get_password_hash("admin123"), role="admin"))
            db.commit()
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(auth.router)
app.include_router(backups.router)
app.include_router(nodes.router)
app.include_router(federation.router)
