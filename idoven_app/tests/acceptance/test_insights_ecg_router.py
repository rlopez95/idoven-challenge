from bson import ObjectId
from fastapi.testclient import TestClient
from fastapi import status
from idoven_app.main import app

client = TestClient(app)

# We will use the ecg_ids from mongo-seed


def test_get_ecg_insights():
    auth_response = client.post("/api/v1/token", data={"username": "daviddoe", "password": "pwd"})
    token = auth_response.json()["access_token"]

    ecg_id = "60d7c1318e1e0a241c4b4d9e"
    response = client.get(f"/api/v1/insights/{ecg_id}", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == status.HTTP_200_OK
    insights_json = response.json()
    assert insights_json == {"III": 0, "aVF": 1}


def test_get_non_existing_ecg_insights_returns_not_found_error():
    auth_response = client.post("/api/v1/token", data={"username": "daviddoe", "password": "pwd"})
    token = auth_response.json()["access_token"]
    ecg_id = str(ObjectId())
    response = client.get(
        f"/api/v1/insights/{ecg_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    insights_json = response.json()
    assert insights_json["detail"] == f"ECG {ecg_id} not found for current user daviddoe"
