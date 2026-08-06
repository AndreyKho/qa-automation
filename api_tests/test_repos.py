import pytest
import requests
import allure
from config.settings import settings
from api_tests.helpers import unique_repo_name


@pytest.mark.api
@allure.epic("API")
@allure.feature("Репозитории")
class TestRepos:
    NEW_DESCRIPTION = "updated by autotest"

    @pytest.mark.smoke
    @allure.story("Создание репозитория")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_repo(self, gitea_client):
        name = unique_repo_name()
        try:
            created = gitea_client.create_repo(name)
            assert isinstance(created["id"], int)
            assert created["name"] == name
            assert created["owner"]["login"] == settings.gitea_user
            assert created["private"] is False
        finally:
            gitea_client.delete_repo(settings.gitea_user, name)

    @pytest.mark.smoke
    @allure.story("Получение репозитория по имени")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_repo(self, gitea_client, repo):
        response = gitea_client.get_repo(settings.gitea_user, repo["name"])
        assert response["id"] == repo["id"]
        assert response["name"] == repo["name"]
        assert response["full_name"] == repo["full_name"]

    @pytest.mark.regression
    @allure.story("Изменение полей репозитория")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_repo(self, gitea_client, repo):
        response = gitea_client.update_repo(settings.gitea_user, repo["name"], description=self.NEW_DESCRIPTION)
        assert response["description"] == self.NEW_DESCRIPTION
        fetched = gitea_client.get_repo(settings.gitea_user, repo["name"])
        assert fetched["description"] == self.NEW_DESCRIPTION

    @pytest.mark.regression
    @allure.story("Удаление репозитория")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_repo(self, gitea_client):
        name = unique_repo_name()
        gitea_client.create_repo(name)
        gitea_client.delete_repo(settings.gitea_user, name)
        with pytest.raises(requests.HTTPError):
            gitea_client.get_repo(settings.gitea_user, name)

    @pytest.mark.regression
    @allure.story("Ошибка при дублировании имени")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_duplicate_repo(self, gitea_client, repo):
        with pytest.raises(requests.HTTPError):
            gitea_client.create_repo(repo["name"])


    @pytest.mark.regression
    @allure.story("Список репозиториев пользователя")
    @allure.severity(allure.severity_level.NORMAL)
    def test_list_repos(self, gitea_client, repo):
        all_repos = gitea_client.list_repos()
        assert isinstance(all_repos, list)
        repo_names = [item["name"] for item in all_repos]
        assert repo["name"] in repo_names

    @pytest.mark.regression
    @allure.story("Создание репозитория")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("private", [True, False])
    def test_create_private_repo(self, private, gitea_client):
        name = unique_repo_name()
        try:
            gitea_client.create_repo(name, private=private)
            fetched = gitea_client.get_repo(settings.gitea_user, name)
            assert fetched["private"] == private
        finally:
            gitea_client.delete_repo(settings.gitea_user, name)