from fastapi import APIRouter

health_router = APIRouter(prefix="/api/v1")

@health_router.get("/health")
def health():
    return {"status": "ECG Processor up and running"}