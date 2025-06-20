import pytest

from models.user_request_model import CreateUserRequest
from assertions.base_assertions import Assertions

class TestDeleteUser:
    def test_delete_user(self, users_client):
        user_id = users_client.create_user()

        response = users_client.delete_user(user_id)
        Assertions.assert_status_code(response, 204)
        users_client.check_deleted_user(user_id)

    @pytest.mark.xfail
    def test_negative_delete_user(self, users_client):
        user_id = users_client.get_nonexistent_user_id()
        response = users_client.delete_user(user_id)

        Assertions.assert_status_code(response, 404)
