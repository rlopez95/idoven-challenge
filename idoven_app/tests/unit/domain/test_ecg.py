import pytest
from datetime import datetime
from idoven_app.idoven.domain.ecg import ECG, Lead, ECGInvalidException
from idoven_app.tests.helper.test_builder import ECGBuilder, TestECGData


@pytest.mark.parametrize(
    "input_signal, expected_cross_count",
    [
        ([1, 0, -1, 2, -3], 3),
        ([1, -1], 1),
        ([-1], 0),
        ([1, 2, 3], 0),
        ([1, 0, 0, -1], 1),
    ],
)
def test_lead_returns_right_cross_zero_count(input_signal, expected_cross_count):
    lead = Lead(name="I", signal=input_signal)
    assert lead.cross_zero_count == expected_cross_count


def test_ecg_returns_leads_zero_crosses_by_lead_name():
    channel_I = Lead(name="I", signal=[1, 0, -1, 2, -3])
    channel_II = Lead(name="II", signal=[-5, 5, 3, -3, -3, -2, -1, 0, 10])
    channel_aVR = Lead(name="aVR", signal=[9, 2, -2, -9, -3])
    leads = [channel_I, channel_II, channel_aVR]
    ecg = ECG(ecg_id="ecg_id", user_id="user_id", date=datetime.now(), leads=leads)
    assert ecg.leads_zero_crosses == {"I": 3, "II": 3, "aVR": 1}


def test_ecg_factory_creates_a_ecg():
    ecg = ECGBuilder().build_ecg_with_id(TestECGData.ANY_ECG_ID).build()
    assert ecg.ecg_id == TestECGData.ANY_ECG_ID


def test_ecg_factory_raises_error_when_invalid_ecg_id():
    invalid_ecg_id = "not-a-valid-object-id"
    with pytest.raises(ECGInvalidException):
        ECGBuilder().build_ecg_with_id(invalid_ecg_id).build()


def test_ecg_factory_raises_error_when_invalid_date():
    invalid_date = ""
    with pytest.raises(ECGInvalidException):
        ECGBuilder().build_ecg_with_date(invalid_date).build()


def test_ecg_factory_raises_error_when_empty_leads():
    empty_leads = []
    with pytest.raises(ECGInvalidException):
        ECGBuilder().build_ecg_with_leads(empty_leads).build()


def test_ecg_factory_raises_error_when_leads_with_no_signal():
    no_signal_leads = [Lead(name="I", signal=[])]
    with pytest.raises(ECGInvalidException):
        ECGBuilder().build_ecg_with_leads(no_signal_leads).build()
