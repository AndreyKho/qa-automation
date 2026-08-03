import pytest
import requests
from config.settings import settings
from api_tests.helpers import unique_repo_name

NEW_DESCRIPTION = "updated by autotest"

@pytest.mark.api
@pytest.mark.smoke
def test_create_repo(gitea_client):
    name = unique_repo_name()
    try:
        created = gitea_client.create_repo(name)
        assert isinstance(created["id"], int)
        assert created["name"] == name
        assert created["owner"]["login"] == settings.gitea_user
        assert created["private"] is False
    finally:
        gitea_client.delete_repo(settings.gitea_user, name)

@pytest.mark.api
@pytest.mark.smoke
def test_get_repo(gitea_client, repo):
    response = gitea_client.get_repo(settings.gitea_user, repo["name"])
    assert response["id"] == repo["id"]
    assert response["name"] == repo["name"]
    assert response["full_name"] == repo["full_name"]

@pytest.mark.api
@pytest.mark.regression
def test_update_repo(gitea_client, repo):
    response = gitea_client.update_repo(settings.gitea_user, repo["name"], description=NEW_DESCRIPTION)
    assert response["description"] == NEW_DESCRIPTION
    fetched = gitea_client.get_repo(settings.gitea_user, repo["name"])
    assert fetched["description"] == NEW_DESCRIPTION

@pytest.mark.api
@pytest.mark.regression
def test_delete_repo(gitea_client):
    name = unique_repo_name()
    gitea_client.create_repo(name)
    gitea_client.delete_repo(settings.gitea_user, name)
    with pytest.raises(requests.HTTPError):
        gitea_client.get_repo(settings.gitea_user, name)


@pytest.mark.api
@pytest.mark.regression
def test_create_duplicate_repo(gitea_client, repo):
    with pytest.raises(requests.HTTPError):
        gitea_client.create_repo(repo["name"])



@pytest.mark.api
@pytest.mark.regression
def test_list_repos(gitea_client, repo):
    all_repos = gitea_client.list_repos()
    assert isinstance(all_repos, list)
    repo_names = [item["name"] for item in all_repos]
    assert repo["name"] in repo_names

@pytest.mark.api
@pytest.mark.regression
@pytest.mark.parametrize("private", [True, False])
def test_create_private_repo(private, gitea_client):
    name = unique_repo_name()
    try:
        gitea_client.create_repo(name, private=private)
        fetched = gitea_client.get_repo(settings.gitea_user, name)
        assert fetched["private"] == private
    finally:
        gitea_client.delete_repo(settings.gitea_user, name)