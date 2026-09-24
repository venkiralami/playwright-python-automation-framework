
import pytest


@pytest.mark.api
def test_create_multiple_users(user_factory):
    first_user = user_factory()
    second_user = user_factory()
    third_user = user_factory()

    assert first_user["id"] == 11
    assert second_user["id"] == 11
    assert third_user["id"] == 11

    assert len({
        first_user["username"],
        second_user["username"],
        third_user["username"],
    }) == 3

    print("First user:", first_user)
    print("Second user:", second_user)
    print("Third user:", third_user)


@pytest.mark.api
def test_create_custom_users(user_factory):
    manager = user_factory(name="QA Manager")
    architect = user_factory(name="QA Architect")

    assert manager["name"] == "QA Manager"
    assert architect["name"] == "QA Architect"

    assert manager["username"] != architect["username"]
    assert manager["email"] != architect["email"]

    print("Manager:", manager)
    print("Architect:", architect)