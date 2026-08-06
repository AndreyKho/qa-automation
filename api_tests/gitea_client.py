import requests
import allure
from config.settings import settings

class GiteaClient:

    def __init__(self, base_url=settings.gitea_url, username=settings.gitea_user, password=settings.gitea_password, timeout=10):
        self.base_url = f"{base_url}/api/v1"
        self.session = requests.Session()
        self.session.auth = (username, password)
        self.timeout = timeout
        self.session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

    @allure.step("DELETE /repos/{owner}/{repo}")
    def delete_repo(self, owner, repo)-> None:
        response = self.session.delete(f"{self.base_url}/repos/{owner}/{repo}", timeout=self.timeout)
        response.raise_for_status()

    @allure.step("POST /user/repos — создание репозитория {name}")
    def create_repo(self, name, description="", private=False):
        body = {
            "name": name,
            "description": description,
            "private": private
        }
        response = self.session.post(f"{self.base_url}/user/repos", json=body, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    @allure.step("GET /repos/{owner}/{repo}")
    def get_repo(self, owner, repo):
        response = self.session.get(f"{self.base_url}/repos/{owner}/{repo}", timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    @allure.step("PATCH /repos/{owner}/{repo}")
    def update_repo(self, owner, repo, **fields):
        response = self.session.patch(f"{self.base_url}/repos/{owner}/{repo}", json=fields, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    @allure.step("GET /user/repos — список репозиториев")
    def list_repos(self):
        response = self.session.get(f"{self.base_url}/user/repos", timeout=self.timeout)
        response.raise_for_status()
        return response.json()