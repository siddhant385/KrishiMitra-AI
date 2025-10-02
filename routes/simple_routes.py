# routes/simple_routes.py
from fastapi import APIRouter

router = APIRouter(prefix="/simple", tags=["simple Router"])

@router.get("/run")
def root():
    return {"message": "FastAPI server is running!"}

@router.get("/health")
def health_check():
    return {"status": "ok"}
