from api.base_client import BaseClient
from config import Settings
from models.user_request_model import CreateUserRequest, UpdateUserRequest, RegisterRequest, RegisterUnknownUserRequest
from models.user_response_model import UsersListResponse, RegisterResponse
from api.routes import ApiRoutes
from assertions.base_assertions import Assertions
from requests import Response
import allure


class UsersClient(BaseClient):
    """
    Клиент для работы с эндпоинтами /users и /register на reqres.in
    """

    @allure.step("Get single user by id={user_id}")
    def get_single_user(self, user_id: int) -> Response:
        return self.get(ApiRoutes.GET_SINGLE_USER.with_id(id=user_id))

    @allure.step("Get users page={page}")
    def get_users(self, page: int = 1) -> Response:
        return self.get(ApiRoutes.GET_USERS.value.format(page=page))

    @allure.step("Create user with payload={data}")
    def create_user(self, data: CreateUserRequest | dict = None) -> Response:
        if data is None:
            data = CreateUserRequest()
            payload = data.model_dump()
        else:
            payload = data
        return self.post(ApiRoutes.CREATE_USER.value, json=payload)

    @allure.step("Update user id={user_id} with payload={data}")
    def update_user(self, user_id: int, data: UpdateUserRequest) -> Response:
        payload = data.model_dump(exclude_none=True)
        return self.put(
            ApiRoutes.UPDATE_USER.with_id(id=user_id),
            json=payload
        )

    @allure.step("Delete user id={user_id}")
    def delete_user(self, user_id: int) -> Response:
        return self.delete(
            ApiRoutes.DELETE_USER.with_id(id=user_id)
        )

    @allure.step("Register user with payload={data}")
    def register_user(self, data: RegisterRequest | dict = None) -> Response:
        if data is None:
            data = RegisterRequest()
            payload = data.model_dump()
        else:
            payload = data
        return self.post(ApiRoutes.REGISTER.value, json=payload)

    @allure.step("Register unknown user with payload={data}")
    def register_unknown_user(self, data: RegisterUnknownUserRequest | dict = None) -> Response:
        if data is None:
            data = RegisterUnknownUserRequest()
            payload = data.model_dump()
        else:
            payload = data
        return self.post(ApiRoutes.REGISTER.value, json=payload)

    @allure.step("Extract value '{key}' from response JSON")
    def get_value_by_parameter(self, response: Response, key: str):
        data = response.json()
        if key not in data:
            raise KeyError(f"Key '{key}' not found in response JSON")
        return data[key]

    @allure.step("Compute nonexistent user id")
    def get_nonexistent_user_id(self) -> int:
        response = self.get_users()
        users_page = UsersListResponse.model_validate(response.json())
        page = 1
        all_ids = set()
        while True:
            for user in users_page.data:
                all_ids.add(user.id)
            if page >= users_page.total_pages:
                break
            page += 1
        return (max(all_ids) + 1) if all_ids else 1

    @allure.step("Check register error message '{expected_msg}'")
    def check_response_error_msg(
        self,
        response: Response,
        expected_msg: str | list
    ) -> None:
        Assertions.assert_status_code(response, 400)
        data = response.json()
        Assertions.assert_json_has_key(response, "error")
        if isinstance(expected_msg, str):
            assert data["error"] == expected_msg, (
                f"Expected '{expected_msg}', got: {data['error']}"
            )
        else:
            assert data["error"] in expected_msg, (
                f"Expected one of {expected_msg}, got: {data['error']}"
            )

    @allure.step("Check register unknown user failure")
    def check_register_unknown_user(self, response: Response) -> None:
        self.check_response_error_msg(
            response,
            "Note: Only defined users succeed registration"
        )

    @allure.step("Check bad data register error")
    def check_bad_data_register(self, response: Response) -> None:
        self.check_response_error_msg(
            response,
            ["Missing email or username", "Missing password"]
        )

    @allure.step("Check users page {page} in response")
    def check_page_users(self, response: Response, page: int) -> None:
        data = UsersListResponse.model_construct(**response.json())
        page_response = data.page
        assert page_response == page, f"Expected page {page}, got {page_response}"

    @allure.step("Check deleted user id={user_id} returns empty")
    def check_deleted_user(self, user_id: int) -> None:
        response = self.get_single_user(user_id)
        Assertions.assert_status_code(response, 404)
        assert response.json() == {}, f"Expected empty JSON object, got: {response.json()}"

    @allure.step("Validate response and status code {expected_status_code}")
    def check_response_and_status_code(
            self,
            response: Response,
            expected_status_code: int,
            schema
    ) -> None:
        # Убедитесь, что передаётся сам Response, а не response.text
        Assertions.assert_status_code(response, expected_status_code)
        # Передаём Response объект в assert_schema
        Assertions.assert_schema(response, schema)


def get_users_client(settings: Settings) -> UsersClient:
    return UsersClient(settings.users_client)





