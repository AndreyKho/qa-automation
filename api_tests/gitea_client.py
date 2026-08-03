import requests
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

    def delete_repo(self, owner, repo)-> None:
        response = self.session.delete(f"{self.base_url}/repos/{owner}/{repo}", timeout=self.timeout)
        response.raise_for_status()

    def create_repo(self, name, description="", private=False):
        body = {
            "name": name,
            "description": description,
            "private": private
        }
        response = self.session.post(f"{self.base_url}/user/repos", json=body, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get_repo(self, owner, repo):
        response = self.session.get(f"{self.base_url}/repos/{owner}/{repo}", timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def update_repo(self, owner, repo, **fields):
        response = self.session.patch(f"{self.base_url}/repos/{owner}/{repo}", json=fields, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def list_repos(self):
        response = self.session.get(f"{self.base_url}/user/repos", timeout=self.timeout)
        response.raise_for_status()
        return response.json()