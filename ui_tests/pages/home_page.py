from playwright.sync_api import Page
from ui_tests.pages.base_page import BasePage
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

class HomePage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.avatar_dropdown = ".navbar-right .dropdown .avatar"

    def is_loaded(self):
        try:
            self.page.locator(self.avatar_dropdown).wait_for(timeout=500)
            return True
        except PlaywrightTimeoutError:
            return False