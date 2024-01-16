from datetime import datetime
from idoven_app.idoven.infrastructure.in_memory_ecg_repository import (
    InMemoryECGRepository,
)
from idoven_app.tests.helper.test_ecg_builder import ECGBuilder, TestECGData


async def test_find_ecg_by_id():
    repository = InMemoryECGRepository()
    ecg = ECGBuilder().build_ecg_with_id(TestECGData.ANY_ECG_ID).build_ecg_with_user_id(TestECGData.ANY_USER_ID).build()

    await repository.save(ecg)
    actual_ecg = await repository.find_by_id(TestECGData.ANY_ECG_ID, TestECGData.ANY_USER_ID)

    assert actual_ecg == ecg
    assert actual_ecg.ecg_id == TestECGData.ANY_ECG_ID
    assert actual_ecg.user_id == TestECGData.ANY_USER_ID


async def test_save_ecg():
    repository = InMemoryECGRepository()
    ecg = ECGBuilder().build_ecg_with_id(TestECGData.ANY_ECG_ID).build_ecg_with_date(datetime.now()).build()

    await repository.save(ecg)
    actual_ecg = await repository.find_by_id(TestECGData.ANY_ECG_ID, TestECGData.ANY_USER_ID)

    assert actual_ecg == ecg
    assert actual_ecg.ecg_id == TestECGData.ANY_ECG_ID
    assert actual_ecg.user_id == TestECGData.ANY_USER_ID
