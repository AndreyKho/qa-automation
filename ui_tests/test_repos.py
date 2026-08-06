import allure
import pytest
from config.settings import settings
from ui_tests.pages.new_repo_page import NewRepoPage
from api_tests.gitea_client import GiteaClient

@pytest.mark.ui
@allure.epic("UI")
@allure.feature("Репозитории")
class TestRepo:
    REPO_NAME = "TestRepo"

    @pytest.mark.smoke
    @allure.story("Создание нового репозитория")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_new_repo(self, authenticated_page):
        newrepopage = NewRepoPage(authenticated_page)
        try:
            newrepopage.create_repo(self.REPO_NAME)
            assert newrepopage.current_url == f"{settings.gitea_url}/{settings.gitea_user}/{self.REPO_NAME}"
        finally:
            GiteaClient().delete_repo(settings.gitea_user, self.REPO_NAME)