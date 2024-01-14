from abc import ABC, abstractmethod
from idoven_app.idoven.domain.ecg import ECG


class ECGRepository(ABC):
    @abstractmethod
    async def find_by_id(self, ecg_id: str) -> ECG | None:
        raise NotImplementedError()

    @abstractmethod
    async def save(self, ecg: ECG) -> None:
        raise NotImplementedError()
