from api.base_client import BaseClient
from config import Settings
from models.user_request_model import CreateUserRequest, UpdateUserRequest
from api.routes import ApiRoutes
from assertions.base_assertions import Assertions
from requests import Response


class UsersClient(BaseClient):
    def create_user(self, data: CreateUserRequest | None = None):
        if data is None:
            data = CreateUserRequest()

        payload = data.model_dump()

        return self.post(ApiRoutes.CREATE_USER, json=payload)

    def get_value_by_parameter(self, response: Response, parameter: str):
        data = response.json()

        return data[parameter]

    def update_user(self, user_id: int, data: UpdateUserRequest | None = None):
        if data is None:
            data = UpdateUserRequest()

        payload = data.model_dump()

        return self.put(ApiRoutes.UPDATE_USER.with_id(id=user_id), json=payload)

    def delete_user(self, user_id: int):

        return self.delete(ApiRoutes.DELETE_USER.with_id(user_id))

    def check_response_and_status_code(self, response: Response, expected_status_code: int, schema):
        Assertions.assert_status_code(response, expected_status_code)
        Assertions.assert_schema(response, schema)


def get_users_client(settings: Settings):

    return UsersClient(settings.users_client)




