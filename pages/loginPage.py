from playwright.sync_api import Page
from pages.basePage import BasePage
from utils.logger import get_logger

class LoginPage(BasePage):
    def __init__(self, page: Page, baseUrl:str):
        super().__init__(page, baseUrl)
        self.logger = get_logger(__name__)
        self.page = page
        self.baseUrl = baseUrl
        self.username = page.get_by_placeholder("Username")
        self.password = page.get_by_placeholder("Password")
        self.login_button = page.get_by_role("button", name="Login")
        self.invalid_credentials = page.get_by_text("Invalid credentials")

    def open(self):
        self.logger.info(f"Navigating to {self.baseUrl}")
        self.navigate()

    def login(self, username: str, password: str):
        self.logger.info(f"Attempting login with username: {username}") 
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()
    
    