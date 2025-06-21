import requests
import allure
from urllib.parse import urljoin
from utils.logger import get_logger
from config import HTTPClientConfig
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


class BaseClient:
    def __init__(self, config: HTTPClientConfig):
        self.logger = get_logger(self.__class__.__name__)
        self.session = requests.Session()

        retries = Retry(
            total=5,
            backoff_factor=0.3,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

        self.session.headers.update(
            {
                'Accept': '*/*',
                "x-api-key": "reqres-free-v1",
                "Connection": "keep-alive",
                "Content-Type": "application/json"
            }
        )
        self.base_url = config.base_url

    @allure.step("Make {method} request to {path}")
    def _request(self, method: str, path: str, **kwargs):
        url = urljoin(self.base_url, str(path))
        self.logger.info(f"{method} {url} | params={kwargs.get('params')} | json={kwargs.get('json')}")
        response = self.session.request(method, url, **kwargs)
        self.logger.info(f"→ {response.status_code} | {response.text}")
        return response

    @allure.step("POST request to {path}")
    def post(self, path: str, json: dict = None, **kwargs):
        return self._request("POST", path, json=json, **kwargs)

    @allure.step("GET request to {path}")
    def get(self, path: str, params: dict = None, **kwargs):
        return self._request("GET", path, params=params, **kwargs)

    @allure.step("PUT request to {path}")
    def put(self, path: str, json: dict = None, **kwargs):
        return self._request("PUT", path, json=json, **kwargs)

    @allure.step("DELETE request to {path}")
    def delete(self, path: str, **kwargs):
        return self._request("DELETE", path, **kwargs)
