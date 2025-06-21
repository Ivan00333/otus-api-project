import allure
import pytest
from models.user_response_model import RegisterResponse


@allure.feature("User Management")
class TestRegisterUser:

    @allure.story("Register new user")
    @allure.title("Successful user registration")
    def test_register_user(self, users_client):
        with allure.step("Send registration request with default payload"):
            response = users_client.register_user()
        with allure.step("Verify status 200 and response schema RegisterResponse"):
            users_client.check_response_and_status_code(response, 200, RegisterResponse)

    @allure.story("Register unknown user")
    @allure.title("Registration attempt for unknown user should fail")
    def test_register_unknown_user(self, users_client):
        with allure.step("Send registration request for unknown user"):
            response = users_client.register_unknown_user()
        with allure.step("Verify registration failure message"):
            users_client.check_register_unknown_user(response)

    @pytest.mark.parametrize(
        "payload",
        [
            {"email": "", "password": "pistol"},
            {"email": "eve.holt@reqres.in", "password": ""},
            {"password": "pistol"},
            {"email": "eve.holt@reqres.in"}
        ]
    )
    @allure.story("Register user with bad data")
    @allure.title("Registration with invalid payload {payload}")
    def test_register_bad_data(self, users_client, payload):
        with allure.step(f"Send registration request with payload={payload}"):
            response = users_client.register_user(payload)
        with allure.step("Verify registration error for bad data"):
            users_client.check_bad_data_register(response)
