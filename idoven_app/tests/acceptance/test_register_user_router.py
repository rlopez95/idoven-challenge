from uuid import uuid1
from fastapi.testclient import TestClient
from fastapi import status
from idoven_app.tests.helper.test_user_builder import TestUserData
from idoven_app.main import app

client = TestClient(app)


def test_register_a_user() -> None:
    auth_response = client.post("/api/v1/token", data={"username": "alice", "password": "password2"})
    token = auth_response.json()["access_token"]

    user_id = str(uuid1())
    register_response = client.post(
        "/api/v1/user",
        json={
            "user_id": user_id,
            "username": TestUserData.ANY_USER_NAME,
            "password": TestUserData.ANY_PASSWORD,
            "role": TestUserData.ANY_ROLE,
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert register_response.status_code == status.HTTP_201_CREATED


def test_register_a_user_with_invalid_role_returns_bad_request() -> None:
    auth_response = client.post("/api/v1/token", data={"username": "alice", "password": "password2"})
    token = auth_response.json()["access_token"]

    invalid_username = ""
    payload = {
        "user_id": TestUserData.ANY_USER_ID,
        "username": invalid_username,
        "password": TestUserData.ANY_PASSWORD,
        "role": TestUserData.ANY_ROLE,
    }
    response = client.post(
        "/api/v1/user",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_register_a_user_with_invalid_user_id_returns_bad_request() -> None:
    auth_response = client.post("/api/v1/token", data={"username": "alice", "password": "password2"})
    token = auth_response.json()["access_token"]

    invalid_id = ""
    payload = {
        "user_id": invalid_id,
        "username": TestUserData.ANY_USER_NAME,
        "password": TestUserData.ANY_PASSWORD,
        "role": TestUserData.ANY_ROLE,
    }
    response = client.post(
        "/api/v1/user",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )

    user_json = response.json()
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert (
        user_json["detail"]
        == f"""The user with id: {invalid_id}, 
            username: {TestUserData.ANY_USER_NAME},
            password: {TestUserData.ANY_PASSWORD}
            and role {TestUserData.ANY_ROLE} is invalid"""
    )


def test_register_duplicated_user_returns_already_exists_error():
    auth_response = client.post("/api/v1/token", data={"username": "alice", "password": "password2"})
    token = auth_response.json()["access_token"]

    user_id = "0d6e5f50-5277-11ec-8b28-0242ac130003"  # from testing data
    register_response = client.post(
        "/api/v1/user",
        json={
            "user_id": user_id,
            "username": TestUserData.ANY_USER_NAME,
            "password": TestUserData.ANY_PASSWORD,
            "role": TestUserData.ANY_ROLE,
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert register_response.status_code == status.HTTP_409_CONFLICT
