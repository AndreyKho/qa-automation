from playwright.sync_api import Page
from ui_tests.pages.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.username_fill = "#user_name"
        self.password_fill = "#password"
        self.sign_in_btn = ".field > button"
        self.invalid_login_msg = ".negative.message > p"

    def login(self, username, password):
        self.type(self.username_fill, username)
        self.type(self.password_fill, password)
        self.click(self.sign_in_btn)

    def get_error_message(self):
        return self.get_text(self.invalid_login_msg)

    