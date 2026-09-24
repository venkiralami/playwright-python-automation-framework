
import re

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.sanity
@pytest.mark.ui
@pytest.mark.test
# The installed pytest-playwright plugin provides the page fixture.
def test_orangehrm_title(page: Page):

    page.goto("https://opensource-demo.orangehrmlive.com/")

    expect(page).to_have_title("OrangeHRM")

    #expect("intentionally failing to test hook failure handling").to_be_visible()


@pytest.mark.ui
@pytest.mark.test
def test_valid_login(page: Page):

    page.goto("https://opensource-demo.orangehrmlive.com/")

    page.get_by_placeholder("Username").fill("Admin")

    page.get_by_placeholder("Password").fill("admin123")

    page.get_by_role("button", name="Login").click()

    expect(page).to_have_url(re.compile(r".*dashboard.*")) # this is better as autowait and retry

    assert "dashboard" in page.url


@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.ui
@pytest.mark.test
def test_invalid_login(page: Page):

    page.goto("https://opensource-demo.orangehrmlive.com/")

    page.get_by_placeholder("Username").fill("Admin")

    page.get_by_placeholder("Password").fill("wrongpassword")

    page.get_by_role("button", name="Login").click()

    expect(page.get_by_text("Invalid credentials")).to_be_visible()  

    #expect("intentionally failing to test hook failure handling").to_be_visible()

@pytest.mark.conf
@pytest.mark.test
def test_config_readerWithotFixture():
    from utils.config_reader import load_config

    config = load_config("qa")
    print(f"Loaded config for QA: {config}")
    assert config["base_url"] == "https://opensource-demo.orangehrmlive.com/"
    #expect("intentionally failing to test hook failure handling").to_be_visible()

@pytest.mark.conf
@pytest.mark.test
def test_config_readerWithFixture(config):
    
    testEnv = config["testenv"]
    base_url = config["base_url"]
    print(f" ENV ==> {testEnv}")
    if testEnv == "qa":
        assert base_url == "https://opensource-demo.orangehrmlive.com/"
    elif testEnv == "uat":
        assert base_url == "https://www.saucedemo.com/"
    elif testEnv == "stage":
         assert base_url == "https://www.saucedemo.com/stage"
    else:
        print("===  No environment set ====")

    #expect("intentionally failing to test hook failure handling").to_be_visible()