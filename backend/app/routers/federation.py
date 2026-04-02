import httpx
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.deps import get_current_user
from app.models import Node, User


router = APIRouter(prefix="/federation", tags=["federation"])


@router.post("/sync")
def sync_nodes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    nodes = db.query(Node).all()
    results = []
    for node in nodes:
        try:
            with httpx.Client(timeout=5.0) as client:
                response = client.get(f"{node.base_url.rstrip('/')}/health")
            results.append({"node": node.name, "status": response.status_code})
        except Exception as exc:
            results.append({"node": node.name, "status": "error", "detail": str(exc)})
    return {"results": results}
