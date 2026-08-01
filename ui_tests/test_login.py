from ui_tests.pages.login_page import LoginPage
from ui_tests.pages.home_page import HomePage
from config.settings import settings
import pytest

INVALID_LOGIN_MSG = "Username or password is incorrect."

@pytest.mark.ui
@pytest.mark.smoke
def test_login(page):
    loginpage = LoginPage(page)
    loginpage.open(f"{settings.gitea_url}/user/login")
    loginpage.login(settings.gitea_user, settings.gitea_password)
    homepage = HomePage(page)
    assert homepage.is_loaded()

@pytest.mark.ui
@pytest.mark.regression
def test_invalid_login(page):
    loginpage = LoginPage(page)
    loginpage.open(f"{settings.gitea_url}/user/login")
    loginpage.login(settings.gitea_user, "testpassword")
    assert loginpage.get_error_message() == INVALID_LOGIN_MSG

@pytest.mark.ui
@pytest.mark.regression
def test_login_out(authenticated_page):
    homepage = HomePage(authenticated_page)
    homepage.logout()
    assert not homepage.is_loaded()