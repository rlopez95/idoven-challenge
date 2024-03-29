from bson import ObjectId
from fastapi.testclient import TestClient
from fastapi import status
from idoven_app.tests.helper.test_ecg_builder import TestECGData
from idoven_app.main import app

client = TestClient(app)


def test_register_a_ecg() -> None:
    auth_response = client.post("/api/v1/token", data={"username": "johndoe", "password": "password1"})
    token = auth_response.json()["access_token"]

    ecg_id = str(ObjectId())
    register_response = client.post(
        "/api/v1/register",
        json={
            "ecg_id": ecg_id,
            "date": str(TestECGData.ANY_DATE),
            "leads": [lead.to_dict() for lead in TestECGData.ANY_LEADS],
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert register_response.status_code == status.HTTP_201_CREATED

    insight_response = client.get(f"/api/v1/insights/{ecg_id}", headers={"Authorization": f"Bearer {token}"})
    assert insight_response.status_code == status.HTTP_200_OK


def test_register_a_ecg_with_no_leads_returns_bad_request() -> None:
    auth_response = client.post("/api/v1/token", data={"username": "johndoe", "password": "password1"})
    token = auth_response.json()["access_token"]

    invalid_leads = []
    payload = {
        "ecg_id": TestECGData.ANY_ECG_ID,
        "date": str(TestECGData.ANY_DATE),
        "leads": invalid_leads,
    }
    response = client.post(
        "/api/v1/register",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )

    ecg_json = response.json()
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert (
        ecg_json["detail"]
        == f"The ECG request with id: {TestECGData.ANY_ECG_ID}, date: {TestECGData.ANY_DATE} and leads {invalid_leads} is invalid"
    )


def test_register_a_ecg_with_invalid_ecg_id_returns_bad_request() -> None:
    auth_response = client.post("/api/v1/token", data={"username": "johndoe", "password": "password1"})
    token = auth_response.json()["access_token"]

    invalid_id = "invalid-ecg-id"
    payload = {
        "ecg_id": invalid_id,
        "date": str(TestECGData.ANY_DATE),
        "leads": [lead.to_dict() for lead in TestECGData.ANY_LEADS],
    }
    response = client.post(
        "/api/v1/register",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )

    ecg_json = response.json()
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert (
        ecg_json["detail"]
        == f"The ECG request with id: {invalid_id}, date: {TestECGData.ANY_DATE} and leads {TestECGData.ANY_LEADS} is invalid"
    )


def test_register_duplicated_ucg_returns_already_exists_error():
    auth_response = client.post("/api/v1/token", data={"username": "johndoe", "password": "password1"})
    token = auth_response.json()["access_token"]

    ecg_id = "60d7c0ed8e1e0a241c4b4d9d"  # from mongo-seed to ease testing
    register_response = client.post(
        "/api/v1/register",
        json={
            "ecg_id": ecg_id,
            "date": str(TestECGData.ANY_DATE),
            "leads": [lead.to_dict() for lead in TestECGData.ANY_LEADS],
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    register_json = register_response.json()
    assert register_response.status_code == status.HTTP_409_CONFLICT
    assert register_json["detail"] == f"The ECG request with id: {ecg_id} already exists"
