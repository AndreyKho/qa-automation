from playwright.sync_api import Page
from ui_tests.pages.base_page import BasePage
from config.settings import settings

class NewRepoPage(BasePage):
    URL = "/repo/create"
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.repo_name_fill = "#repo_name"
        self.create_repo_btn = ".inline > .button"
        self.code_btn = '[data-text="Code"]'

    def create_repo(self, name: str):
        self.open(settings.gitea_url + self.URL)
        self.type(self.repo_name_fill, name)
        self.click(self.create_repo_btn)
        self.page.locator(self.code_btn).wait_for(timeout=1000)