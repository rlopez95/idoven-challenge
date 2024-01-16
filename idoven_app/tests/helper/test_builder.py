from typing import Self
from datetime import datetime
from bson import ObjectId
from uuid import uuid1
from idoven_app.idoven.domain.ecg import ECGFactory, ECG, Lead


class TestECGData:
    ANY_ECG_ID = str(ObjectId())
    ANY_USER_ID = str(uuid1())
    ANY_DATE = datetime(2024, 1, 1, 12, 30, 0)
    ANY_LEADS = [
        Lead(name="I", signal=[-1, 2, -1, -2, 3]),
        Lead(name="II", signal=[5, 0, -5, 0, 5]),
    ]


class ECGBuilder:
    def __init__(self) -> None:
        self._ecg_id = TestECGData.ANY_ECG_ID
        self._user_id = TestECGData.ANY_USER_ID
        self._date = TestECGData.ANY_DATE
        self._leads = TestECGData.ANY_LEADS

    def build_ecg_with_id(self, ecg_id: str) -> Self:
        self._ecg_id = ecg_id
        return self

    def build_ecg_with_user_id(self, user_id: str) -> Self:
        self._user_id = user_id
        return self

    def build_ecg_with_date(self, date: datetime) -> Self:
        self._date = date
        return self

    def build_ecg_with_leads(self, leads: list[Lead]) -> Self:
        self._leads = leads
        return self

    def build(self) -> ECG:
        return ECGFactory.make(ecg_id=self._ecg_id, user_id=self._user_id, date=self._date, leads=self._leads)
