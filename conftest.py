import pytest
import os
import re

from pathlib import Path
from utils.config_reader import load_config
from pages.loginPage import LoginPage
from utils.logger import get_logger
from api.apiClient import APIClient
from utils.test_data_generator import generate_user

logger = get_logger(__name__)

#pytest_addoption is a Pytest hook. We're extending Pytest with our own command-line option:
def pytest_addoption(parser):
    parser.addoption("--env", default="qa", action="store", help="Envronment: qa, uat, stage")

@pytest.fixture(scope="session")
def config(request):
    env = request.config.getoption("--env");
    return load_config(env)

@pytest.fixture  # defaluted to function scope
def login_page(page, config):
    login_page = LoginPage(page, config["base_url"])
    login_page.open()
    return login_page

@pytest.fixture(scope="session")
def secret_credentials():
    username_env = os.getenv("APP_USERNAME")
    password_env = os.getenv("APP_PASSWORD")

    if not username_env or not password_env:
        pytest.fail("Environment variables APP_USERNAME and APP_PASSWORD must be set.") 
        # run below command in powershell to set the environment variables before running the tests
        # $env:APP_USERNAME="Admin" 
        # $env:APP_PASSWORD="admin123"   

    return { "username": username_env, "password": password_env }

# hook to get failed test screenshot. This hook is called after each test is executed, and it allows us to access the test report and take a screenshot if the test failed.
# SCREENSHOT_DIR = Path("screenshots")
# SCREENSHOT_DIR.mkdir(exist_ok=True)

# # Disabled because of the following error: "TypeError: 'NoneType' object is not callable" when using pytest-playwright plugin.
# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item, call):

#     outcome = yield

#     report = outcome.get_result()
    
#     logger.info(f"Test {item} finished with status: {report.outcome}")
#     if report.when == "call" and report.failed:

#         page = item.funcargs.get("page")

#         if page:

#             safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", item.nodeid)

#             screenshot_path = (SCREENSHOT_DIR / f"{safe_name}.png").resolve()

#             page.screenshot(path=str(screenshot_path), full_page=True)


@pytest.fixture(scope="session")
def api_client(config):
    return APIClient(config["api_base_url"])


@pytest.fixture
def created_user(api_client):
    user_data = generate_user()

    payload = {
        "name": f"{user_data['first_name']} {user_data['last_name']}",
        "username": user_data["username"],
        "email": user_data["email"],
    }

    response = api_client.post("/users", json=payload)
    assert response.status_code == 201, (
        f"User creation failed: {response.status_code} - {response.text}"
    )

    created = response.json()
    logger.info("SETUP - Created user: %s", created)

    try:
        yield created
    finally:
        user_id = created.get("id")

        if user_id:
            try:
                delete_response = api_client.delete(f"/users/{user_id}")
                logger.info(
                    "TEARDOWN - Delete user %s returned status %s",
                    user_id,
                    delete_response.status_code,
                )
            except Exception:
                logger.exception(
                    "TEARDOWN - Failed to delete user %s",
                    user_id,
                )



@pytest.fixture
def user_factory(api_client, worker_id):
    created_users = []

    def create_user(
        name=None,
        username=None,
        email=None,
    ):
        user_data = generate_user()

        payload = {
            "name": name or (
                f"{user_data['first_name']} "
                f"{user_data['last_name']}"
            ),
            "username": username or user_data["username"],
            "email": email or user_data["email"],
        }

        response = api_client.post("/users", json=payload)

        assert response.status_code == 201, (
            f"User creation failed: "
            f"{response.status_code} - {response.text}"
        )

        created = response.json()
        created_users.append(created)

        logger.info(
            "WORKER %s - Created user: %s",
            worker_id,
            created,
        )

        return created

    try:
        yield create_user

    finally:
        for user in reversed(created_users):
            user_id = user.get("id")

            if not user_id:
                continue

            try:
                response = api_client.delete(
                    f"/users/{user_id}"
                )

                logger.info(
                    "WORKER %s - Delete user %s (%s): HTTP %s",
                    worker_id,
                    user_id,
                    user.get("username"),
                    response.status_code,
                )

            except Exception:
                logger.exception(
                    "FACTORY - Failed to delete user %s",
                    user_id,
                )