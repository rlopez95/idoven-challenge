from datetime import datetime
from pydantic import BaseModel
from idoven_app.idoven.domain.ecg import Lead


class ECGRequest(BaseModel):
    ecg_id: str
    date: datetime
    leads: list[Lead]
