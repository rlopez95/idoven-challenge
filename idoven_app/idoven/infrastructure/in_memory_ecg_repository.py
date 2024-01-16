import asyncio
from idoven_app.idoven.domain.ecg import ECG
from idoven_app.idoven.domain.ecg_repository import ECGRepository


class InMemoryECGRepository(ECGRepository):
    _lock = asyncio.Lock()

    def __init__(self) -> None:
        self._ecgs: dict[tuple(str, str), ECG] = {}

    async def find_by_id(self, ecg_id: str, user_id: str) -> ECG | None:
        return self._ecgs.get((ecg_id, user_id))

    async def save(self, ecg: ECG) -> None:
        async with InMemoryECGRepository._lock:
            self._ecgs[(ecg.ecg_id, ecg.user_id)] = ecg
