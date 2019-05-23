import requests
from os import getenv


class GithubIntegration:
    ROOT = 'https://api.github.com/'

    def __init__(self, owner, repository):
        self.owner = owner
        self.repository = repository

    def createIssue(self, issue):
        url = '{}repos/{owner}/{repository}/issues?access_token={}'.format(
            GithubIntegration.ROOT,
            getenv('GITHUB_ACCESS_TOKEN'),
            ** vars(self)
        )

        response = requests.post(url, json=issue)
        res_data = response.json()

        return res_data
