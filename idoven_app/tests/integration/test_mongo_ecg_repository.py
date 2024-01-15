from bson import ObjectId
from idoven_app.idoven.infrastructure.mongo_ecg_repository import MongoECGRepository
from idoven_app.tests.helper.test_builder import ECGBuilder
from idoven_app.idoven.config import settings


async def test_register_a_ecg():
    ecg_id = str(ObjectId())
    ecg = ECGBuilder().build_ecg_with_id(ecg_id).build()
    repository = MongoECGRepository(settings.mongo_uri)
    await repository.save(ecg)
    new_ecg = await repository.find_by_id(ecg_id)
    assert new_ecg
    assert new_ecg.ecg_id == ecg_id
