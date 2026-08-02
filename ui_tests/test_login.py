from ui_tests.pages.login_page import LoginPage
from ui_tests.pages.home_page import HomePage
from ui_tests.pages.new_repo_page import NewRepoPage
from api_tests.gitea_client import GiteaClient
from config.settings import settings
import pytest

INVALID_LOGIN_MSG = "Username or password is incorrect."
REPO_NAME = "TestRepo"

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

@pytest.mark.ui
@pytest.mark.smoke
def test_create_new_repo(authenticated_page):
    newrepopage = NewRepoPage(authenticated_page)
    try:
        newrepopage.create_repo(REPO_NAME)
        assert newrepopage.current_url == f"{settings.gitea_url}/{settings.gitea_user}/{REPO_NAME}"
    finally:
        GiteaClient().delete_repo(settings.gitea_user, REPO_NAME)