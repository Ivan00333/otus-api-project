import requests
from urllib.parse import urljoin
from utils.logger import get_logger
from config import HTTPClientConfig


class BaseClient:
    def __init__(self, config: HTTPClientConfig):
        self.logger = get_logger(self.__class__.__name__)
        self.session = requests.Session()
        self.session.headers.update({'Accept': 'application/json', "x-api-key": "reqres-free-v1"})
        self.base_url = config.base_url

    def _request(self, method: str, path: str, **kwargs):
        url = urljoin(self.base_url, str(path))
        self.logger.info(f"{method} {url} | params={kwargs.get('params')} | json={kwargs.get('json')}")
        response = self.session.request(method, url, **kwargs)
        self.logger.info(f"→ {response.status_code} | {response.text}")
        return response

    def post(self, path: str, json: dict = None, **kwargs):
        return self._request("POST", path, json=json, **kwargs)

    def get(self, path: str, params: dict = None, **kwargs):
        return self._request("GET", path, params=params, **kwargs)

    def put(self, path: str, json: dict = None, **kwargs):
        return self._request(path, json=json, **kwargs)

    def delete(self, path: str, **kwargs):
        return self._request(path, **kwargs)
