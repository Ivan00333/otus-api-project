from api.base_client import BaseClient
from config import Settings
from models.user_request_model import CreateUserRequest, UpdateUserRequest
from api.routes import ApiRoutes
from assertions.base_assertions import Assertions
from requests import Response


class UsersClient(BaseClient):
    def create_user(self, user: CreateUserRequest):
        user_data = user()

        return self.post(ApiRoutes.CREATE_USER, json=user_data.model_dump(mode='json'))

    def check_response_and_status_code(self, response: Response, expected_status_code: int, schema):
        Assertions.assert_status_code(response, expected_status_code)
        Assertions.assert_schema(response, schema)

def get_users_client(settings: Settings):

    return UsersClient(settings.users_client)




