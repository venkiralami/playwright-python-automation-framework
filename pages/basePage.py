
from playwright.sync_api import Page

class BasePage:
    def __init__(self, page: Page, baseUrl):
        self.page = page
        self.baseUrl = baseUrl
        
    def navigate(self):
        self.page.goto(self.baseUrl)

    def get_title(self) -> str:
        return self.page.title()

    def get_current_url(self) -> str:
        return self.page.url

    def pause(self):
        self.page.pause()
    