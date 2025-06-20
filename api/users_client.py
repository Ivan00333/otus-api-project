from api.base_client import BaseClient
from config import Settings
from models.user_request_model import CreateUserRequest, UpdateUserRequest
from models.user_response_model import UsersListResponse, SingleUserResponse
from api.routes import ApiRoutes
from assertions.base_assertions import Assertions
from requests import Response


class UsersClient(BaseClient):

    def get_single_user(self, user_id: int):

        return self.get(ApiRoutes.GET_SINGLE_USER.with_id(id=user_id))

    def get_users(self, page: int = 1):

        return self.get(ApiRoutes.GET_USERS.value.format(page=page))

    def create_user(self, data: CreateUserRequest | None = None):
        if data is None:
            data = CreateUserRequest()

        payload = data.model_dump()

        return self.post(ApiRoutes.CREATE_USER, json=payload)

    def get_value_by_parameter(self, response: Response, key: str):
        data = response.json()

        if key not in data:
            raise KeyError(f"Key '{key}' not found in response JSON")

        return data[key]

    def update_user(self, user_id: int, data: UpdateUserRequest):
        payload = data.model_dump(exclude_none=True)

        return self.put(ApiRoutes.UPDATE_USER.with_id(id=user_id), json=payload)

    def delete_user(self, user_id: int):

        return self.delete(ApiRoutes.DELETE_USER.with_id(id=user_id))

    def get_nonexistent_user_id(self):
        response = self.get_users()
        users_page = UsersListResponse.model_validate(response.json())
        page = 1
        all_ids = set()

        while True:
            for user in users_page.data:
                all_ids.add(user.id)

            if page > users_page.total_pages:
                break

        return (max(all_ids) + 1) if all_ids else 1

    def check_page_users(self, response: Response, page: int):
        data = UsersListResponse.model_construct(**response.json())
        page_response = data.page

        assert page_response == page, f"Expected page {page}, got {page_response}"

    def check_deleted_user(self, user_id: int):
        response = self.put(ApiRoutes.GET_SINGLE_USER.with_id(id=user_id))
        Assertions.assert_status_code(response, 404)
        assert response.json() == {}, f"Expected empty JSON object, got: {response.json()}"

    def check_response_and_status_code(self, response: Response, expected_status_code: int, schema):
        Assertions.assert_status_code(response, expected_status_code)
        Assertions.assert_schema(response, schema)


def get_users_client(settings: Settings):

    return UsersClient(settings.users_client)




