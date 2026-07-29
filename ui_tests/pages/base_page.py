from playwright.sync_api import Page

class BasePage():
    def __init__(self, page: Page) -> None:
        self.page = page

    def open(self, url):
        self.page.goto(url)

    def click(self, locator: str):
        self.page.locator(locator).click()

    def type(self, locator: str, text: str):
        self.page.locator(locator).fill(text)

    def get_text(self, locator: str)-> str:
        text = self.page.locator(locator).inner_text()
        return text

    @property
    def current_url(self):
        return self.page.url
    
