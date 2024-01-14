import pymongo
from pymongo import MongoClient
from bson import ObjectId
from idoven.domain.ecg_repository import ECGRepository
from idoven.domain.ecg import ECG


class MongoECGRepository(ECGRepository):
    def __init__(self, mongo_uri: str) -> None:
        ...

    async def find_by_id(self, ecg_id: str) -> ECG | None:
        ...

    async def save(self, ecg: ECG) -> None:
        ...

    @staticmethod
    def _create_ecg(ecg: dict) -> ECG:
        ...
