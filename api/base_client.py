import requests
from config import settings
from urllib.parse import urljoin

class BaseClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'Accept': 'application/json'})
        user_client = settings.users_client
        self.base_url = user_client.base_url

    def _request(self, method: str, path: str, **kwargs):
        url = urljoin(self.base_url, path)
        response = self.session.request(method, url)
        return response

    def post(self, path: str, json: dict = None):
        return self._request("POST", path, json=json)
