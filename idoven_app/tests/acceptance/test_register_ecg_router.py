from bson import ObjectId
from fastapi.testclient import TestClient
from fastapi import status
from idoven_app.tests.helper.test_builder import TestECGData
from idoven_app.main import app

client = TestClient(app)


def test_register_a_ecg() -> None:
    ecg_id = str(ObjectId())
    register_response = client.post(
        "/api/v1/register",
        json={
            "ecg_id": ecg_id,
            "date": str(TestECGData.ANY_DATE),
            "leads": [lead.to_dict() for lead in TestECGData.ANY_LEADS],
        },
    )

    assert register_response.status_code == status.HTTP_201_CREATED

    insight_response = client.get(f"/api/v1/insights/{ecg_id}")
    assert insight_response.status_code == status.HTTP_200_OK


def test_register_a_ecg_with_no_leads_returns_bad_request() -> None:
    invalid_leads = []
    payload = {
        "ecg_id": TestECGData.ANY_ECG_ID,
        "date": str(TestECGData.ANY_DATE),
        "leads": invalid_leads,
    }
    response = client.post("/api/v1/register", json=payload)

    ecg_json = response.json()
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert (
        ecg_json["detail"]
        == f"The ECG request with id: {TestECGData.ANY_ECG_ID}, date: {TestECGData.ANY_DATE} and leads {invalid_leads} is invalid"
    )


def test_register_a_ecg_with_invalid_ecg_id_returns_bad_request() -> None:
    invalid_id = "invalid-ecg-id"
    payload = {
        "ecg_id": invalid_id,
        "date": str(TestECGData.ANY_DATE),
        "leads": [lead.to_dict() for lead in TestECGData.ANY_LEADS],
    }
    response = client.post("/api/v1/register", json=payload)

    ecg_json = response.json()
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert (
        ecg_json["detail"]
        == f"The ECG request with id: {invalid_id}, date: {TestECGData.ANY_DATE} and leads {TestECGData.ANY_LEADS} is invalid"
    )
