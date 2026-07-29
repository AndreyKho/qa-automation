from playwright.sync_api import sync_playwright
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
        