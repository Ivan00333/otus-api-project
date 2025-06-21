from http.client import responses

import pytest

from models.user_response_model import RegisterResponse

class TestRegisterUser:

    def test_register_user(self, users_client):
        response = users_client.register_user()

        users_client.check_response_and_status_code(response, 200, RegisterResponse)

    def test_register_unknown_user(self, users_client):
        response = users_client.register_unknown_user()

        users_client.check_register_unknow_user(response)

    @pytest.mark.parametrize("payload",
                             [
                                 {"email": "", "password": "pistol"},
                                 {"email": "eve.holt@reqres.in", "password": ""},
                                 {"password": "pistol"},
                                 {"email": "eve.holt@reqres.in"}
                             ]
    )
    def test_register_bad_data(self, users_client, payload):
        response = users_client.register_user(payload)

        users_client.check_bad_data_register(response)