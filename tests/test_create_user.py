import pytest
from models.user_request_model import CreateUserRequest
from models.user_response_model import CreateUserResponse
from assertions.base_assertions import Assertions
import allure


@allure.feature("User Management")
class TestCreateUser:

    @allure.story("Positive Create User")
    @allure.title("Create a new user with default data")
    def test_create_user(self, users_client):
        with allure.step("Create user via API"):
            response = users_client.create_user()
        with allure.step("Verify status code and response schema"):
            users_client.check_response_and_status_code(response, 201, CreateUserResponse)

    @pytest.mark.xfail(reason="Reqres.in does not validate bad name", strict=False)
    @pytest.mark.parametrize("bad_name", ["", None, 2])
    @allure.story("Negative Create User")
    @allure.title("Create user with invalid name: {bad_name}")
    def test_create_user_bad_name(self, users_client, bad_name):
        with allure.step(f"Construct payload with bad name={bad_name}"):
            payload = CreateUserRequest.model_construct(name=bad_name)
        with allure.step("Send create user request"):
            response = users_client.create_user(payload)
        with allure.step("Verify 400 status code for invalid name"):
            Assertions.assert_status_code(response, 400)

    @pytest.mark.xfail(reason="Reqres.in does not validate bad job", strict=False)
    @pytest.mark.parametrize("bad_job", ["", None, 4])
    @allure.story("Negative Create User")
    @allure.title("Create user with invalid job: {bad_job}")
    def test_create_user_bad_job(self, users_client, bad_job):
        with allure.step(f"Construct payload with bad job={bad_job}"):
            payload = CreateUserRequest.model_construct(job=bad_job)
        with allure.step("Send create user request"):
            response = users_client.create_user(payload)
        with allure.step("Verify 400 status code for invalid job"):
            Assertions.assert_status_code(response, 400)

