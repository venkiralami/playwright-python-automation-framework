import pytest
import re
import os

from playwright.sync_api import Page, expect
from pages.loginPage import LoginPage

from utils.data_reader import load_json

json_data = load_json("testdata/login_data.json")


@pytest.mark.valid
#@pytest.mark.parametrize("username, password",[username_env, password_env])
def test_valid_login(page: Page, login_page: LoginPage, secret_credentials):
    username = secret_credentials["username"]
    password = secret_credentials["password"]
    print(f"\n Logging in with username: {username}")
    login_page.login(username, password)
    expect(page).to_have_url(re.compile(r".*dashboard.*")) # this is better as autowait and retry



@pytest.mark.parametrize("username, password", [pytest.param("Admin", "wrong_password", id="valid_username_invalid_password"), pytest.param("wrong_username", "admin123", id="invalid_username_valid_password"), pytest.param("wrong_username", "wrong_password", id="invalid_username_invalid_password")])
def test_invalid_login(login_page: LoginPage, config, username, password):

    login_page.login(username, password)
    expect(login_page.invalid_credentials).to_be_visible()

@pytest.mark.json
@pytest.mark.parametrize("data", json_data, ids=["valid_username_invalid_password","invalid_username_valid_password","invalid_username_invalid_password"])
def test_invalid_login_json(login_page: LoginPage, config, data):

    login_page.login(data["username"], data["password"])
    expect(login_page.invalid_credentials).to_be_visible()
     