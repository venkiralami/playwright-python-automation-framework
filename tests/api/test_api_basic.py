import pytest
import requests

from utils import logger
from utils.logger import get_logger

logger = get_logger(__name__)

@pytest.mark.smoke
@pytest.mark.api
def test_get_users_withot_fixture():

    response = requests.get("https://jsonplaceholder.typicode.com/users", timeout=10)
    

    assert response.status_code == 200

    users = response.json()

    assert isinstance(users, list)
    assert len(users) > 0

    first_user = users[0]

    assert "id" in first_user
    assert "name" in first_user
    assert "email" in first_user

    print("\nUser ID:", first_user["id"])
    print("Name:", first_user["name"])
    print("Email:", first_user["email"])

@pytest.mark.api
def test_get_users(api_client):

    response = api_client.get("/users")

    assert response.status_code == 200

    users = response.json()

    assert isinstance(users, list)
    assert len(users) > 0

    first_user = users[0]

    assert "id" in first_user
    assert "name" in first_user
    assert "email" in first_user

    print("\nUser ID: Fix ", first_user["id"])
    print("Name:", first_user["name"])
    print("Email:", first_user["email"])

@pytest.mark.api
def test_create_user(api_client):

    payload = {
        "name": "Venkat Automation",
        "username": "venkatqa",
        "email": "automation@example.com"
    }

    response = api_client.post(
        "/users",
        json=payload
    )

    print("Status:", response.status_code)
    print("Response:", response.json())

    assert response.status_code == 201

    created_user = response.json()

    assert created_user["name"] == payload["name"]
    assert created_user["username"] == payload["username"]
    assert created_user["email"] == payload["email"]

    assert "id" in created_user


@pytest.mark.api
def test_update_user(api_client):

    payload = {
        "name": "Venkat Updated",
        "username": "venkatqa_updated",
        "email": "updated@example.com"
    }

    response = api_client.put(
        "/users/1",
        json=payload
    )

    print("PUT Status:", response.status_code)
    print("PUT Response:", response.json())

    assert response.status_code == 200

    updated_user = response.json()

    assert updated_user["name"] == payload["name"]
    assert updated_user["username"] == payload["username"]
    assert updated_user["email"] == payload["email"]
    assert updated_user["id"] == 1


@pytest.mark.api
def test_delete_user(api_client):

    response = api_client.delete("/users/1")

    print("DELETE Status:", response.status_code)

    assert response.status_code == 200

@pytest.mark.api
def test_create_user_fixture(created_user):

    logger.info(f"TEST - Created user: {created_user}")
    print("\nTEST - Created user:", created_user)

    assert "id" in created_user
    assert created_user["name"]
    assert created_user["username"]
    assert created_user["email"]

    
