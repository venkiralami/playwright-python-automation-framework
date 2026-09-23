import pytest

from playwright.sync_api import Page, expect
from pages.loginPage import LoginPage

from utils.logger import get_logger
logger = get_logger(__name__)

@pytest.mark.debug
@pytest.mark.hooktest
def test_orangehrm_title(page: Page):
    logger.info("Testing OrangeHRM title")
    login_page = LoginPage(page, "https://www.amazon.com/")
    login_page.open()
    print(login_page.get_title())
    print(login_page.get_current_url())
    expect(page).to_have_title("OrangeHRM - intentionally failing test to check hook failure handling")
    logger.info("Test completed: test_orangehrm_title")

@pytest.mark.debug
@pytest.mark.hooktest
def test_hook_fail1(page: Page, login_page: LoginPage, config):
    logger.info("Testing hook failure scenario 1")
    print(login_page.get_title())
    print(login_page.get_current_url())
    expect(page).to_have_title("Intentionally failing test to check hook failure handling")
    logger.info("Test completed: test_hook_fail1")

@pytest.mark.debug
@pytest.mark.hooktest
def test_hook_fail2(page: Page):
    logger.info("Testing hook failure scenario 2")
    login_page = LoginPage(page, "https://www.flipkart.com/")
    login_page.open()
    print(login_page.get_title())
    print(login_page.get_current_url())
    expect(page).to_have_title("Intentionally failing test to check hook failure")
    logger.info("Test completed: test_hook_fail2")