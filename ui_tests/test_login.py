from ui_tests.pages.login_page import LoginPage
from ui_tests.pages.home_page import HomePage
from config.settings import settings
import pytest
import allure

@pytest.mark.ui
@allure.epic("UI")
@allure.feature("Аутентификация")
class TestLogin:
    INVALID_LOGIN_MSG = "Username or password is incorrect."

    @pytest.mark.smoke
    @allure.story("Авторизация с валидными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login(self, page):
        loginpage = LoginPage(page)
        loginpage.open(f"{settings.gitea_url}/user/login")
        loginpage.login(settings.gitea_user, settings.gitea_password)
        homepage = HomePage(page)
        assert homepage.is_loaded()

    @pytest.mark.regression
    @allure.story("Ошибка авторизации с неверным паролем")
    @allure.severity(allure.severity_level.NORMAL)
    def test_invalid_login(self, page):
        loginpage = LoginPage(page)
        loginpage.open(f"{settings.gitea_url}/user/login")
        loginpage.login(settings.gitea_user, "testpassword")
        assert loginpage.get_error_message() == self.INVALID_LOGIN_MSG

    @pytest.mark.regression
    @allure.story("Выход из аккаунта")
    @allure.severity(allure.severity_level.NORMAL)
    def test_logout(self, authenticated_page):
        homepage = HomePage(authenticated_page)
        homepage.logout()
        assert not homepage.is_loaded()