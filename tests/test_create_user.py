import pytest
from models.user_request_model import CreateUserRequest
from models.user_response_model import CreateUserResponse
from assertions.base_assertions import Assertions


class TestCreateUser:

    def test_create_user(self, users_client):
        response = users_client.create_user()
        users_client.check_response_and_status_code(response, 201, CreateUserResponse)

    @pytest.mark.xfail
    @pytest.mark.parametrize("bad_name", ["", None, 2])
    def test_create_user_bad_name(self, users_client, bad_name):
        payload = CreateUserRequest.model_construct(name=bad_name)
        response = users_client.create_user(payload)

        Assertions.assert_status_code(response, 400)

    @pytest.mark.xfail
    @pytest.mark.parametrize("bad_job", ["", None, 4])
    def test_create_user_bad_job(self, users_client, bad_job):
        payload = CreateUserRequest.model_construct(job=bad_job)
        response = users_client.create_user(payload)

        Assertions.assert_status_code(response, 400)

