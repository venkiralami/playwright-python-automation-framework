
import re

import pytest
from playwright.sync_api import Page, expect
from pages.loginPage import LoginPage

@pytest.mark.login
@pytest.mark.sanity
@pytest.mark.ui
# The installed pytest-playwright plugin provides the page fixture.
def test_orangehrm_title(page: Page, login_page: LoginPage, config):
   
    print(login_page.get_title())
    print(login_page.get_current_url())
    expect(page).to_have_title("OrangeHRM")

@pytest.mark.login
@pytest.mark.smoke
@pytest.mark.ui
def test_valid_login(page: Page, login_page: LoginPage, config):
    
    login_page.login(config["username"], config["password"])

    expect(page).to_have_url(re.compile(r".*dashboard.*")) # this is better as autowait and retry

@pytest.mark.login
@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.ui
def test_invalid_login(login_page: LoginPage, config):

    login_page.login(config["username"], "wrong_password")
    expect(login_page.invalid_credentials).to_be_visible()
    #expect(page.get_by_text("Invalid credentials")).to_be_visible()  

    