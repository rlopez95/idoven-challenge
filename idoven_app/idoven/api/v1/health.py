from fastapi import APIRouter
from idoven_app.idoven.config import settings

health_router = APIRouter(prefix=settings.api_v1_prefix)


@health_router.get("/health")
def health():
    return {"status": "ECG Processor up and running"}
