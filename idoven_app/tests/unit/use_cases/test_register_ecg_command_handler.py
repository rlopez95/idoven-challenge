from unittest.mock import AsyncMock
from idoven.use_cases.register_ecg_command import RegisterECGCommandHandler, RegisterECGCommand
from idoven.domain.ecg_repository import ECGRepository
from tests.helper.test_builder import ECGBuilder, TestECGData


async def test_register_ecg():
    ecg = ECGBuilder().build()
    command = RegisterECGCommand(ecg_id=TestECGData.ANY_ECG_ID, date=TestECGData.ANY_DATE, leads=TestECGData.ANY_LEADS)

    repository = AsyncMock(ECGRepository)
    register_command_handler = RegisterECGCommandHandler(ecg_repository=repository)
    await register_command_handler.process(command)

    repository.save.assert_awaited_once_with(ecg)
