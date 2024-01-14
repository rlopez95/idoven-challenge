from abc import ABC, abstractmethod
from idoven.domain.command import Command
from idoven.domain.command_response import CommandResponse


class CommandHandler(ABC):
    @abstractmethod
    async def process(self, command: Command) -> CommandResponse:
        pass
