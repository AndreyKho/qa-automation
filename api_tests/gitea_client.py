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

    def delete_repo(self, owner, repo):
        response = self.session.delete(f"{self.base_url}/repos/{owner}/{repo}", timeout=self.timeout)
        response.raise_for_status()