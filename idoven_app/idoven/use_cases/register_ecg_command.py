import uuid
from datetime import datetime
from idoven.domain.ecg_repository import ECGRepository
from idoven.domain.ecg import ECGFactory
from idoven.domain.command_handler import CommandHandler
from idoven.domain.command import Command
from idoven.domain.command_response import CommandResponse
from idoven.domain.ecg import Lead


class RegisterECGCommand(Command):
    def __init__(self, ecg_id: str, date: datetime, leads: list[Lead]) -> None:
        self.ecg_id = ecg_id
        self.date = date
        self.leads = leads
        super().__init__(uuid.uuid1())


class RegisterECGCommandResponse(CommandResponse):
    pass


class RegisterECGCommandHandler(CommandHandler):
    def __init__(self, ecg_repository: ECGRepository):
        self._ecg_repository = ecg_repository

    async def process(self, command: RegisterECGCommand) -> RegisterECGCommandResponse:
        ecg = ECGFactory.make(ecg_id=command.ecg_id, date=command.date, leads=command.leads)
        await self._ecg_repository.save(ecg)
        return RegisterECGCommandResponse()
