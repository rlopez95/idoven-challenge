from dataclasses import dataclass
from datetime import datetime


@dataclass
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


@dataclass
class ECG:
    id: str
    date: datetime
    leads: list[Lead]

    @property
    def leads_zero_crosses(self) -> dict[str, int]:
        return {lead.name: lead.cross_zero_count for lead in self.leads}
