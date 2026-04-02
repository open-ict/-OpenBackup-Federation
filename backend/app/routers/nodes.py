from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.deps import get_current_user
from app.models import Node, User
from app.schemas.node import NodeCreate, NodeOut


router = APIRouter(prefix="/nodes", tags=["nodes"])


@router.post("/register", response_model=NodeOut)
def register_node(
    payload: NodeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = db.query(Node).filter(Node.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Node already exists")

    node = Node(**payload.model_dump())
    db.add(node)
    db.commit()
    db.refresh(node)
    return node


@router.get("", response_model=list[NodeOut])
def list_nodes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Node).order_by(Node.created_at.desc()).all()
