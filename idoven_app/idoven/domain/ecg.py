from dataclasses import dataclass, asdict
from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId


@dataclass(frozen=True)
class Lead:
    name: str
    signal: list[int]
    sample_size: int | None = None  # the number of times a signal is read in a second

    @property
    def cross_zero_count(self) -> int:
        return sum(
            (self.signal[i - 1] >= 0 and self.signal[i] < 0) or (self.signal[i - 1] < 0 and self.signal[i] >= 0)
            for i in range(1, len(self.signal))
        )

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ECG:
    ecg_id: str
    date: datetime
    leads: list[Lead]

    @property
    def leads_zero_crosses(self) -> dict[str, int]:
        return {lead.name: lead.cross_zero_count for lead in self.leads}


class ECGFactory:
    @staticmethod
    def make(ecg_id: str, date: datetime, leads: list[Lead]) -> ECG:
        try:
            ObjectId(ecg_id)
        except InvalidId as exception:
            raise ECGInvalidException("ECG id must be a valid identifier") from exception

        if not date:
            raise ECGInvalidException("ECG must have a date")

        if not leads:
            raise ECGInvalidException("ECG cannot have an empty leads list")

        if not all(lead.signal for lead in leads):
            raise ECGInvalidException("All ECG channels must have a value")

        return ECG(ecg_id=ecg_id, date=date, leads=leads)


class ECGInvalidException(Exception):
    pass

class ECGNotFoundException(Exception):
    pass
