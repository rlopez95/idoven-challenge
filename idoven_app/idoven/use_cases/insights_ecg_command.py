import uuid
from uuid import UUID
from idoven_app.idoven.domain.command import Command
from idoven_app.idoven.domain.command_handler import CommandHandler
from idoven_app.idoven.domain.command_response import CommandResponse
from idoven_app.idoven.domain.ecg import ECG, ECGNotFoundException
from idoven_app.idoven.domain.ecg_repository import ECGRepository


class InsightsECGCommand(Command):
    def __init__(self, ecg_id: str, user_id: UUID) -> None:
        self.ecg_id = ecg_id
        self.user_id = user_id
        super().__init__(uuid.uuid1())


class InsightsCommandResponse(CommandResponse):
    def __init__(self, ecg: ECG) -> None:
        self.insights = ecg.leads_zero_crosses


class InsightsECGCommandHandler(CommandHandler):
    def __init__(self, ecg_repository: ECGRepository):
        self._ecg_repository = ecg_repository

    async def process(self, command: InsightsECGCommand) -> InsightsCommandResponse:
        ecg = await self._ecg_repository.find_by_id(command.ecg_id, command.user_id)
        if not ecg:
            raise ECGNotFoundException()
        return InsightsCommandResponse(ecg)
