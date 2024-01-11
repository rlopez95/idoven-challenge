import pytest
from datetime import datetime
from idoven.domain.ecg import ECG, Lead


@pytest.mark.parametrize(
    "input_signal, expected_cross_count",
    [([1, 0, -1, 2, -3], 3), ([1, -1], 1), ([], 0), ([1, 2, 3], 0), ([1, 0, 0, -1], 1)],
)
def test_lead_returns_right_cross_zero_count(input_signal, expected_cross_count):
    lead = Lead(name="I", signal=input_signal)
    assert lead.cross_zero_count == expected_cross_count


def test_ecg_returns_leads_zero_crosses_by_lead_name():
    channel_I = Lead(name="I", signal=[1, 0, -1, 2, -3])
    channel_II = Lead(name="II", signal=[-5, 5, 3, -3, -3, -2, -1, 0, 10])
    channel_aVR = Lead(name="aVR", signal=[9, 2, -2, -9, -3])
    leads = [channel_I, channel_II, channel_aVR]
    ecg = ECG(id="ecg_id", date=datetime.now(), leads=leads)
    assert ecg.leads_zero_crosses == {"I": 3, "II": 3, "aVR": 1}
