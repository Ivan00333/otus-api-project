import pytest
from models.user_request_model import UpdateUserRequest
from models.user_response_model import UpdateUserResponse
from assertions.base_assertions import Assertions

class TestUpdateUser:
    def test_update_user(self, prepare_user, users_client):
        user_id = prepare_user

        new_name = 'Ivan'
        new_job = 'QA'

        payload = UpdateUserRequest(name=new_name, job=new_job)
        response = users_client.update_user(user_id, payload)

        users_client.check_response_and_status_code(response, 200, UpdateUserResponse)
        Assertions.assert_json_value(response, "name", new_name, "Name was not updated")
        Assertions.assert_json_value(response, "job", new_job, "Job was not updated")

    @pytest.mark.xfail
    @pytest.mark.parametrize(
        "new_name, new_job",
    [
        ("", ""),
        (None, None)
    ]
                             )
    def test_negative_update_user(self, prepare_user, users_client, new_name, new_job):
        user_id = prepare_user
        payload = UpdateUserRequest(name=new_name, job=new_job)
        response = users_client.update_user(user_id, payload)

        users_client.check_response_and_status_code(response, 400, UpdateUserResponse)

    @pytest.mark.xfail
    def test_update_user_wrong_id(self, users_client):
        payload = UpdateUserRequest()
        user_id = users_client.get_nonexistent_user_id()
        response = users_client.update_user(user_id, payload)

        Assertions.assert_status_code(response, 404)

