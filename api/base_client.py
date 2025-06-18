import requests
from config import get_base_url

class BaseClient:
    def __init__(self):
        self.base_url = get_base_url()
        self.session = requests.Session()

    def post(self, api: str, json: dict = None, params: dict = None, headers: dict = None):
        url =
        response = self.session.post(f"{self.base_url}{api}")

        return response
