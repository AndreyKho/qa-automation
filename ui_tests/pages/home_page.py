from playwright.sync_api import Page
from ui_tests.pages.base_page import BasePage
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

class HomePage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.avatar_dropdown = ".navbar-right .dropdown .avatar"
        self.sign_out_btn = 'a[data-url="/user/logout"]'
        self.sign_in_btn = 'a[href^="/user/login"]'

    def is_loaded(self):
        try:
            self.page.locator(self.avatar_dropdown).wait_for(timeout=1000)
            return True
        except PlaywrightTimeoutError:
            return False

    def _open_user_menu(self):
        self.click(self.avatar_dropdown)

    def logout(self):
        self._open_user_menu()
        self.click(self.sign_out_btn)
        self.page.locator(self.sign_in_btn).wait_for(timeout=1000)
