import pytest
from models.user_request_model import UpdateUserRequest

class TestUpdateUser:
    def test_update_user(self, prepare_user, users_client):
        user_id = prepare_user

        users_client.update_user(user_id, UpdateUserRequest)