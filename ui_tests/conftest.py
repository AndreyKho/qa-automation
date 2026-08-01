from playwright.sync_api import sync_playwright
from ui_tests.pages.login_page import LoginPage
from config.settings import settings
import pytest

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        yield b
        b.close()


@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context(viewport={"width": 1920, "height": 1080}, locale="en-US")
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture(scope="function")
def authenticated_page(page):
    login_page = LoginPage(page)
    login_page.open(f"{settings.gitea_url}/user/login")
    login_page.login(settings.gitea_user, settings.gitea_password)
    return page