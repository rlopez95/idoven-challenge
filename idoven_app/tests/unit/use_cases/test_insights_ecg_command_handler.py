import pytest
from unittest.mock import AsyncMock
from idoven_app.idoven.domain.ecg import ECGNotFoundException
from idoven_app.idoven.domain.ecg_repository import ECGRepository
from idoven_app.idoven.use_cases.insights_ecg_command import InsightsECGCommand, InsightsECGCommandHandler
from idoven_app.tests.helper.test_builder import ECGBuilder, TestECGData


async def test_get_insights_ecg():
    command = InsightsECGCommand(TestECGData.ANY_ECG_ID)
    repository = AsyncMock(ECGRepository)
    repository.find_by_id.return_value = ECGBuilder().build_ecg_with_id(TestECGData.ANY_ECG_ID).build()
    handler = InsightsECGCommandHandler(repository)
    actual_ecg = await handler.process(command)

    repository.find_by_id.assert_called_once_with(command.ecg_id)


async def test_raises_an_error_when_the_ecg_is_not_found():
    command = InsightsECGCommand(TestECGData.ANY_ECG_ID)
    repository = AsyncMock(ECGRepository)
    repository.find_by_id.return_value = None
    handler = InsightsECGCommandHandler(repository)

    with pytest.raises(ECGNotFoundException):
        await handler.process(command)
