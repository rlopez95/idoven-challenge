from fastapi import FastAPI
from idoven.api.v1.health import health_router
from idoven.api.v1.ecg.register_ecg_router import register_ecg_router

app = FastAPI()

app.include_router(health_router)
app.include_router(register_ecg_router)