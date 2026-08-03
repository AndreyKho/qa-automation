import pytest
from api_tests.gitea_client import GiteaClient
from config.settings import settings
from api_tests.helpers import unique_repo_name


@pytest.fixture(scope="session")
def gitea_client():
    return GiteaClient()

@pytest.fixture(scope="function")
def repo(gitea_client):
    created_repo = gitea_client.create_repo(unique_repo_name())
    yield created_repo
    try:
        gitea_client.delete_repo(settings.gitea_user, unique_repo_name())
    except:
        pass