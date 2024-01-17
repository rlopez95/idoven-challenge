from uuid import UUID
from bson import ObjectId
from motor import motor_asyncio
from pymongo.errors import DuplicateKeyError
from idoven_app.idoven.domain.ecg_repository import ECGRepository
from idoven_app.idoven.domain.ecg import ECG, DuplicatedECGException, Lead


class MongoECGRepository(ECGRepository):
    def __init__(self, mongo_uri: str) -> None:
        client = motor_asyncio.AsyncIOMotorClient(mongo_uri)
        self._database = client.ecg

    async def find_by_id(self, ecg_id: str, user_id: str) -> ECG | None:
        ecg = await self._database.ecg.find_one({"_id": ObjectId(ecg_id), "user_id": str(user_id)})
        return MongoECGRepository._create_ecg(ecg) if ecg else None

    async def save(self, ecg: ECG) -> None:
        try:
            await self._database.ecg.insert_one(
                {
                    "_id": ObjectId(ecg.ecg_id),
                    "user_id": str(ecg.user_id),
                    "date": ecg.date,
                    "leads": [lead.to_dict() for lead in ecg.leads],
                }
            )
        except DuplicateKeyError as duplicated_error:
            raise DuplicatedECGException() from duplicated_error

    @staticmethod
    def _create_ecg(ecg: dict) -> ECG:
        return ECG(
            ecg_id=str(ecg["_id"]),
            user_id=ecg["user_id"],
            date=ecg["date"],
            leads=[Lead(**lead) for lead in ecg["leads"]],
        )
