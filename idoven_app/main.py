from fastapi import FastAPI
from idoven_app.idoven.api.v1.ecg.insights_ecg_router import insights_ecg_router
from idoven_app.idoven.api.v1.ecg.register_ecg_router import register_ecg_router
from idoven_app.idoven.api.v1.health import health_router
from idoven_app.idoven.api.v1.auth import auth_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(health_router)
app.include_router(register_ecg_router)
app.include_router(insights_ecg_router)
